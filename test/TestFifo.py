from simpleMediaCenter.playlist.Playlist import FiFo
import unittest

class TestFifo(unittest.TestCase):
    fifo = None
    testfilepath1 = "TEST VIDEO-1.mp4"
    testfilepath2 = "TEST VIDEO-2.mp4"

    def setUp(self):
        self.fifo = FiFo()
        
    def tearDown(self):
        self.fifo = None
        
    def test_ordering(self):
        self.fifo.add(self.testfilepath1)
        self.fifo.add(self.testfilepath2)
        self.assertEqual(self.fifo.getNext(),self.testfilepath1)
        self.assertEqual(self.fifo.getNext(),self.testfilepath2)
        
    
        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestFifo))
        return testSuite
        
        
