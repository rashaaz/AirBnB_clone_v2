#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Starts a Flask web application
"""
from models import storage
from models.state import State
from models.amenity import Amenity
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def appcontext_teardown(self):
    """Displays the HBNB filters page
    """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def state_id():
    """Close the current SQLAlchemy Session"""
    return render_template('10-hbnb_filters.html',
                           states=storage.all(State),
                           amenities=storage.all(Amenity))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
