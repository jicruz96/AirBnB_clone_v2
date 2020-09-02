#!/usr/bin/python3
""" starts a Flask web application that lists states """


from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def remove_session(dummy):
    """ function that closes db connection after every request """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states():
    """ returns states page """
    states = list(storage.all("State").values())
    states = [(state.id, state.name) for state in states]
    states.sort()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":

    # Your web application must be listening on 0.0.0.0, port 5000
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
