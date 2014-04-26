from simpleMediaCenter.player.Omxplayer import Omxplayer
from simpleMediaCenter.helpers.twitch import TwitchVideoResolver
import logging
import os

class Twitchplayer(Omxplayer):
    __logger=logging.getLogger(__name__)
    __playerline="omxplayer -b"
    __cmdline="-o both"
    __playlist="twitchplaylist.m3u8"
    

    def __init__(self, cmdline = "-o both"):
        self.__logger.debug("Twitchplayer init")
        self.__cmdline=cmdline
               
    
    def getcmdline(self,file):
        return self.__playerline + " " + self.__cmdline + " '" + file + "'"
        
    def stop(self):
        super(Twitchplayer, self).stop()
        if (os.path.isfile(self.__playlist)):
            os.remove(self.__playlist)
            
