#!/usr/bin/python3
""" App is a Flask instance

    Returns:
        if not response
        [error]: [ Not found]
"""

import os
from models import storage
from flask_cors import CORS
from flask import Flask, jsonify
from api.v1.views import app_views
from flask.helpers import flash, make_response

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(exception):
    """[call class storage from models]

    Args:
        exception ([error]): [call storage class]
    """
    storage.close()


@app.errorhandler(404)
def handler_error(error):
    """ if not found return a Json string with error

    Args:
        error ([error]): [log error]

    Returns:
        [json]: [error message]
    """
    return {"error": "Not found"}, 404


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
