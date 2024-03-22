#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Starts a Flask web application
"""
from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def appcontext_teardown(self):
    """Defines a route to display a list of states
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def state_info():
    """Close the current SQLAlchemy Session"""
    return render_template('7-states_list.html',
                           states=storage.all(State))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
