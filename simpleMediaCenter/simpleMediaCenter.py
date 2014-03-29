from interface.WebInterface import WebInterface
from player.Omxplayer import Omxplayer
from fileCrawler.FileCrawler import FileCrawler
#from fileCrawler.FileCrawler import FileCrawler
import logging
import os

pathToTemplates=os.path.abspath('./interface/templates/')
pathToStatic=os.path.abspath('./interface/static/')

logging.basicConfig(level=logging.DEBUG)
omxplayer = Omxplayer("-o hdmi")
fileCrawler = FileCrawler()
interface = WebInterface(pathToTemplates,pathToStatic, player=omxplayer, browser=fileCrawler)
interface.run()


