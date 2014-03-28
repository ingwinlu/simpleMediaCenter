from interface.WebInterface import WebInterface
from player.Omxplayer import Omxplayer
import logging

logging.basicConfig(level=logging.DEBUG)
omxplayer = Omxplayer("")
interface = WebInterface(player=omxplayer)
interface.run()



