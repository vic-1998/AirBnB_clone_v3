#!/usr/bin/python3
"""Create a new view for places reviews.py"""

from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def getReviews(place_id):
    """Get a Reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place = place.reviews
    list_reviews = []
    for review in place:
        list_reviews.append(review.to_dict())
    return(jsonify(list_reviews), 200)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get a reviews"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return(jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a state"""
    empty_dict = {}

    try:
        json_review = storage.get(Review, review_id)
        json_review.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    if storage.get(Place, place_id) is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return(make_response('Not a JSON', 400))
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return(make_response(jsonify(review.to_dict()), 201))


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return(make_response('Not a JSON', 400))
    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return(make_response(jsonify(review.to_dict()), 200))
