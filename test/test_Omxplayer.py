from simpleMediaCenter.player.Omxplayer import Omxplayer
import unittest
import time

class TestOmxplayer(unittest.TestCase):
    omxplayer = None
    testfilepath1 = "TEST VIDEO-1.mp4"
    testfilepath2 = "TEST VIDEO-2.mp4"
    

    def setUp(self):
        self.omxplayer = Omxplayer("-o both")
        
    def tearDown(self):
        self.omxplayer.stop()
        self.omxplayer=None
        
    def test_playback(self):
        self.omxplayer.play(self.testfilepath1)
        #time.sleep(2)
        self.assertEqual(self.omxplayer.getDict()['playerStatus'], 1)
        self.assertEqual(self.omxplayer.getDict()['currentFile'], self.testfilepath1)
        self.omxplayer.pause()   
        self.assertEqual(self.omxplayer.getDict()['playerStatus'], 2)
        self.omxplayer.pause()  
        self.assertEqual(self.omxplayer.getDict()['playerStatus'], 1)
        self.omxplayer.stop()  
        self.assertEqual(self.omxplayer.getDict()['playerStatus'], 0)
        
    def test_play_while_play(self):
        self.omxplayer.play(self.testfilepath1)
        self.omxplayer.play(self.testfilepath2)
        self.assertEqual(self.omxplayer.getDict()['currentFile'], self.testfilepath2)
        
    def test_keymapping(self):
        self.assertEqual(self.omxplayer.keymapping['pause'], 'p')
        self.assertEqual(self.omxplayer.keymapping['quit'], 'q')
        self.assertEqual(self.omxplayer.keymapping['volume']['up'], '+')
        self.assertEqual(self.omxplayer.keymapping['volume']['down'], '-')

        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestOmxplayer))
        return testSuite
        
        
