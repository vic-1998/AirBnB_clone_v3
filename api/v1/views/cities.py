#!/usr/bin/python3

from flask import Flask
from flask.json import jsonify, request
from flask.wrappers import Request
from werkzeug.exceptions import abort
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET', 'POST'])
def states(state_id):
    """ 
    route cities by states id
    made get and post petition

    Args:
        state_id ([integer]): [id state in DB]
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')
    
    if request.method == 'POST':
        res_json = request.get_json()
        if res_json is None:
            abort(400, 'Not a JSON')
        if res_json.get('name') is None:
            abort(400, 'Missing name')
        
        

@app_views.route('/api/v1/cities/<city_id>/cities', methods=['GET', 'DELETE'])
def cities(city_id):
    """
    route cities, search cities by id cities
    made get and post petitions
    Args:
        city_id ([integer]): [id city in DB]
    """
    city_obj = storage.get('City',city_id)
    if city_obj is None:
        abort(404, 'Not found')
        
    if request.method == 'GET':
        return jsonify(city_obj.to_json())
    
    if request.method == 'DELETE':
        city_obj.delete()
        del city_obj
        return jsonify({}), 200