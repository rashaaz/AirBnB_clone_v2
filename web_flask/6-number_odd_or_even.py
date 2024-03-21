#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Starts a Flask web application
"""
from flask import Flask
from flask import render_template
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


@app.route('/python', strict_slashes=False)
@app.route('/python/<string:text>', strict_slashes=False)
def python_text(text='is cool'):
    """Defines a route with a dynamic message starting with 'Python'"""
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def only_digits_dynamic(n=None):
    """Defines a route with a dynamic message for integers"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def first_template(n=None):
    """Defines a route to render an HTML template for integers"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def conditional_templating(n=None):
    """Defines a route to render an HTML template for odd or even numbers"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
