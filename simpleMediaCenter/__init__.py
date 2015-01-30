from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask.ext.socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

import simpleMediaCenter.views