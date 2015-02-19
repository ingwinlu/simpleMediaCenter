import os
import subprocess
import time
from threading import Thread
from simpleMediaCenter.utils import get_dbus_session_addr, dbus_ms_to_seconds, dbus_playbackStatus_to_status


class OMXPlayerRunner(Thread):
    def __init__(self, location):
        Thread.__init__(self)
        self.location = location

    def run(self):
        self.running = True
        omx_subprocess = subprocess.Popen(
                [
                    'omxplayer',
                    '-o', 'both',
                    self.location
                ],
                stdout=subprocess.PIPE, 
                stdin=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                close_fds=True
            )
        while self.running and omx_subprocess.returncode is None:
            omx_subprocess.poll()
            time.sleep(1)
        if not omx_subprocess.returncode:
            # process did not end normally, kill via stdin
            omx_subprocess.stdin.write('q')
            omx_subprocess.terminate()
            omx_subprocess.wait()

    def stop(self):
        self.running = False

class OMXPlayer(object):
    def __init__(self, dbus_file='/tmp/omxplayerdbus'):
        self.__status = {
            'location'      : 'None',
            'title'         : 'None',
            'status'        : 'stopped',
            'duration'      : 0,
            'position'      : 0
        }
        self.env = os.environ.copy()
        self.runner = None
        self.dbus_file = dbus_file

    def play(self, toPlay):
        if self.runner:
            self.runner.stop()
            self.runner.join()
        self.__status.update(toPlay)
        self.runner = OMXPlayerRunner(self.__status['location'])
        self.runner.start()

    def stop(self):
        if self.runner:
            self.runner.stop()
            self.runner.join()
            self.runner = None

    def pause(self):
        print('pause')
        pass

    def vol_down(self):
        print('vol down')
        pass

    def vol_up(self):
        print('vol up')
        pass

    @property
    def duration(self):
        duration = 0
        try:
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            duration = subprocess.check_output([
                'dbus-send', '--print-reply=literal', '--session',
                '--reply-timeout=500', '--dest=org.mpris.MediaPlayer2.omxplayer',
                '/org/mpris/MediaPlayer2', 'org.freedesktop.DBus.Properties.Duration'],
                env = self.env)
            duration = dbus_ms_to_seconds(duration)
        except Exception as e:
            print(repr(e))
            pass
        return duration

    @property
    def position(self):
        position = 0
        try:
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            position = subprocess.check_output([
                'dbus-send', '--print-reply=literal', '--session',
                '--reply-timeout=500', '--dest=org.mpris.MediaPlayer2.omxplayer',
                '/org/mpris/MediaPlayer2', 'org.freedesktop.DBus.Properties.Position'],
                env = self.env)
            position = dbus_ms_to_seconds(position)
        except Exception as e:
            print(repr(e))
            pass
        return position

    @property
    def playbackStatus(self):
        playbackStatus = 'stopped'
        try:
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            playbackStatus = subprocess.check_output([
                'dbus-send', '--print-reply=literal', '--session',
                '--reply-timeout=500', '--dest=org.mpris.MediaPlayer2.omxplayer',
                '/org/mpris/MediaPlayer2', 'org.freedesktop.DBus.Properties.PlaybackStatus'],
                env = self.env)
            playbackStatus = dbus_playbackStatus_to_status(playbackStatus)
        except Exception as e:
            print(repr(e))
            pass
        return playbackStatus

    @property
    def status(self):
        self.__status.update({
            'status': self.playbackStatus,
            'position' : self.position,
            'duration' : self.duration
            })
        return self.__status
    

testFile = {
    'location' : '/media/smb-192.168.0.10-Cloud/Top.Gear.S22E04.HDTV.x264-ORGANiC[ettv]/Top.Gear.S22E04.HDTV.x264-ORGANiC.mp4',
    'title' : 'top gear s22e04 test'
}


'''
#!/usr/bin/env python

import dbus, time
from subprocess import Popen

# media file to open
file="/path/to/media/file.mp4"

# open omxplayer
cmd = "omxplayer --win '0 0 100 100' %s" %(file)
Popen([cmd], shell=True)

# wait for omxplayer to initialise
done,retry=0,0
while done==0:
    try:
        with open('/tmp/omxplayerdbus', 'r+') as f:
            omxplayerdbus = f.read().strip()
        bus = dbus.bus.BusConnection(omxplayerdbus)
        object = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
        dbusIfaceProp = dbus.Interface(object,'org.freedesktop.DBus.Properties')
        dbusIfaceKey = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
        done=1
    except:
        retry+=1
        if retry >= 50:
            print "ERROR"
            raise SystemExit

# property: print duration of file
print dbusIfaceProp.Duration()

# key: pause after 5 seconds
time.sleep(5)
dbusIfaceKey.Action(dbus.Int32("16"))

# key: un-pause after 5 seconds
time.sleep(5)
dbusIfaceKey.Action(dbus.Int32("16"))

# key: quit after 5 seconds
time.sleep(5)
dbusIfaceKey.Action(dbus.Int32("15"))
'''