#TODO: check for right environment

from simpleMediaCenter import app, socketio, utils

if __name__ == '__main__':
    args = utils.get_args()
    socketio.run(app, host=args.ip, port=args.port)