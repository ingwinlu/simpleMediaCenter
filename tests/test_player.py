import subprocess
import time
import unittest
import os
from simpleMediaCenter.player import OMXPlayer
from simpleMediaCenter.utils import get_dbus_session_addr

class TestOMXPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.testFile = {
            'location' : '/media/smb-192.168.0.10-Cloud/Top.Gear.S22E04.HDTV.x264-ORGANiC[ettv]/Top.Gear.S22E04.HDTV.x264-ORGANiC.mp4',
            'title' : 'top gear s22e04 test'
        }
        self.dbusLocation = '/tmp/omxplayerdbus.winlu'
        with open(self.dbusLocation) as f:
            self.dbusSession = f.read()[:-1]

    def test_status_stopped(self):
        omxplayer = OMXPlayer(self.dbusLocation)
        self.assertDictEqual(omxplayer.status, {'status': 'stopped', 'location': 'None', 'title': 'None', 'duration': 0, 'position': 0})

    def test_status_play_pause_stop(self):
        omxplayer = OMXPlayer('/tmp/omxplayerdbus.winlu')
        omxplayer.play(self.testFile)
        time.sleep(3) #dbus needs a few seconds to be ready
        self.assertEqual(omxplayer.status['status'], 'playing')
        omxplayer.pause()
        self.assertEqual(omxplayer.status['status'], 'paused')
        omxplayer.stop()
        self.assertEqual(omxplayer.status['status'], 'stopped')

    def test_duration(self):
        omxplayer = OMXPlayer('/tmp/omxplayerdbus.winlu')
        self.assertEqual(omxplayer.duration, 0)
        omxplayer.play(self.testFile)
        time.sleep(3)
        self.assertNotEqual(omxplayer.duration, 0)

    def test_dbus_session_reader(self):
        self.assertEqual(get_dbus_session_addr(self.dbusLocation), self.dbusSession)

    def tearDown(self):
        with open(os.devnull, "w") as fnull:
            subprocess.call(['killall','omxplayer.bin'], stdout = fnull, stderr = fnull)
        