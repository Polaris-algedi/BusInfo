#!/usr/bin/python3
"""
This is the main module of our Flask web application.
It defines the Flask application instance and routes.
"""

from flask import Flask, jsonify, make_response, render_template
# from flask_cors import CORS
from models import storage
import os

# Flask application instance
app = Flask(__name__)


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

@app.route('/login', strict_slashes=False)
def login():
    return render_template('login.html')

@app.route('/fares-by-bus-lines', strict_slashes=False)
def get_fares_by_bus_lines():
    return render_template('fares_by_bus_lines.html')

@app.route('/home', strict_slashes=False)
def home():
    return render_template('busEAT.html')

@app.route('/', strict_slashes=False)
def about():
    return render_template('about.html')


if __name__ == "__main__":
    # Run the Flask web server
    app.run(host=os.getenv('BUS_API_HOST', '0.0.0.0'),
            port=int(os.getenv('BUS_API_PORT', '5001')),
            threaded=True, debug=True)