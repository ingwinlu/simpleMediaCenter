#!/usr/bin/env python2

from simpleMediaCenter import utils, app, socketio

if __name__ == '__main__':
    args = utils.get_args()
    socketio.run(app, host=args.ip, port=args.port)