import requests
from urllib import quote_plus
import json
from sqlalchemy import text
from index import db, app
from JobSchedule import JobSchedule
from multiprocessing import Queue
from Queue import Empty
import time

# def update_bar(pbar):
#   print
#   L.acquire()
#   pbar.update()
#   L.release()

def write_place_name_to_db(home_id, replace_name):
  with app.app_context():
    query = '''
      UPDATE home_page 
      SET map_box_place_name = '{replace_name}',
          hash_code = MD5('{replace_name}')
      WHERE
          id = {home_id}
    '''.format(home_id=home_id, replace_name=replace_name)
    try:
      db.session.execute(text(query))
      db.session.commit()
    except Exception as e:
      db.session.rollback()

def update_step(home_id, step):
  with app.app_context():
    query = '''
      UPDATE home_page 
      SET 
          step = {step}
      WHERE
          id = {home_id}
    '''.format(home_id=home_id, step=step)
    try:
      db.session.execute(text(query))
      db.session.commit()
    except Exception as e:
      db.session.rollback()

def sync_by_address(update_pbar, pid, queue):
  while not queue.empty():
    try:
      data = queue.get(False)
      home_id, address = data[0], data[1]
      releveance = 0.9
      url = "https://api.tiles.mapbox.com/geocoding/v5/mapbox.places/{address}.json".format(address=quote_plus(address))
      querystring = {"country":"us","limit":"1","access_token": app.config['MAP_BOX_ACCESSTOKEN']}
      headers = {
          'cache-control': "no-cache",
          }
      response = requests.request("GET", url, headers=headers, params=querystring)
      result = json.loads(response.text)
      
      if len(result['features'])>0 and result['features'][0]['relevance']>= releveance:
        write_place_name_to_db(home_id=home_id, replace_name=result['features'][0]['place_name']) 
      update_pbar('progress')
    except Empty:
      return
    except Exception as e:
      update_pbar('progress')
      time.sleep(10)
    update_step(home_id=home_id, step=1)

def sync_by_lang_lat(update_pbar, queue):
  while not queue.empty():
    try:
      data = queue.get(False)
      home_id, lang, lat = data[0], data[1], data[2]
      url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{lang},{lat}.json".format(lang=lang, lat=lat)
      querystring = {"country":"us","limit":"1","access_token": app.config['MAP_BOX_ACCESSTOKEN_LIST'][pid]}
      headers = {
          'cache-control': "no-cache",
          }
      response = requests.request("GET", url, headers=headers, params=querystring)
      result = json.loads(response.text)
      if len(result['features'])>0:
        write_place_name_to_db(home_id=home_id, replace_name=result['features'][0]['place_name']) 
      update_pbar('progress')
    except Empty:
      return

def sync_place_data():
  place_q = Queue()
  query = '''
    SELECT id, address 
    FROM  
        home_page
    WHERE
       address is not null
    AND
       map_box_place_name is null
    AND
      step is null
    LIMIT 10000
  '''
  datas = db.session.execute(text(query))
  for item in datas:
    place_q.put(item)

  print'step one back-fill with place name start {count} rows'.format(count=datas.rowcount)
  jc = JobSchedule(function=sync_by_address, queue=place_q,
    prcesscount=app.config['PROCESS_COUNT'], thread_count=app.config['THREAD_COUNT'], max_size=datas.rowcount)
  jc.start()

  # lang_lat_q = Queue()
  # query = '''
  #   SELECT id, longitude, latitude
  #   FROM  
  #       home_page
  #   WHERE
  #      map_box_place_name is null
  #   AND
  #      longitude is not null
  #   AND
  #      latitude is not null
  # '''
  # 
  # datas = db.session.execute(text(query))
  # for item in datas:
  #   lang_lat_q.put(item)

  # print 'step two back-fill with lang and lat start {count} rows'.format(count=datas.rowcount)
  # jc = JobSchedule(function=sync_by_lang_lat, queue=lang_lat_q,
  #   prcesscount=4, thread_count=50, max_size=datas.rowcount)
  # jc.start()
