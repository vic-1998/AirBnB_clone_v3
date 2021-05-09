#!/usr/bin/python3
"""
Places Viewer

"""

from flask.helpers import make_response
from models import storage
from models import Place
from api.v1.views import app_views
from flask import Flask, json, abort, request, jsonify


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def getPlaces():
    """get all places
    """
    places = []
    for place in storage.all('Place').values():
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def getPlaceId(place_id):
    """get a place by id

    Args:
        place_id ([string]): [place id information]
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delPlace(place_id):
    """[delete a place]

    Args:
        place_id ([string]): [identifier of place]
    """
    empty_dict = {}

    try:
        json_places = storage.get('Place', place_id)
        json_places.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def postPlace():
    """ Create a new places by city id
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place = Place(**request.get_json())
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def putPlace(place_id):
    """update a place by id

    Args:
        place_id ([string]): [identifier of place]
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id',
                        'created_at', 'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict()), 200
