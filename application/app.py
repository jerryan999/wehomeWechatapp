# -*- coding: utf-8 -*-
from .models import City
from index import app, db
from .utils.helper import uuid_gen, json_validate, requires_auth
from .utils.query import QueryHelper
from flask import request, jsonify
import json

logger = app.logger

@app.route('/api/index_page', methods=['POST'])
@uuid_gen
@json_validate(filter=['token'])
@requires_auth
def index_page():
  columns = ['rental_radio', 'house_price_trend', 'increase_radio', 'rental_income_radio']
  d = {}
  try:
    index_page = QueryHelper.get_index_page()
    index_page.rental_radio = json.loads(index_page.rental_radio) if index_page.rental_radio else None
    index_page.house_price_trend = json.loads(index_page.house_price_trend) if index_page.house_price_trend else None
    index_page.increase_radio = json.loads(index_page.increase_radio) if index_page.increase_radio else None
    index_page.rental_income_radio = json.loads(index_page.rental_income_radio) if index_page.rental_income_radio else None
    d['index_page'] = index_page
  except Exception as e:
    logger.error("Failed to get index page list {}".format(e))
    return jsonify(success=False,
      message='Failed to get index page list')
  return QueryHelper.to_json_with_filter(rows_dict=d, columns=columns)

@app.route('/api/get_cities', methods=['POST'])
@uuid_gen
@json_validate(filter=['token'])
@requires_auth
def get_cities():
  columns = ['id', 'city_name']
  d = {}
  try:
    index_page = QueryHelper.get_cities()
    d['city'] = index_page
  except Exception as e:
    logger.error("Failed to get city list {}".format(e))
    return jsonify(success=False,
      message='Failed to get city list')
  return QueryHelper.to_json_with_filter(rows_dict=d, columns=columns)

@app.route('/api/city_page', methods=['POST'])
@uuid_gen
@json_validate(filter=['city_id', 'token'])
@requires_auth
def city_page():
  columns = ['sale_online_offline', 'rent_online_offline', 'house_sale_number', 'house_rent_number',
    'block_villa_max', 'block_villa_min', 'block_apartment_max', 'block_apartment_min', 'one_room_one_toilet',
    'two_room_two_toilet', 'three_room_two_toilet', 'rental_radio', 'house_price_trend', 'increase_radio',
    'rental_income_radio', 'list_average_price', 'deal_average_price', 'city_name']
  d = {}
  try:
    incoming = request.get_json()
    city_page = QueryHelper.get_city_page_with_city_id(city_id=incoming['city_id'])
    d['city_name'] = city_page.city.city_name
    city_page.rent_online_offline = json.loads(city_page.rent_online_offline) if city_page.rent_online_offline else None
    city_page.sale_online_offline = json.loads(city_page.sale_online_offline) if city_page.sale_online_offline else None
    city_page.house_price_trend = json.loads(city_page.house_price_trend) if city_page.house_price_trend else None
    city_page.one_room_one_toilet = json.loads(city_page.one_room_one_toilet) if city_page.one_room_one_toilet else None
    city_page.two_room_two_toilet = json.loads(city_page.two_room_two_toilet) if city_page.two_room_two_toilet else None
    city_page.three_room_two_toilet = json.loads(city_page.three_room_two_toilet) if city_page.three_room_two_toilet else None
    d['city_page'] = city_page
  except Exception as e:
    print e
    logger.error("Failed to get city page list {}".format(e))
    return jsonify(success=False,
      message='Failed to get city page list')
  return QueryHelper.to_json_with_filter(rows_dict=d, columns=columns)

@app.route('/api/home_page', methods=['POST'])
@uuid_gen
@json_validate(filter=['place_name', 'token'])
@requires_auth
def home_page():
  columns = ['map_box_place_name', 'score', 'house_price_dollar', 'house_price_dollar', 'exchange_rate',
    'rent', 'size', 'bedroom', 'bathroom', 'rental_radio', 'increase_radio', 'rental_income_radio', 'furture_increase_radio',
    'house_price_trend', 'neighborhood_rent_radio', 'city_name']
  d = {}
  try:
    incoming = request.get_json()
    home_page = QueryHelper.get_home_page_with_place_name(place_name=incoming['place_name'])
    d['neighborhood_trend'] = json.loads(home_page.neighborhood.house_price_trend) if home_page.neighborhood.house_price_trend else None
    d['neighborhood_rent_radio']= home_page.neighborhood.neighbor_rental_radio
    d['city_trend'] = json.loads(home_page.neighborhood.city.citypage.house_price_trend) if home_page.city and home_page.city.citypage.house_price_trend else None
    d['city_name'] = home_page.city.city_name if home_page.city else None
    d['exchange_rate'] = QueryHelper.get_index_page().exchange_rate
    home_page.house_price_trend = json.loads(home_page.house_price_trend) if home_page.house_price_trend else None
    d['home_page'] = home_page
  except Exception as e:
    logger.error("Failed to get home page list {}".format(e))
    return jsonify(success=False,
      message='Failed to get home page list')
  return QueryHelper.to_json_with_filter(rows_dict=d, columns=columns)

@app.route('/ping', methods=['GET'])
def ping():
  return 'pong'