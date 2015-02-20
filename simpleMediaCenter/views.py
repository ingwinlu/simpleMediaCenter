from simpleMediaCenter import app, socketio
from simpleMediaCenter.player import OMXPlayer, testFile

from threading import Thread

from flask import render_template
from flask.ext.socketio import emit

import time

omxplayer = OMXPlayer(app.args.dbus)
update_thread = None

def player_update_thread():
    while True:
        time.sleep(1)
        socketio.emit('player_status', omxplayer.status, namespace='/controller')

@app.route('/')
def index():
    global update_thread
    if update_thread is None:
        update_thread = Thread(target=player_update_thread)
        update_thread.start()
    return render_template('index.html')

@socketio.on('connect', namespace='/controller')
def io_connect():
    print('new connection')
    socketio.emit('player_status', omxplayer.status, namespace='/controller')

@socketio.on('player_stop', namespace='/controller')
def io_controller():
    omxplayer.stop()

@socketio.on('player_play', namespace='/controller')
def io_controller():
    omxplayer.play(testFile)

@socketio.on('player_pause', namespace='/controller')
def io_controller():
    omxplayer.pause()

@socketio.on('player_vol_down', namespace='/controller')
def io_controller():
    omxplayer.vol_down()

@socketio.on('player_vol_up', namespace='/controller')
def io_controller():
    omxplayer.vol_up()

@socketio.on('set_pos', namespace='/controller')
def jump_to_position(data):
    omxplayer.position = data['position']
'''
    TODO, implement REST API for non socketio compatible clients
'''