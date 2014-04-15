from player.Omxplayer import Omxplayer
import youtube_dl
import logging
import sys
import os
import subprocess
import shlex
import time
import threading

class Youtubeplayer(Omxplayer):
    __playerline="omxplayer -b --live"
    __cmdline="-o both"
    __ytdl=None

    def __init__(self, cmdline = "-o both"):
        logging.debug("Youtubeplayer init")
        self.__cmdline=cmdline
        self.__ytdl=youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
        self.__ytdl.add_default_info_extractors()
  
    def getcmdline(self,url):
        result = self.__ytdl.extract_info(url,download=False)
        cmdline = self.__playerline + " " + self.__cmdline + " '" + result['url'] + "'"
        logging.debug('Youtubeplayer cmdline: ' + cmdline)
        return cmdline

