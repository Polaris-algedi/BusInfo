#!/usr/bin/python3
""" bus stops module """

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.route import Route
from models.stop import BusStop




@app_views.route('/stops', methods=['GET'], strict_slashes=False)
@app_views.route('/stops/<stop_id>', methods=['GET'], strict_slashes=False)
def get_stop(stop_id=None):
    """ Retrieves a Stop object or the list of all Stop objects """
    if stop_id:
        stop = storage.get(BusStop, stop_id)
        if stop is None:
            abort(404)
        return jsonify(stop.to_dict())
    else:
        stops = storage.all(BusStop).values()
        list_stops = []
        for stop in stops:
            list_stops.append(stop.to_dict())

        return jsonify(list_stops)



@app_views.route('/routes/<route_id>/stops', methods=['GET'], strict_slashes=False)
def get_route_stops(route_id):
    """ Retrieves a Route object or the list of all Route objects """
    route = storage.get(Route, route_id)
    if route is None:
        abort(404)
    stops = route.stops
    list_stops = []
    for stop in stops:    
        list_stops.append(stop.to_dict())

    return jsonify(list_stops)