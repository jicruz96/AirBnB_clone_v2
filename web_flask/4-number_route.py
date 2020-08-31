#!/usr/bin/python3
""" starts a Flask web app """

from web_flask import app


@app.route('/', strict_slashes=False)
def home():
    """ returns page content for home page """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ returns page content for /hbnb page """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ returns page content for c page """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """ returns page content for python page """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ returns page content for number page if input is a number """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
