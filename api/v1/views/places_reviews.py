#!/usr/bin/python3
"""Create a new view for places reviews.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReviews(place_id):
    """Get a Reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for data in place.reviews:
        reviews.append(data.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getReviewId(review_id):
    """get a reviews"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReviewId(review_id):
    """deletes a state"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    data = request.get_json()
    if data is None:
        return "Not a JSON", 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if data.get('user_id') is None:
        return "Missing user_id", 400
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if data.get('text') is None:
        return "Missing text", 400
    else:
        review = Review(**data)
        review.place_id = place_id
        review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    if request.get_json() is None:
        return "Not a JSON", 400
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    tables = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for attr, val in request.get_json().items():
        if attr not in tables:
            setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict()), 200
