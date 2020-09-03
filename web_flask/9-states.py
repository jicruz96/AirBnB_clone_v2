#!/usr/bin/python3
""" something """

from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def remove_session(dummy):
    """ removes session """
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def hi_states(id=None):
    """ returns states/<id> page """
    states = storage.all("State")
    if id is not None:
        id = 'State.{}'.format(id)
    return render_template('9-states.html', states=states, id=id)


if __name__ == "__main__":

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
