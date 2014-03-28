from interface.WebInterface import WebInterface
from player.Omxplayer import Omxplayer
import logging

pathToTemplates='./interface/templates/'
pathToStatic='./interface/static'

logging.basicConfig(level=logging.DEBUG)
omxplayer = Omxplayer("")
interface = WebInterface(player=omxplayer)
interface.run()


