from player.Omxplayer import Omxplayer
from helpers.twitch import TwitchVideoResolver
import logging
import sys
import os

class Twitchplayer(Omxplayer):
    __playerline="omxplayer"
    __cmdline=""
    __playlist="twitchplaylist.m3u8"
    

    def __init__(self, cmdline = "-o both"):
        logging.debug("Twitchplayer init")
        self.__cmdline=cmdline
               
    
    def getcmdline(self,file):
        tvr = TwitchVideoResolver(logging) 
        tvr.saveHLSToPlaylist(file, 0, self.__playlist)
        return self.__playerline + " " + self.__cmdline + " '" + self.__playlist + "'"
        
    def stop(self):
        super(Twitchplayer, self).stop()
        if (os.path.isfile(self.__playlist)):
            os.remove(self.__playlist)
            
