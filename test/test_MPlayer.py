from simpleMediaCenter.player.MPlayer import MPlayer
import unittest
import time

class TestMPlayer(unittest.TestCase):
    testfilepath1 = "TEST VIDEO-1.mp4"
    testfilepath2 = "TEST VIDEO-2.mp4"
    

    def setUp(self):
        self.mplayer = MPlayer()
        
    def tearDown(self):
        self.mplayer.stop()
        self.mplayer=None
        
    def test_playback(self):
        self.mplayer.play(self.testfilepath1)
        #time.sleep(2)
        self.assertEqual(self.mplayer.getDict()['playerStatus'], 1)
        self.assertEqual(self.mplayer.getDict()['currentFile'], self.testfilepath1)
        self.mplayer.pause()   
        self.assertEqual(self.mplayer.getDict()['playerStatus'], 2)
        self.mplayer.pause()  
        self.assertEqual(self.mplayer.getDict()['playerStatus'], 1)
        self.mplayer.stop()  
        self.assertEqual(self.mplayer.getDict()['playerStatus'], 0)
        
    def test_play_while_play(self):
        self.mplayer.play(self.testfilepath1)
        self.mplayer.play(self.testfilepath2)
        self.assertEqual(self.mplayer.getDict()['currentFile'], self.testfilepath2)
        
    def test_keymapping(self):
        self.assertEqual(self.mplayer.keymapping['pause'], 'pause\n')
        self.assertEqual(self.mplayer.keymapping['quit'], 'quit\n')
        self.assertEqual(self.mplayer.keymapping['volume']['up'], 'volume +5\n')
        self.assertEqual(self.mplayer.keymapping['volume']['down'], 'volume -5\n')

        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestMPlayer))
        return testSuite
        
        
