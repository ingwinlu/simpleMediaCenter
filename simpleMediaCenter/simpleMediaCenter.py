from interface.WebInterface import WebInterface, WebController
from interface.Interface import InterfaceListable
from player.Omxplayer import Omxplayer
from player.Twitchplayer import Twitchplayer
from browser.Browser import FileBrowser, TwitchBrowser
from playlist.Playlist import Single
import logging
import os
import configparser

#config = configparser.ConfigParser()
#config_file = 'simpleMediaCenter-config.ini'
#load config sections over modules

pathToTemplates=os.path.abspath('./interface/templates/')
pathToStatic=os.path.abspath('./interface/static/')

logging.basicConfig(level=logging.DEBUG)

logging.info("creating player objects")
omxplayer = Omxplayer("-o both")
twitchplayer = Twitchplayer("-o both")
playerlist = InterfaceListable([omxplayer,twitchplayer])

logging.info("creating browser objects")
fileBrowser = FileBrowser()
twitchWinluBrowser = TwitchBrowser('winlu')
twitchKillerkakaduBrowser = TwitchBrowser('killerkakadu')
browserlist = InterfaceListable([fileBrowser,twitchWinluBrowser,twitchKillerkakaduBrowser])

logging.info("creating playlist objects")
#playList = Single()
#playlistlist = InterfaceListable([playList])
playlistlist = InterfaceListable([])

logging.info("creating controller")
controller = WebController(playerList=playerlist, playlistList=playlistlist, browserList=browserlist)

logging.info("creating webinterface")
interface = WebInterface(
    pathToTemplates,
    pathToStatic, 
    controller
    )
    
interface.run()


