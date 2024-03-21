#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Starts a Flask web application
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Defines a route with a basic message"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Defines a route with another message"""
    return 'HBNB'


@app.route('/c/<string:text>', strict_slashes=False)
def c_text(text=None):
    """Defines a route with a dynamic message starting with 'C'"""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<string:text>', strict_slashes=False)
def python_text(text='is_cool'):
    """Defines a route with a dynamic message starting with 'Python'"""
    return "Python {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
