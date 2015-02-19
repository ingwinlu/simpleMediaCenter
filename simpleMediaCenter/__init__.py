from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask.ext.socketio import SocketIO

from simpleMediaCenter.utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.args = get_args()
socketio = SocketIO(app)

import simpleMediaCenter.views