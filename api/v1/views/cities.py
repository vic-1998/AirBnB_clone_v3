#!/usr/bin/python3
"""[viewer cities by and cities by states_id]
"""

from flask import Flask
from flask.helpers import make_response
from flask.json import jsonify, request
from werkzeug.exceptions import abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def allCities():
    ''' search all cities'''
    cities = []
    for city in storage.all("City").values():
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def getCitiesByState(state_id):
    ''' search cities by id '''
    all_cities = storage.get("State", state_id)
    if all_cities is None:
        abort(404)
    data = []
    for city in all_cities.cities:
        data.append(city.to_dict())
    return jsonify(data)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def getCitiesId(city_id):
    """
    Get cities by city Id
    Args:
        city_id ([integer]): [id city in DB]
    """
    cityId = storage.get("City", city_id)
    if cityId is None:
        abort(404)
    return jsonify(cityId.to_dict())


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delcity(city_id):
    """deletes a city"""
    empty_dict = {}

    try:
        json_cities = storage.get("City", city_id)
        json_cities.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route('/states/<string:state_id>/cities/',
                 methods=['POST'], strict_slashes=False)
def postCity(state_id):
    """create a new city"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data = request.get_json()
    data['state_id'] = state_id
    new_City = City(**data)
    storage.save()
    return make_response(jsonify(new_City.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def putCity(city_id):
    """update a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
