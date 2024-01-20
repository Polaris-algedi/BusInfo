#!/usr/bin/python3
"""
This is the main module of our Flask web application.
It defines the Flask application instance and routes.
"""

from flask import Flask, jsonify, make_response
from api.v1.views import app_views  # Importing Blueprint
# from flask_cors import CORS
from models import storage
import os

# Flask application instance
app = Flask(__name__)

# Register the Blueprint to the Flask application
app.register_blueprint(app_views)

# Create a CORS instance allowing: /* for 0.0.0.0
# cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """
    This function is called after each request.
    It ensures that SQLAlchemy session is removed after each request.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    This function is called when a 404 error occurs.
    It returns a JSON response with a 'Not found' message.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Run the Flask web server
    app.run(host=os.getenv('BUS_API_HOST', '0.0.0.0'),
            port=int(os.getenv('BUS_API_PORT', '5000')),
            threaded=True, debug=True)