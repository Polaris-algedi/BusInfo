#!/usr/bin/python3
"""
This module initializes a Blueprint instance.
"""

from flask import Blueprint

# Create a Blueprint instance
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all views from the index module
from api.v1.views.index import *
from api.v1.views.schedules import *
from api.v1.views.routes import *
from api.v1.views.bus_stops import *
"""from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *"""