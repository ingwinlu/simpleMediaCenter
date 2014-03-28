from interface.WebInterface import WebInterface
from player.Omxplayer import Omxplayer
import logging
import os

pathToTemplates=os.path.abspath('./interface/templates/')
pathToStatic=os.path.abspath('./interface/static')

print(pathToTemplates)
print(pathToStatic)

logging.basicConfig(level=logging.DEBUG)
omxplayer = Omxplayer("")
interface = WebInterface(pathToTemplates,pathToStatic,player=omxplayer)
interface.run()


