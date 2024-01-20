#!/usr/bin/python3
"""
This module defines a route status for a Flask application using a Blueprint.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def api_status():
    """
    This function is linked to the '/status' route.
    It returns a JSON object with the status of the API.
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """Stats"""
    DB_CLASSES = {
    'User': "User",
    'Route': "Route",
    'Feedback': "Feedback",
    'Bus': "Bus",
    'Schedule': "Schedule",
    'BusStop': "BusStop"
}
    stats = {}
    for key, value in DB_CLASSES.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
