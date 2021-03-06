from index import db, bcrypt
# from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
import datetime

class City(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  city_name = db.Column(db.String(255), index=True)
  eng_name = db.Column(db.String(255), index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  # neighborhoods = relationship("Neighborhood", back_populates="city")
  homepages = relationship("HomePage", back_populates="city")
  citypage = relationship("CityPage", back_populates="city", uselist=False)
  city_ranking_list = relationship("CityRankingList", back_populates="city")
  city_collections = relationship("CityCollection", back_populates="city")

class Neighborhood(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  neighbor_name = db.Column(db.Text())
  neighbor_rental_radio = db.Column(db.Float())
  house_price_trend = db.Column(db.Text())
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  homepages = relationship("HomePage", back_populates="neighborhood")

class IndexPage(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  rental_radio = db.Column(db.Text())
  house_price_trend = db.Column(db.Text())
  increase_radio = db.Column(db.Text())
  exchange_rate = db.Column(db.Float())
  rental_income_radio = db.Column(db.Text())
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

class CityPage(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  city_id = db.Column(db.Integer(), db.ForeignKey("city.id", ondelete="CASCADE"), index=True, nullable=False, unique=True)
  sale_online_offline = db.Column(db.Text())
  rent_online_offline = db.Column(db.Text())
  house_sale_number = db.Column(db.Integer())
  house_rent_number = db.Column(db.Integer())
  block_villa_max = db.Column(db.Float())
  block_villa_median = db.Column(db.Float())
  block_villa_min = db.Column(db.Float())
  list_average_price = db.Column(db.Float())
  deal_average_price = db.Column(db.Float())
  block_apartment_max = db.Column(db.Float())
  block_apartment_median = db.Column(db.Float())
  block_apartment_min = db.Column(db.Float())
  one_room_one_toilet = db.Column(db.Text())
  two_room_two_toilet = db.Column(db.Text())
  three_room_two_toilet = db.Column(db.Text())
  rental_radio = db.Column(db.Float())
  house_price_trend = db.Column(db.Text())
  increase_radio = db.Column(db.Float())
  rental_income_radio = db.Column(db.Float())
  one_bed_one_bath_lower_bound = db.Column(db.Integer())
  one_bed_one_bath_upper_bound = db.Column(db.Integer())
  two_bed_two_bath_lower_bound = db.Column(db.Integer())
  two_bed_two_bath_upper_bound = db.Column(db.Integer())
  three_bed_two_bath_lower_bound = db.Column(db.Integer())
  three_bed_two_bath_upper_bound = db.Column(db.Integer())
  pic_url = db.Column(db.String(1024))
  app_pic_url = db.Column(db.String(1024))
  button_pic_url = db.Column(db.String(1024))
  button_dark_pic_url = db.Column(db.String(1024))
  long_b1 = db.Column(db.Float())
  long_b2 = db.Column(db.Float())
  long_b3 = db.Column(db.Float())
  airbnb_b1 = db.Column(db.Float())
  airbnb_b2 = db.Column(db.Float())
  airbnb_b3 = db.Column(db.Float())
  count_long = db.Column(db.Float())
  count_airbnb = db.Column(db.Float())
  occ_rate_long = db.Column(db.Float())
  occ_rate_airbnb = db.Column(db.Float())
  avg_long = db.Column(db.Float())
  avg_airbnb = db.Column(db.Float())
  return_long = db.Column(db.Float())
  return_airbnb = db.Column(db.Float())
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  city = relationship("City", back_populates="citypage")

class HomePage(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  neighbor_id = db.Column(db.Integer(), db.ForeignKey("neighborhood.id", ondelete="CASCADE"), index=True, nullable=False)
  city_id = db.Column(db.Integer(), db.ForeignKey("city.id", ondelete="CASCADE"), index=True)
  source_id = db.Column(db.String(255), unique=True)
  source = db.Column(db.String(255), index=True)
  map_box_place_name = db.Column(db.Text())
  address = db.Column(db.Text(), index=True)
  score = db.Column(db.Float())
  house_price_dollar = db.Column(db.Float())
  rent = db.Column(db.Float())
  size = db.Column(db.Integer())
  bedroom = db.Column(db.Integer())
  bathroom = db.Column(db.Float())
  rental_radio = db.Column(db.Float(), index=True)
  increase_radio = db.Column(db.Float())
  rental_income_radio = db.Column(db.Float())
  longitude = db.Column(db.Float())
  latitude = db.Column(db.Float())
  # md5 hash code for map_box_place_name
  hash_code = db.Column(db.CHAR(32), index=True)
  # which step back fill in
  step = db.Column(db.Integer(), default=0, index=True)
  adjust_score = db.Column(db.Float(), index=True)
  property_score = db.Column(db.Float(), index=True)
  neighborhood_score = db.Column(db.Float(), index=True)
  pic_url = db.Column(db.String(2048))
  apt_no = db.Column(db.String(32), index=True)
  apt_step = db.Column(db.Integer(), default=None, index=True)
  airbnb_rent = db.Column(db.Float())
  tax = db.Column(db.Float())
  insurance = db.Column(db.Float())
  pm_long = db.Column(db.Float())
  pm_short = db.Column(db.Float())
  price_history = db.Column(db.Text())
  nearby_school = db.Column(db.Text())
  description = db.Column(db.Text())
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  neighborhood = relationship("Neighborhood", back_populates="homepages")
  city = relationship("City", back_populates="homepages")
  collections = relationship("Collection", back_populates="homepage")
  city_ranking_list = relationship("CityRankingList", back_populates="home")
  total_ranking_list = relationship("TotalRankingList", back_populates="home")
  super_ranking_list = relationship("SuperRankingList", back_populates="home")

  __table_args__ = (
    db.Index("idx_longitude_latitude", "longitude", "latitude"),
    db.Index("idx_home_page_source_id", 'source_id'),
    db.Index("idx_home_page_created_at", 'created_at'),
    db.Index("idx_home_page_updated_at", 'updated_at'),
  )

class UnmatchedPlace(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  place_name = db.Column(db.Text(), index=True)
  # one of ['map_box_place_name', 'score', 'house_price_dollar', 'exchange_rate',
  #  'rent', 'rental_radio', 'increase_radio', 'rental_income_radio',
  #  'neighborhood_rent_radio', 'city_name', 'city_trend', 'neighborhood_trend']
  type = db.Column(db.String(64), index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __init__(self, place_name, type):
    self.place_name = place_name
    self.type = type

  __table_args__ = (
    db.Index("idx_place_name_type", "place_name", "type"),
  )

class FeedBack(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"), index=True)
  content = db.Column(db.Text(), index=True, nullable=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __init__(self, content, user_id):
    self.content = content
    self.user_id = user_id

class User(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  phone = db.Column(db.String(255), index=True)
  openid = db.Column(db.String(64), index=True, unique=True)
  nick_name= db.Column(db.String(255))
  gender = db.Column(db.Integer)
  language = db.Column(db.String(255), index=True)
  city = db.Column(db.String(255), index=True)
  province = db.Column(db.String(255), index=True)
  country = db.Column(db.String(255), index=True)
  country_code = db.Column(db.String(16), index=True)
  avatar_url = db.Column(db.String(1024))
  # 0 or null => mini program
  # 1 => app
  type = db.Column(db.Integer(), index=True)
  # mini program is null
  password = db.Column(db.String(255), index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __init__(self, openid, nick_name, gender, language, city, province, country, avatar_url, phone=None, type=0, password=None, country_code=None):
    self.openid = openid
    self.nick_name = nick_name
    self.gender = gender
    self.language = language
    self.city = city
    self.province = province
    self.country = country
    self.avatar_url = avatar_url
    self.phone = phone
    self.type = type
    self.country_code = country_code
    self.password = User.hashed_password(password) if password else password

  @staticmethod
  def hashed_password(password):
    return bcrypt.generate_password_hash(password)

  __table_args__ = (
    db.Index("idx_user_phone_country", "phone", "country"),
    db.UniqueConstraint("phone", name='unique_user_phone'),
  )

class Phone(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  phone = db.Column(db.String(255))
  country = db.Column(db.String(255))
  verification_code = db.Column(db.String(255))
  verification_code_created_at = db.Column(db.DateTime())
  is_verified = db.Column(db.Boolean(), index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  __table_args__ = (
    db.Index("idx_phone", "phone"),
    db.Index("idx_phone_country", "phone", "country"),
    db.UniqueConstraint("phone", "country", name='unique_phone_contry'),
  )

  def __init__(self, phone, country, verification_code, verification_code_created_at, is_verified=False):
    self.phone = phone
    self.country = country
    self.verification_code = verification_code
    self.verification_code_created_at = verification_code_created_at
    self.is_verified = is_verified

class Collection(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
  home_id = db.Column(db.Integer(), db.ForeignKey("home_page.id", ondelete="CASCADE"), index=True, nullable=False)
  is_active = db.Column(db.Boolean(), default=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  homepage = relationship("HomePage", back_populates="collections")

  def __init__(self, user_id, home_id, is_active=True):
    self.user_id = user_id
    self.home_id = home_id
    self.is_active = is_active

  __table_args__ = (
    db.Index("idx_user_id_home_id", "user_id", "home_id"),
  )

class CityCount(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  city_id = db.Column(db.Integer(), db.ForeignKey("city.id", ondelete="CASCADE"), index=True, nullable=False)
  diamond_room_num = db.Column(db.Integer())
  gold_room_num = db.Column(db.Integer())
  sliver_room_num = db.Column(db.Integer())
  bronze_room_num = db.Column(db.Integer())
  today_sale_online = db.Column(db.Integer())
  today_sale_offline = db.Column(db.Integer())
  today_rent_online = db.Column(db.Integer())
  today_rent_offline = db.Column(db.Integer())
  date = db.Column(db.Date(), nullable=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  __table_args__ = (
    db.Index("idx_city_id_date", "city_id", "date"),
  )

class CityRankingList(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  city_id = db.Column(db.Integer(), db.ForeignKey("city.id", ondelete="CASCADE"), index=True, nullable=False)
  home_id = db.Column(db.Integer(), db.ForeignKey("home_page.id", ondelete="CASCADE"), index=True, nullable=False)
  date = db.Column(db.Date(), nullable=False, index=True)
  score = db.Column(db.Float(), index=True)
  pic_url = db.Column(db.String(1024))
  is_active = db.Column(db.Boolean(), default=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  home = relationship("HomePage", back_populates='city_ranking_list', uselist=False)
  city = relationship("City", back_populates="city_ranking_list")

  __table_args__ = (
    db.Index("idx_city_id_date_city_rank", "city_id", "date"),
    db.Index("idx_city_id_is_active", "city_id", "is_active"),
    db.UniqueConstraint('home_id', 'date', name='unique_city_home_id_date'),
  )

class TotalRankingList(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  home_id = db.Column(db.Integer(), db.ForeignKey("home_page.id", ondelete="CASCADE"), index=True, nullable=False)
  date = db.Column(db.Date(), nullable=False, index=True)
  score = db.Column(db.Float(), index=True)
  pic_url = db.Column(db.String(1024))
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  home = relationship("HomePage", back_populates='total_ranking_list', uselist=False)

  __table_args__ = (
    db.UniqueConstraint('home_id', 'date', name='unique_home_id_date'),
  )

class SuperRankingList(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  home_id = db.Column(db.Integer(), db.ForeignKey("home_page.id", ondelete="CASCADE"), index=True, nullable=False)
  history_date = db.Column(db.Date(), nullable=False, index=True)
  recent_date = db.Column(db.Date(), nullable=False, index=True)
  history_price = db.Column(db.Integer, nullable=False)
  rencent_price = db.Column(db.Integer, nullable=False)
  pic_url = db.Column(db.String(1024))
  is_active = db.Column(db.Boolean(), default=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  home = relationship("HomePage", back_populates='super_ranking_list', uselist=False)

class CarouselFigure(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  index = db.Column(db.Integer(), index=True)
  pic_url = db.Column(db.String(1024))
  is_active = db.Column(db.Boolean(), default=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  external_link = db.Column(db.String(1024))

class Answer(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  pic_url = db.Column(db.String(1024))
  is_active = db.Column(db.Boolean(), default=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

class UserQueryFrequency(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"), index=True)
  frequency = db.Column(db.Integer(), index=True)
  date = db.Column(db.Date(), nullable=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __init__(self, user_id, frequency, date):
    self.user_id = user_id
    self.frequency = frequency
    self.date = date

  __table_args__ = (
    db.Index("idx_user_id_date", "user_id", "date"),
  )

class CityCollection(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
  city_id = db.Column(db.Integer(), db.ForeignKey("city.id", ondelete="CASCADE"), index=True, nullable=False)
  is_active = db.Column(db.Boolean(), default=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
  city = relationship("City", back_populates="city_collections")

  def __init__(self, user_id, city_id, is_active=True):
    self.user_id = user_id
    self.city_id = city_id
    self.is_active = is_active

  __table_args__ = (
    db.Index("idx_citycollection_user_id_city_id_is_active", "user_id", "city_id", 'is_active'),
    db.Index("idx_citycollection_user_id_is_active", "user_id", 'is_active'),
  )

class ReadCondition(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
  city_id = db.Column(db.Integer(), db.ForeignKey("city.id", ondelete="CASCADE"), index=True, nullable=False)
  rank_date = db.Column(db.Date(), nullable=False, index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __init__(self, user_id, city_id, rank_date):
    self.user_id = user_id
    self.city_id = city_id
    self.rank_date = rank_date

  __table_args__ = (
    db.Index("idx_readcondition_user_id_city_id_date", "user_id", "city_id", 'rank_date'),
  )

class Picture(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  pic_url = db.Column(db.String(1024))
  is_active = db.Column(db.Boolean(), default=False, index=True)
  # 0 => index page card pic
  # 1 => app total rank cover pic
  # 2 => app super rank cover pic
  type = db.Column(db.Integer(), index=True)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
  updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

  __table_args__ = (
    db.Index("idx_picture_type_is_active", "type", 'is_active'),
  )

class CityPct(db.Model):
  id = db.Column(db.Integer(), index=True, primary_key=True)
  city_id = db.Column(db.Integer())
  bin_pct = db.Column(db.Text())
