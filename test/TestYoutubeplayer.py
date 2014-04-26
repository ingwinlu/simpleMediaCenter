from simpleMediaCenter.player.Youtubeplayer import Youtubeplayer
import unittest
import time
import requests
import os

class TestYoutubeplayer(unittest.TestCase):
    youtubeplayer = None  
    youtubeurl= "https://www.youtube.com/watch?v=Cwr-FhjE8Fw"

    def setUp(self):
        self.youtubeplayer = Youtubeplayer()
        
    def tearDown(self):
        self.youtubeplayer.stop()
        self.youtubeplayer=None
    
    '''
    def test_download(self):
        filename = self.youtubeplayer.startDownload(self.youtubeurl)
        self.assertTrue(os.path.isfile(filename))
    '''
    def test_playback(self):
        self.assertEqual(self.youtubeplayer.getDict()['playerStatus'], 0)
        self.youtubeplayer.play(self.youtubeurl)
        time.sleep(10)
        self.youtubeplayer.pause()   
        self.assertEqual(self.youtubeplayer.getDict()['playerStatus'], 2)
        self.youtubeplayer.pause()  
        self.assertEqual(self.youtubeplayer.getDict()['playerStatus'], 1)
        self.youtubeplayer.stop()  
        self.assertEqual(self.youtubeplayer.getDict()['playerStatus'], 0)

        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestYoutubeplayer))
        return testSuite
        
