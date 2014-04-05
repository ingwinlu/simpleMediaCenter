from player.Omxplayer import Omxplayer
from helpers.twitch import TwitchVideoResolver
import logging
import sys

class Twitchplayer(Omxplayer):
    __playerline="omxplayer"
    __cmdline=""
    

    def __init__(self, cmdline = "-o both"):
        logging.debug("Twitchplayer init")
        self.__cmdline=cmdline
               
    
    def getcmdline(self,file):
        tvr = TwitchVideoResolver(logging) 
        return self.__playerline + " " + self.__cmdline + " '" + tvr.getRTMPUrl(file, sys.maxsize) + "'"
        
            
