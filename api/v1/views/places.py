#!/usr/bin/python3
"""
Places Viewer

"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def getPlaces(city_id=None):
    """get all places
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def getPlaceId(place_id=None):
    """get a place by id

    Args:
        place_id ([string]): [place id information]
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delPlace(place_id=None):
    """[delete a place]

    Args:
        place_id ([string]): [identifier of place]
    """
    json_places = storage.get(Place, place_id)
    if json_places is None:
        abort(404)
    else:
        json_places.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def postPlace(city_id=None):
    """ Create a new places by city id
    """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    if 'user_id' not in place.keys():
        abort(400, {'Missing user_id'})
    userid = storage.get(User, place['user_id'])
    if not userid:
        abort(404)
    if 'name' not in place:
        abort(400, {'Missing name'})
    new_place = Place(**place)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def putPlace(place_id=None):
    """update a place by id

    Args:
        place_id ([strings]): [identifier of place]
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id',
                        'created_at', 'updated_at']:
            setattr(place, attr, val)
    storage.save()
    return jsonify(place.to_dict()), 200
