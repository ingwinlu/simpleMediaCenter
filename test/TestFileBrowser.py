from simpleMediaCenter.browser.Browser import FileBrowser
import unittest
import time
import os

class TestFileBrowser(unittest.TestCase):
    fileBrowser = None
    

    def setUp(self):
        self.fileBrowser = FileBrowser(".")
        
    def tearDown(self):
        self.fileBrowser = None
        
    def test_AbsPath(self):
        dic = self.fileBrowser.getDict()
        self.assertEqual(dic['browserWorkingDir'], os.path.abspath("."))
        
    def test_supported_Players(self):
        self.assertIn('Omxplayer', self.fileBrowser.getSupportedPlayers())
        self.assertNotIn('Twitchplayer', self.fileBrowser.getSupportedPlayers())
        
    #need more testcases for navigation testing and wrong input
        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestFileBrowser))
        return testSuite
        
