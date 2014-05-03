from simpleMediaCenter.player.Omxplayer import Omxplayer
import logging
import os

class MPlayer(Omxplayer):
    __logger=logging.getLogger(__name__)
    __playerline="mplayer -slave -fs -vo xv -zoom"
    
    keymapping = {
        'pause' : 'pause\n',
        'quit'  : 'quit\n',
        'volume': {
                    'up'   : 'volume +5\n',
                    'down' : 'volume -5\n'
                  }
        }

    def __init__(self):
        self.__logger.debug("init")
    
    def getcmdline(self,file):
        return self.__playerline + " " + " '" + file + "'"
        

