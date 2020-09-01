#!/usr/bin/python3
""" starts a Flask web app """

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """ returns page for home page """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ returns page for /hbnb page """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ returns page for c page """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """ returns page for python page """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ returns page for number page if input is a number """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ returns page for number_template page if input is a number """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_bro(n):
    """ returns page for number_odd_or_even page if input is a number """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
