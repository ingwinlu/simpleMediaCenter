from browser.Browser import TwitchBrowser
import unittest
import time
import os
import logging

class TestTwitchBrowser(unittest.TestCase):
    twitchBrowser = None
    

    def setUp(self):
        self.twitchBrowser = TwitchBrowser()
        
    def tearDown(self):
        self.twitchBrowser = None
        
    def test_Root_Path(self):
        dic = self.twitchBrowser.getDict()
        self.assertEqual(dic['browserWorkingDir'], "/")
        
    def test_basic_navigation(self):
        tempBrowser = TwitchBrowser()
        tempBrowser.setWorkingDir(0)
        self.assertEqual(tempBrowser.getDict()['browserWorkingDir'], "Featured")
        tempBrowser.setWorkingDir(0) # should refresh
        self.assertEqual(tempBrowser.getDict()['browserWorkingDir'], "Featured")
        tempBrowser.setWorkingDir(1) # should go to root directory
        self.assertEqual(tempBrowser.getDict()['browserWorkingDir'], "/")
        tempBrowser.setWorkingDir(0) # should go to Featured
        self.assertEqual(tempBrowser.getDict()['browserWorkingDir'], "Featured")
        
    #need more testcases for navigation and wrong input
        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestTwitchBrowser))
        return testSuite
        
