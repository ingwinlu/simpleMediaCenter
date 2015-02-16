from simpleMediaCenter import app, socketio

from flask import render_template
from flask.ext.socketio import emit

DEFAULT_STATUS={
        'player': 'not_implemented',
        'time' : 0
    }

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/controller')
def io_connect():
    emit_status(DEFAULT_STATUS)

@socketio.on('my event', namespace='/controller')
def io_controller(new_state):
    print(new_state)
    emit_status(DEFAULT_STATUS)

def emit_status(status):
    emit('new_status', status)
