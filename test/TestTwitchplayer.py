from simpleMediaCenter.player.Twitchplayer import Twitchplayer
import unittest
import time
import requests

class TestTwitchplayer(unittest.TestCase):
    twitchplayer = None  
    twitchurl= "https://api.twitch.tv/kraken/streams/featured?limit=1"
    playurl= None

    def setUp(self):
        self.twitchplayer = Twitchplayer()
        tempjson = requests.get(self.twitchurl).json()
        #self.playurl = "twitch.tv/"
        self.playurl = tempjson['featured'][0]['stream']['channel']['name']
        
    def tearDown(self):
        self.twitchplayer.stop()
        self.twitchplayer=None
        
    def test_playback(self):
        self.assertEqual(self.twitchplayer.getDict()['playerStatus'], 0)
        self.twitchplayer.play(self.playurl)
        time.sleep(10)
        self.twitchplayer.pause()   
        self.assertEqual(self.twitchplayer.getDict()['playerStatus'], 2)
        self.twitchplayer.pause()  
        self.assertEqual(self.twitchplayer.getDict()['playerStatus'], 1)
        self.twitchplayer.stop()  
        self.assertEqual(self.twitchplayer.getDict()['playerStatus'], 0)
        
        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestTwitchplayer))
        return testSuite
        
