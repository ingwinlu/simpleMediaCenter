from player.Omxplayer import Omxplayer
import logging
import subprocess
import shlex
import time

class Livestreamer(Omxplayer):
    __playerline="livestreamer"
    __mediaplayer=""
    

    def __init__(self, mediaplayer = "omxplayer -o hdmi"):
        logging.debug("livestreamer init")
        self.__mediaplayer=mediaplayer
               
    
    def getcmdline(self,file):
        return self.__playerline + " " + file + " " + "best -np '" + self.mediaplayer + "'"
            
  
    
    