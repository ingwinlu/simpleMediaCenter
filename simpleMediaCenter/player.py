import os
import subprocess
import time
from threading import Thread
from simpleMediaCenter.utils import get_dbus_session_addr, \
    sanitize_dbus_ms, dbus_playbackStatus_to_status, \
    calculate_pos
from simpleMediaCenter import app

DEVNULL = open(os.devnull, 'wb')
DEFAULT_STATUS = {
            'location'      : 'None',
            'title'         : 'None',
            'status'        : 'stopped',
            'duration'      : 0,
            'position'      : 0
        }

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
                stdout=DEVNULL, 
                stdin=subprocess.PIPE, 
                stderr=DEVNULL,
                close_fds=True
            )
        while self.running and omx_subprocess.returncode is None:
            omx_subprocess.poll()
            time.sleep(1)
        if not omx_subprocess.returncode:
            # process did not end normally, kill via stdin
            try:
                omx_subprocess.stdin.write('q')
                omx_subprocess.terminate()
            except:
                pass
            omx_subprocess.wait()

    def stop(self):
        self.running = False

class OMXPlayer(object):
    def __init__(self, dbus_file=app.args.dbus):
        self.__status = DEFAULT_STATUS.copy()
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
        self.__status.update(DEFAULT_STATUS)

    def pause(self):
        try:
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            subprocess.call([
                'dbus-send', '--print-reply=literal', '--session', '--dest=org.mpris.MediaPlayer2.omxplayer',
                '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player.Action', 'int32:16'],
                env = self.env,
                stdout=DEVNULL,
                stderr=DEVNULL)
        except subprocess.CalledProcessError as e:
            pass

    def vol_down(self):
        try:
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            subprocess.call([
                'dbus-send', '--print-reply=literal', '--session', '--dest=org.mpris.MediaPlayer2.omxplayer',
                '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player.Action', 'int32:17'],
                env = self.env,
                stdout=DEVNULL,
                stderr=DEVNULL)
        except subprocess.CalledProcessError as e:
            pass

    def vol_up(self):
        try:
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            subprocess.call([
                'dbus-send', '--print-reply=literal', '--session', '--dest=org.mpris.MediaPlayer2.omxplayer',
                '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player.Action', 'int32:18'],
                env = self.env,
                stdout=DEVNULL,
                stderr=DEVNULL)
        except subprocess.CalledProcessError as e:
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
                env = self.env,
                stderr=DEVNULL)
            duration = sanitize_dbus_ms(duration)
        except subprocess.CalledProcessError as e:
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
                env = self.env,
                stderr=DEVNULL)
            position = sanitize_dbus_ms(position)
        except subprocess.CalledProcessError as e:
            pass
        return position

    @position.setter
    def position(self, new_position_percent):
        try:
            new_position = calculate_pos(new_position_percent, self.duration)
            pos_str = str(new_position)
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            subprocess.call([
                'dbus-send', '--print-reply=literal', '--session',
                '--dest=org.mpris.MediaPlayer2.omxplayer', '/org/mpris/MediaPlayer2',
                'org.mpris.MediaPlayer2.Player.SetPosition', 'objpath:/not/used',
                'int64:' + pos_str],
                env = self.env,
                stdout=DEVNULL,
                stderr=DEVNULL)
        except subprocess.CalledProcessError as e:
            pass

    @property
    def playbackStatus(self):
        playbackStatus = 'stopped'
        try:
            self.env['DBUS_SESSION_BUS_ADDRESS'] = get_dbus_session_addr(self.dbus_file)
            output = subprocess.check_output([
                'dbus-send', '--print-reply=literal', '--session',
                '--reply-timeout=500', '--dest=org.mpris.MediaPlayer2.omxplayer',
                '/org/mpris/MediaPlayer2', 'org.freedesktop.DBus.Properties.PlaybackStatus'],
                env = self.env,
                stderr=DEVNULL)
            playbackStatus = dbus_playbackStatus_to_status(output)
        except subprocess.CalledProcessError as e:
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

testStream = {
}
