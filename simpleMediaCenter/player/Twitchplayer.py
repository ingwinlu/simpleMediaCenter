from simpleMediaCenter.player.Omxplayer import Omxplayer
from simpleMediaCenter.helpers.twitch import TwitchVideoResolver
import logging
import os

class Twitchplayer(Omxplayer):
    __logger=logging.getLogger(__name__)
    __cmdline="-o both"
    __playerline="omxplayer -b"
    __playlist="twitchplaylist.m3u8"
    

    def __init__(self, cmdline = "-o both"):
        self.__logger.debug("Twitchplayer init")
        self.__cmdline=cmdline
               
    
    def getcmdline(self,file):
        tvr = TwitchVideoResolver(self.__logger) 
        tvr.saveHLSToPlaylist(file, 0, self.__playlist)
        cmdline = self.__playerline + " " + self.__cmdline + " '" + self.__playlist + "'"
        self.__logger.debug('twitchplayer cmdline: ' + cmdline)
        return cmdline
        
    def stop(self):
        super(Twitchplayer, self).stop()
        if (os.path.isfile(self.__playlist)):
            os.remove(self.__playlist)
            
