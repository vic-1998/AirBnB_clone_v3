#!/usr/bin/python3
"""Create a new view for places reviews.py"""

from models import storage
from models.user import User
from models.state import State
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def getReviews(place_id):
    """Get a Reviews"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    review = []
    for data in place.review:
        review.append(data.to_dict())
    return jsonify(review)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get review information for specified review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review based on its review_id"""
    """deletes a state"""
    empty_dict = {}

    try:
        json_review = storage.get("Review", review_id)
        json_review.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    if storage.get("Place", place_id) is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if storage.get("User", data["user_id"]) is None:
        abort(404)
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    new_review = Review(user_id=data["user_id"],
                        place_id=place_id,
                        text=data["text"])
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict())
