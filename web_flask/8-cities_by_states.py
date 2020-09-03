#!/usr/bin/python3
""" something """

from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def remove_session(dummy):
    """ removes session """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """ returns /cities_by_states page """
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
