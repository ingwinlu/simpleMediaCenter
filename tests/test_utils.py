import unittest

from simpleMediaCenter.utils import sanitize_dbus_ms, dbus_playbackStatus_to_status

class TestUtils(unittest.TestCase):
    def test_duration_to_seconds(self):
        input = ['   int64 3713120000\n', '   int64 1331686\n']
        input = map(sanitize_dbus_ms,input)
        self.assertEqual(input, [3713120000, 1331686])
    
    def test_dbus_playbackStatus_to_status(self):
        input = ['   Playing']
        input = map(dbus_playbackStatus_to_status,input)
        self.assertEqual(input, ['playing'])

