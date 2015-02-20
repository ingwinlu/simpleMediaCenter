import argparse

def get_args():
    parser = argparse.ArgumentParser(description= "simple Media Center application")
    parser.add_argument("-i", "--ip", nargs="?", default="0.0.0.0", help="ip address on which to serve [0.0.0.0]")
    parser.add_argument("-p", "--port", nargs="?", type=int, default=5000, help="port on which to serve [5000]")
    parser.add_argument("--dbus", nargs="?", default="/tmp/omxplayerdbus.winlu", help="omxplayer dbus file location [/tmp/omxplayerdbus]")
    #parser.add_argument("--dbus-pid", nargs="?", default="/tmp/omxplayerdbus.winlu.pid", help="omxplayer dbus pid file location [/tmp/omxplayerdbus.pid]")
    #parser.add_argument("--player", nargs="?", default="omxplayer", help="omxplayer executable [omxplayer]")
    '''
        TODO remove .winlu
    '''
    return parser.parse_args()

def get_dbus_session_addr(dbus_file='/tmp/omxplayerdbus'):
    try:
        with open(dbus_file, 'r') as f:
            return f.read()[:-1]
    except:
        return None

def sanitize_dbus_ms(duration):
    ms = 0
    try:
        ms = int(duration.split()[1])
    except:
        pass
    return ms

def ms_to_seconds(ms):
    return ms / 1000000

def seconds_to_ms(seconds):
    return seconds * 1000000

def calculate_pos(duration, percent):
    return percent * duration / 100

def dbus_playbackStatus_to_status(dbus_status):
    return dbus_status.split()[0].lower()