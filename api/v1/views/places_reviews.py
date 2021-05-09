#!/usr/bin/python3
"""Create a new view for places reviews.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReviews(place_id=None):
    """Get a Reviews"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for data in place.reviews:
        reviews.append(data.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def getReviewId(review_id=None):
    """get a reviews"""
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReviewId(review_id=None):
    """deletes a state"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def postReviewId(place_id=None):
    """create a new review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    places = request.get_json()
    if 'user_id' not in places:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", places['user_id'])
    if user is None:
        abort(404)
    if 'text' not in places:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    places['place_id'] = place_id
    review = Review(**places)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def putReviewId(review_id=None):
    """update a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    tables = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for attr, val in request.get_json().items():
        if attr not in tables:
            setattr(review, attr, val)
    storage.save()
    return jsonify(review.to_dict()), 200
