#!/usr/bin/env python3
""" starts a Flask web app """

from web_flask import app


@app.route('/')
def hello_hbnb():
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
