#!/usr/bin/python3
""" starts a Flask web app """

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """ returns page for home page """
    return "Hello HBNB!"
