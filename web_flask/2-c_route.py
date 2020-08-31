#!/usr/bin/python3
""" starts a Flask web app """

from web_flask import app


@app.route('/', strict_slashes=False)
def home():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<string:text>')
def c(text):
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )