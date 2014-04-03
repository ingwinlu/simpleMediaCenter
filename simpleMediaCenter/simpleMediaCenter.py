from interface.WebInterface import WebInterface
from player.Omxplayer import Omxplayer
from browser.Browser import FileBrowser
from playlist.Playlist import Single
import logging
import os

pathToTemplates=os.path.abspath('./interface/templates/')
pathToStatic=os.path.abspath('./interface/static/')

logging.basicConfig(level=logging.DEBUG)
omxplayer = Omxplayer("-o both")
fileBrowser = FileBrowser()
playList = Single()
interface = WebInterface(pathToTemplates,pathToStatic, player=omxplayer, playlist=playList, browser=fileBrowser)
interface.run()


