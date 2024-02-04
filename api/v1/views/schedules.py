#!/usr/bin/python3
""" schedule module """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.schedule import Schedule


def jsonify_schedule(schedule):
    """ Prepare a Schedule object for jsonify """
    instance_as_dict = schedule.to_dict()
    instance_as_dict['first_departure'] = str(schedule.first_departure)
    instance_as_dict['last_departure'] = str(schedule.last_departure)
    instance_as_dict['duration'] = str(schedule.duration)
    instance_as_dict['bus_frequency'] = str(schedule.bus_frequency)
    return instance_as_dict

@app_views.route('/schedules', methods=['GET'], strict_slashes=False)
@app_views.route('/schedules/<schedule_id>', methods=['GET'], strict_slashes=False)
def get_schedule(schedule_id=None):
    """ Retrieves a Schedule object or the list of all Schedule objects """
    if schedule_id:
        schedule = storage.get(Schedule, schedule_id)
        if schedule is None:
            abort(404)
            
        return jsonify(jsonify_schedule(schedule))
    else:
        schedules = storage.all(Schedule).values()
        list_schedules = []
        for schedule in schedules:
            list_schedules.append(jsonify_schedule(schedule))

        return jsonify(list_schedules)

@app_views.route('/schedules/<schedule_id>', methods=['DELETE'], strict_slashes=False)
def delete_schedule(schedule_id):
    """ Deletes a Schedule object """
    schedule = storage.get(Schedule, schedule_id)
    if schedule is None:
        abort(404)
    storage.delete(schedule)
    storage.save()
    return jsonify({}), 200

#@app_views.route('/schedules', methods=['POST'], strict_slashes=False)
#def post_schedule():
    """ Creates a Schedule """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'bus_id' not in request.get_json():
        abort(400, description="Missing bus_id")
    if 'route_id' not in request.get_json():
        abort(400, description="Missing route_id")
    if 'stop_id' not in request.get_json():
        abort(400, description="Missing stop_id")
    data = request.get_json()
    schedule = Schedule(**data)
    schedule.save()
    return jsonify(schedule.to_dict()), 201

#@app_views.route('/schedules/<schedule_id>', methods=['PUT'], strict_slashes=False)
#def put_schedule(schedule_id):
    """ Updates a Schedule object """
    schedule = storage.get(Schedule, schedule_id)
    if schedule is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(schedule, key, value)
    schedule.save()
    return jsonify(schedule.to_dict()), 200
