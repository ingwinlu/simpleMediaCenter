from simpleMediaCenter import app, socketio

from flask import render_template
from flask.ext.socketio import emit

STATE={
        'player': 'stop',
        'volume': 50,
        'time_current' : 0,
        'time_total' : 1
    }

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/controller')
def io_connect():
    print('new connection')
    emit_status(STATE)

@socketio.on('controller', namespace='/controller')
def io_controller(client_msg):
    STATE.update(client_msg)
    emit_status(STATE)

def emit_status(state):
    emit('new_state', state)

'''
    TODO, implement REST API for non socketio compatible clients
'''