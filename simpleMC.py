#!/usr/bin/env python2

from simpleMediaCenter import app, socketio


if __name__ == '__main__':
    socketio.run(app, host=app.args.ip, port=app.args.port)