from simpleMediaCenter.interface.Interface import InterfaceListable
from simpleMediaCenter.player.Omxplayer import Omxplayer
from simpleMediaCenter.player.Twitchplayer import Twitchplayer
from simpleMediaCenter.player.Youtubeplayer import Youtubeplayer
from simpleMediaCenter.browser.Browser import *
import logging
import unittest

class TestAutoPlayerSelect(unittest.TestCase):

    def test_auto_select(self):
        logging.info("creating player objects")
        omxplayer = Omxplayer("-o both")
        twitchplayer = Twitchplayer("-o both")
        youtubeplayer = Youtubeplayer("-o both")
        playerlist = InterfaceListable([omxplayer,twitchplayer, youtubeplayer])
        
        logging.info("creating browser objects")
        fileBrowser = FileBrowser()
        twitchWinluBrowser = TwitchBrowser('winlu')
        twitchKillerkakaduBrowser = TwitchBrowser('killerkakadu')
        youtubeBrowser = YoutubeBrowser()
        browserList = InterfaceListable([fileBrowser,twitchWinluBrowser,twitchKillerkakaduBrowser,youtubeBrowser])
        
        browserList.setActive(0)
        for supportedPlayer in browserList.getActive().getSupportedPlayers():
            id = playerlist.getIDfromName(supportedPlayer)
            if (id is not None):
                break
                
        self.assertEqual(id,0)
        
        browserList.setActive(1)
        for supportedPlayer in browserList.getActive().getSupportedPlayers():
            id = playerlist.getIDfromName(supportedPlayer)
            if (id is not None):
                break
                
        self.assertEqual(id,1)
        
        browserList.setActive(2)
        for supportedPlayer in browserList.getActive().getSupportedPlayers():
            id = playerlist.getIDfromName(supportedPlayer)
            if (id is not None):
                break
                
        self.assertEqual(id,1)
        
        browserList.setActive(3)
        for supportedPlayer in browserList.getActive().getSupportedPlayers():
            id = playerlist.getIDfromName(supportedPlayer)
            if (id is not None):
                break
                
        self.assertEqual(id,2)
        


        
    def suite(self):
        testSuite = unittest.TestSuite()
        testSuite.addTest(unittest.makeSuite(TestAutoPlayerSelect))
        return testSuite
        
