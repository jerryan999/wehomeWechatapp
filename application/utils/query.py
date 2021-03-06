from ..models import City, IndexPage, CityPage, HomePage, UnmatchedPlace, FeedBack, User, Phone, Collection, CityCount, CityRankingList, TotalRankingList, CityPct
from ..models import SuperRankingList, CarouselFigure, Answer, UserQueryFrequency, CityCollection, ReadCondition, Picture
from index import app, db, bcrypt
from flask import jsonify
from sqlalchemy import and_
import hashlib
from urllib import quote_plus
import requests
import json
from sqlalchemy.exc import DataError, IntegrityError
import datetime
import sys
from qiniu import Auth
from flask.json import dumps
import pandas as pd

FIVE_MINUTES = 60*5

class QueryHelper(object):
  'You can use this class query the complex query via the SqlAlchemy query'
  @classmethod
  def to_json_with_filter(cls, rows_dict, columns):
    d = {'success':True}
    for k, v in rows_dict.items():
      # handle the dict and integer and float
      if type(v) == type({}) or type(v) == type(1) or type(v) == type(1.0) or type(v) == type('') or type(v) == type(u'') or type(v) == type(True) \
       or type(datetime.datetime.now()) == type(v):
        d[k] = v
      # handle the model object
      elif (type(v) != type([])) and (v is not None):
        d[k] = {_k:_v for _k, _v in v.__dict__.items() if _k in columns}
      # handle the list
      elif v is not None:
        l = []
        for item in v:
          # handle the model object
          if type(item) != type({}):
            l.append({_k:_v for _k, _v in item.__dict__.items() if _k in columns})
          # handle the dict  
          else:
            l.append({_k:_v for _k, _v in item.items() if _k in columns})
        d[k] = l
      # handle the None  
      else:
        d[k] = {}
    return jsonify(d), 200

  @classmethod
  def to_dict_with_filter(cls, rows_dict, columns):
    d = {'success':True}
    for k, v in rows_dict.items():
      # handle the dict and integer and float
      if type(v) == type({}) or type(v) == type(1) or type(v) == type(1.0) or type(v) == type('') or type(v) == type(u'') or type(v) == type(True) \
       or type(datetime.datetime.now()) == type(v):
        d[k] = v
      # handle the model object
      elif (type(v) != type([])) and (v is not None):
        d[k] = {_k:_v for _k, _v in v.__dict__.items() if _k in columns}
      # handle the list
      elif v is not None:
        l = []
        for item in v:
          # handle the model object
          if type(item) != type({}):
            l.append({_k:_v for _k, _v in item.__dict__.items() if _k in columns})
          # handle the dict  
          else:
            l.append({_k:_v for _k, _v in item.items() if _k in columns})
        d[k] = l
      # handle the None  
      else:
        d[k] = {}
    return d

  @classmethod
  def get_index_page(cls):
    return IndexPage.query.first()

  @classmethod
  def get_cities(cls):
    return City.query.all()

  @classmethod
  def get_cities_filter_id(cls, min_id, max_id):
    return City.query.filter(City.id.between(min_id, max_id)).all()

  @classmethod
  def get_city_page_with_city_id(cls, city_id):
    return CityPage.query.filter_by(city_id=city_id).first()

  @classmethod
  def get_home_page_with_home_id(cls, home_id):
    return HomePage.query.filter_by(id=home_id).first()

  @classmethod
  def get_home_page_with_place_name(cls, place_name):
    md5 = hashlib.md5()
    md5.update(place_name.encode("utf-8"))
    return HomePage.query.filter(and_(HomePage.hash_code==md5.hexdigest(), HomePage.map_box_place_name==place_name)).order_by(HomePage.score.desc()).first()

  @classmethod
  def get_unmatched_place_with_name_type(cls, place_name, type):
    return UnmatchedPlace.query.filter(and_(UnmatchedPlace.place_name==place_name, UnmatchedPlace.type==type)).first()

  @classmethod
  def add_unmatched_place(cls, place_name, type):
    place = cls.get_unmatched_place_with_name_type(place_name, type)
    if place:
      return True
    try:
      place = UnmatchedPlace(place_name=place_name, type=type)
      db.session.add(place)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return False
    return True

  @classmethod
  def parse_address_by_map_box(cls, place_name):
    try:
      releveance = 0.7
      url = "https://api.tiles.mapbox.com/geocoding/v5/mapbox.places/{address}.json".format(address=quote_plus(place_name))
      querystring = {"country":"us","limit":"1","access_token": app.config['MAP_BOX_ACCESSTOKEN']}
      headers = {
          'cache-control': "no-cache",
          }
      response = requests.request("GET", url, headers=headers, params=querystring, proxies=None, timeout=2)
      result = json.loads(response.text)
      if len(result['features'])>0 and result['features'][0]['relevance']>= releveance:
        return result['features'][0]['place_name']
    except Exception as e:
      return place_name
    return place_name

  @classmethod
  def add_feed_back(cls, content, user_id):
    try:
      fb = FeedBack(content=content, user_id=user_id)
      db.session.add(fb)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return False
    return True

  @classmethod
  def get_wechat_sessionkey_and_openid(cls, code):
    querystring = {
      'appid': app.config['WECHAT_APP_ID'],
      'secret': app.config['WECHAT_APP_SECRET'],
      'js_code': code,
      'grant_type': app.config['WECHAT_APP_GRANT_TYPE']
      }
    response = requests.request("GET", app.config['WECHAT_APP_CODE_URL'], params=querystring)
    return json.loads(response.text)

  @classmethod
  def get_user_with_openid(cls, openid):
    return User.query.filter_by(openid=openid).first()

  @classmethod
  def add_or_set_user(cls, openid, nick_name, gender, language, city, province, country, avatar_url, phone=None):
    user = cls.get_user_with_openid(openid=openid)
    if user:
      user.nick_name, user.gender = nick_name, gender
      user.language, user.city = language, city
      user.province, user.country = province, country
      user.avatar_url = avatar_url
    else:
      user = User(openid=openid, nick_name=nick_name, gender=gender,
        language=language, city=city, province=province, country=country, 
        avatar_url=avatar_url, phone=phone)
    try:
      db.session.merge(user)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return None
    return cls.get_user_with_openid(openid=openid)

  @classmethod
  def get_phone_with_phone_and_country(cls, phone, country):
    return Phone.query.filter_by(phone=phone, country=country).first()

  @classmethod
  def add_or_set_phone(cls, phone_nu, country, verification_code, verification_code_created_at, is_verified=False):
    phone = cls.get_phone_with_phone_and_country(phone=phone_nu, country=country)
    try:
      if not phone:
        phone = Phone(phone_nu, country, verification_code,
          verification_code_created_at, is_verified)
      else:
        phone.phone, phone.country = phone_nu, country
        phone.verification_code, phone.is_verified = verification_code, is_verified
        phone.verification_code_created_at = verification_code_created_at
      db.session.merge(phone)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return None
    return phone

  @classmethod
  def get_phone_with_phone_and_country(cls, phone, country):
    return Phone.query.filter(and_(Phone.phone==phone, Phone.country==country)).first()

  @classmethod
  def verify_sms_code(cls, phone, country, code, expiration=FIVE_MINUTES):
    phone = cls.get_phone_with_phone_and_country(phone, country)
    if phone and phone.verification_code == code \
        and phone.verification_code_created_at + datetime.timedelta(seconds=expiration) > datetime.datetime.utcnow():
      return True 
    return False

  @classmethod
  def get_user_with_id(cls, user_id):
    return User.query.filter_by(id=user_id).first()

  @classmethod
  def set_user_phone_with_id(cls, user_id, phone, country_code, is_verified=True):
    user = cls.get_user_with_id(user_id=user_id)
    # valdate_user = cls.get_user_with_phone_and_country(phone=phone, country=country_code)
    # if (not user) or (valdate_user):
    #   return False
    try:
      user.phone = phone
      user.country_code = country_code
      db.session.merge(user)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return False
    return True

  @classmethod
  def set_phone_is_verified(cls, phone, country):
    phone = cls.get_phone_with_phone_and_country(phone=phone, country=country)
    try:
      phone.is_verified = True
      db.session.merge(phone)
      db.session.commit()
    except Exception as e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return False
    return True

  @classmethod
  def get_collection_with_user_home(cls, user_id, home_id):
    return Collection.query.filter(and_(Collection.user_id==user_id, Collection.home_id==home_id)).first()

  @classmethod
  def get_active_collection_with_user_home(cls, user_id, home_id):
    return Collection.query.filter(and_(Collection.user_id==user_id, Collection.home_id==home_id,Collection.is_active==True)).first()

  @classmethod
  def set_collection(cls, user_id, home_id):
    collection = cls.get_collection_with_user_home(user_id=user_id, home_id=home_id)
    if not collection:
      collection = Collection(user_id=user_id, home_id=home_id)
    else:
      collection.is_active = True

    try:
      db.session.merge(collection)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return None
    return cls.get_collection_with_user_home(user_id=user_id, home_id=home_id)

  @classmethod
  def del_collection(cls, user_id, home_id):
    collection = cls.get_collection_with_user_home(user_id=user_id, home_id=home_id)
    if not collection:
      return False
    collection.is_active = False
    try:
      db.session.merge(collection)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return False
    return True

  @classmethod
  def get_collections_with_user(cls, user_id):
    return Collection.query.filter(and_(Collection.user_id==user_id, Collection.is_active==True)).all()

  @classmethod
  def get_city_count_with_date_and_city(cls, city_id, date=None):
    return CityCount.query.filter_by(city_id=city_id).order_by(CityCount.date.desc()).first()

  @classmethod
  def get_city_ranking_list_with_city(cls, city_id, date=None):
    return CityRankingList.query.filter_by(city_id=city_id).order_by(
        CityRankingList.date.desc()).limit(10).all()

  @classmethod
  def get_total_ranking_list_with_city(cls, date=None):
    return TotalRankingList.query.order_by(TotalRankingList.date.desc()).limit(10).all()

  @classmethod
  def get_super_ranking_list_with_city(cls):
    return SuperRankingList.query.filter_by(is_active=True).limit(10).all()

  @classmethod
  def get_carouse_figure(cls):
    return CarouselFigure.query.filter_by(is_active=True).all()

  @classmethod
  def v2_get_carouse_figure(cls):
    return CarouselFigure.query.filter_by(is_active=False).all()

  @classmethod
  def v3_get_carouse_figure(cls):
    return CarouselFigure.query.filter_by(is_active=True).all()

  @classmethod
  def pares_qiniu_pic(cls, key):
    if not key:
      return None
    q = Auth(app.config['QINIU_AK'], app.config['QINIU_SK'])
    return q.private_download_url(app.config['QINIU_DOMAIN']+key, app.config['QINIU_EXPIRES'])

  @classmethod
  def get_answer_url(cls):
    return Answer.query.filter_by(is_active=True).first()

  @classmethod
  def validate_query_frequency_grant(cls, user_id, date):
    user = cls.get_user_with_id(user_id=user_id)
    if not user:
      return False
    if user.phone:
      return True

    frequency = UserQueryFrequency.query.filter(and_(UserQueryFrequency.user_id==user_id,
      UserQueryFrequency.date==date)).first()

    if not frequency:
      frequency = UserQueryFrequency(user_id=user_id, frequency=1, date=date)
      db.session.add(frequency)
      db.session.commit()
      return True
    if frequency.frequency < app.config['USER_QUERY_COUNT']:
      frequency.frequency += 1
      db.session.merge(frequency)
      db.session.commit()
      return True
    return False

  @classmethod
  def get_home_collection_with_user_city(cls, user_id, city_id):
    return CityCollection.query.filter(and_(CityCollection.user_id==user_id, CityCollection.city_id==city_id)).first()

  @classmethod
  def set_city_collections(cls, user_id, city_ids):
    try:
      for city_id in city_ids:
        city_collection = cls.get_home_collection_with_user_city(user_id=user_id, city_id=city_id)
        if not city_collection:
          city_collection = CityCollection(user_id=user_id, city_id=city_id)
        else:
          city_collection.is_active = True
        db.session.merge(city_collection)
        db.session.commit()
    except (DataError, IntegrityError), e:
      db.session.rollback()
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return False
    return True

  @classmethod
  def del_city_collection(cls, user_id, city_id):
    city_collection = cls.get_home_collection_with_user_city(user_id=user_id, city_id=city_id)
    if not city_collection:
      return False
    city_collection.is_active = False
    try:
      db.session.merge(city_collection)
      db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return False
    return True

  @classmethod
  def get_read_condition_with_user(cls, user_id, city_id, rank_date):
    return ReadCondition.query.filter(and_(ReadCondition.user_id==user_id,
      ReadCondition.city_id==city_id, ReadCondition.rank_date==rank_date)).first()

  @classmethod
  def set_read_condition(cls, user_id, city_id, rank_date):
    rc = cls.get_read_condition_with_user(user_id=user_id, city_id=city_id, rank_date=rank_date)
    try:
      if not rc:
        rc = ReadCondition(user_id=user_id, city_id=city_id, rank_date=rank_date)
        db.session.add(rc)
        db.session.commit()
    except (DataError, IntegrityError), e:
      app.logger.error(sys._getframe().f_code.co_name + str(e))
      return None
    return rc

  @classmethod
  def get_city_collections(cls, user_id):
    return CityCollection.query.filter(and_(CityCollection.user_id==user_id, CityCollection.is_active==True)).all()

  @classmethod
  def get_collection_with_user_and_city(cls, user_id, city_id):
    return CityCollection.query.filter(and_(CityCollection.user_id==user_id,
      CityCollection.city_id==city_id, CityCollection.is_active==True)).first()

  @classmethod
  def get_today_new_home_with_user(cls, user_id):
    query = '''
      SELECT
        l.id
      FROM
        "public"."user" u
      INNER JOIN
        city_collection c
      ON
        u.id = c.user_id
      AND
        u.id = {user_id}
      AND
        c.is_active is true
      INNER JOIN
        city_ranking_list l
      ON
        c.city_id = l.city_id
      AND
        l.date = (SELECT MAX(date) AS date FROM city_ranking_list LIMIT 1)
    '''.format(user_id=user_id)
    result = db.session.execute(query)
    return result.fetchall()

  @classmethod
  def get_today_first_new_home(cls):
    query = '''
      SELECT 
        home_id, id
      FROM 
        city_ranking_list 
      WHERE 
        date = (SELECT max(date) FROM city_ranking_list LIMIT 1)
      ORDER BY score DESC LIMIT 1
    '''
    result = db.session.execute(query)
    home_id = result.first()
    if home_id:
      return cls.get_home_page_with_home_id(home_id=home_id[0]), result.rowcount, home_id[1]
    return None, 0, -1

  @classmethod
  def get_city_ranking_list_with_id(cls, id):
    return CityRankingList.query.filter_by(id=id).first()

  @classmethod
  def get_newest_all_city_ranking_list(cls):
    max_date = db.session.query(db.func.max(CityRankingList.date)).scalar()
    return CityRankingList.query.filter_by(date=max_date).order_by(CityRankingList.score.desc()).all()

  @classmethod
  def get_newest_follow_city_ranking_list(cls, ids):
    max_date = db.session.query(db.func.max(CityRankingList.date)).scalar()
    return CityRankingList.query.filter(CityRankingList.id.in_(ids)).order_by(CityRankingList.score.desc()).all()

  @classmethod
  def get_index_page_card_pic_url(cls):
    return Picture.query.filter(and_(Picture.type==0, Picture.is_active==True)).first()

  @classmethod
  def get_apartment_no_with_place_name(cls, place_name):
    md5 = hashlib.md5()
    md5.update(place_name.encode("utf-8"))
    return HomePage.query.filter(and_(HomePage.hash_code==md5.hexdigest(),
      HomePage.map_box_place_name==place_name, HomePage.apt_no.isnot(None))).order_by(HomePage.score.desc()).all()

  @classmethod
  def get_home_page_id_with_place_name(cls, place_name):
    # the method get home by silimar
    query = '''
      SELECT 
        id, map_box_place_name <-> '{place_name}' AS smar 
      FROM 
        home_page 
      ORDER BY smar LIMIT 1
    '''.format(place_name=place_name)
    result = db.session.execute(query)
    return result.fetchall()

  @classmethod
  def get_home_pages_with_query(cls,city_id,offset,limit,**kwargs):
    THREE_MONTH_AGO = datetime.datetime.today()-datetime.timedelta(days=90)
    betters_ids = CityRankingList.query.filter(and_(CityRankingList.city_id==city_id,CityRankingList.created_at>THREE_MONTH_AGO)).all()
    ids = [i.home_id for i in betters_ids]

    query = db.session.query(HomePage)
    query=query.filter(HomePage.id.in_(ids))

    offset = int(offset) if offset<20 else 20
    limit = int(limit) if limit<10 else 10

    filters_category = ['bedroom','bathroom','zipcode','city_id']
    filters_range = ['price_l','price_h','hq']   # hq= high quality
    sorts = ['sort_price','sort_list']

    #query = query.order_by(HomePage.map_box_place_name)
    query = query.filter(getattr(HomePage,'city_id')==city_id)
    # filters
    for attr,value in kwargs.iteritems():
      if attr in filters_category and attr!='zipcode':
        query = query.filter(getattr(HomePage,attr)==value)
      if attr in filters_category and attr == 'zipcode' and value:
        query = query.filter(HomePage.map_box_place_name.like('%{}, United States'.format(value)))
      if attr in filters_range and attr=='price_l' and value:
        query = query.filter(HomePage.house_price_dollar>=value)
      if attr in filters_range and attr=='price_h' and value:
        query = query.filter(HomePage.house_price_dollar<=value)
     #  # sort here
      if attr in sorts and attr=='sort_price':
        if int(value)==1:
          query = query.order_by(HomePage.house_price_dollar.asc())
        elif int(value)==-1:
          query = query.order_by(HomePage.house_price_dollar.desc())
      if attr in sorts and attr=='sort_list':
        if int(value)==1:
          query = query.order_by(HomePage.created_at.asc())
        elif int(value)==-1:
          query = query.order_by(HomePage.created_at.desc())

    record_query = query.paginate(offset,limit,False)
    total = record_query.total
    return record_query.items,total

  @classmethod
  def get_score_pct_position(cls,score,city_id):
    citypct = CityPct.query.filter_by(city_id=city_id).first()
    if citypct and citypct.city_id!=0:
      s = citypct.bin_pct.replace('(','[').replace(')',']')
      pct_positions = pd.DataFrame(json.loads(s))
      pct_positions.drop_duplicates(subset=0, keep='last',inplace=True)
      pct_positions.set_index(0,inplace=True)
      compare_index = pct_positions.index.get_loc(score,method='nearest')
      value = pct_positions.iloc[compare_index][1]
      return float(value)

  @classmethod
  def get_user_with_phone_and_country(cls, phone, country):
    user = User.query.filter_by(phone=phone, country_code=country).first()
    if user:
      return user
    else:
      return None

  @classmethod
  def get_app_rank_pic_with_type(cls, type):
    return Picture.query.filter(and_(Picture.type==type, Picture.is_active==True)).first()

  @classmethod
  def get_wechat_access_token_for_app(cls, code):
    querystring = {
      'appid': app.config['WECHAT_APP_ID_FOR_APP'],
      'secret': app.config['WECHAT_SECRET_FOR_APP'],
      'code': code,
      'grant_type': app.config['WECHAT_GRANT_TYPE_FOR_APP']
      }
    response = requests.request("GET", app.config['WEHCAT_GET_ACCESS_TOKEN_URL'], params=querystring)
    return json.loads(response.text)

  @classmethod
  def get_wechat_user_info_for_app(cls, access_token, openid):
    querystring = {
      'access_token': access_token,
      'openid': openid
      }
    response = requests.request("GET", app.config['WEHCAT_GET_USERINFO_URL'], params=querystring)
    return json.loads(response.text)

  @classmethod
  def get_user_with_openid(cls, openid):
    return User.query.filter_by(openid=openid).first()

  @classmethod
  def to_response(cls, data):
    return app.response_class(
        response=(dumps(data), '\n'),
        status=200,
        mimetype='application/json'
    )
