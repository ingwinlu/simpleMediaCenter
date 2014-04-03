from interface.WebInterface import WebInterface
from player.Omxplayer import Omxplayer
from fileCrawler.FileCrawler import FileCrawler
from playlist.Playlist import Single
import logging
import os

pathToTemplates=os.path.abspath('./interface/templates/')
pathToStatic=os.path.abspath('./interface/static/')

logging.basicConfig(level=logging.DEBUG)
omxplayer = Omxplayer("-o hdmi")
fileCrawler = FileCrawler()
playList = Single()
interface = WebInterface(pathToTemplates,pathToStatic, player=omxplayer, playlist=playList, browser=fileCrawler)
interface.run()


