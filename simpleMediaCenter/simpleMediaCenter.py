from interface.WebInterface import WebInterface, WebController
from interface.Interface import InterfaceListable
from player.Omxplayer import Omxplayer
from player.Twitchplayer import Twitchplayer
from browser.Browser import FileBrowser
from playlist.Playlist import Single
import logging
import os

pathToTemplates=os.path.abspath('./interface/templates/')
pathToStatic=os.path.abspath('./interface/static/')

logging.basicConfig(level=logging.DEBUG)

logging.info("creating player objects")
omxplayer = Omxplayer("-o both")
twitchplayer = Twitchplayer("-o both")
playerlist = InterfaceListable([omxplayer,twitchplayer])

logging.info("creating browser objects")
fileBrowser = FileBrowser()
browserlist = InterfaceListable([fileBrowser])

logging.info("creating playlist objects")
playList = Single()
playlistlist = InterfaceListable([playList])

logging.info("creating controller")
controller = WebController(playerList=playerlist, playlistList=playlistlist, browserList=browserlist)

logging.info("creating webinterface")
interface = WebInterface(
    pathToTemplates,
    pathToStatic, 
    controller
    )
    
interface.run()


