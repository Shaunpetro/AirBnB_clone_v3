#!/usr/bin/python3
"""
Module for handling City objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves all City objects linked to a State by state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a specific City object by ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object linked to a State by state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, description="Not a JSON")
    if "name" not in city_json:
        abort(400, description="Missing name")
    
    city_json["state_id"] = state_id
    new_city = City(**city_json)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a specific City object by ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, description="Not a JSON")
    for key, value in city_json.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
