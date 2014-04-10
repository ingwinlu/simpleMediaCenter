from browser.Browser import TwitchBrowser
import unittest
import time
import os

class TestTwitchBrowser(unittest.TestCase):
    twitchBrowser = None
    

    def setUp(self):
        self.twitchBrowser = TwitchBrowser()
        
    def tearDown(self):
        self.twitchBrowser = None
        
    def test_Root_Path(self):
        dic = self.twitchBrowser.getDict()
        self.assertEqual(dic['browserWorkingDir'], "/")
        
    def test_change_to_featured(self):
        tempBrowser = TwitchBrowser()
        tempBrowser.setWorkingDir(3)
        self.assertEqual(dic['browserWorkingDir'], "Featured")
        
    #need more testcases for navigation and wrong input
        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestTwitchBrowser))
        return testSuite
        
