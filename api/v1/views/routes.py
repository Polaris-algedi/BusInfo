#!/usr/bin/python3
""" routes module """

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.schedule import Schedule
from models.route import Route



@app_views.route('/routes', methods=['GET'], strict_slashes=False)
@app_views.route('/routes/<route_id>', methods=['GET'], strict_slashes=False)
def get_route(route_id=None):
    """ Retrieves a Route object or the list of all Route objects """
    if route_id:
        route = storage.get(Route, route_id)
        if route is None:
            abort(404)
        return jsonify(route.to_dict())
    else:
        routes = storage.all(Route).values()
        list_routes = []
        for route in routes:
            list_routes.append(route.to_dict())

        return jsonify(list_routes)


@app_views.route('schedule/<schedule_id>/routes', methods=['GET'], strict_slashes=False)
def get_schedule_routes(schedule_id):
    """ Retrieves a Route object or the list of all Route objects """
    schedule = storage.get(Schedule, schedule_id)
    if schedule is None:
        abort(404)
    routes = schedule.routes
    list_routes = []
    for route in routes:    
        list_routes.append(route.to_dict())

    return jsonify(list_routes)



