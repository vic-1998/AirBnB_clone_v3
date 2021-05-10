#!/usr/bin/python3
"""Create a new view for Amenity"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAmenity():
    """Get a Amenity"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenityId(amenity_id):
    """delete a new amenities"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delAmenity(amenity_id):
    """deletes a Amenity"""
    empty_dict = {}

    try:
        json_ameni = storage.get(Amenity, amenity_id)
        json_ameni.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def postAmenity():
    """create a new amenities"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenities = Amenity(**request.get_json())
    amenities.save()
    return make_response(jsonify(amenities.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def putAmenity(amenity_id):
    """update a amenities"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenities, attr, val)
    amenities.save()
    return jsonify(amenities.to_dict())
