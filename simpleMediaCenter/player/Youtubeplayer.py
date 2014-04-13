#import youtube_dl
#rework to use youtube_dl module and not process for improved performance

from player.Omxplayer import Omxplayer
import logging
import sys
import os
import subprocess
import shlex
import time

class Youtubeplayer(Omxplayer):
    __youtubeprocess=None
    __playerline="omxplayer --live"
    __cmdline="-o both"
    __tempfile=""
    __youtubedlline=""
    

    def __init__(self, cmdline = "-o both"):
        logging.debug("Youtubeplayer init")
        self.__cmdline=cmdline
        self.__tempfile="temp.mp4"
        self.__youtubedlline="youtube-dl --no-part -o " + self.__tempfile
        
    def startDownload(self, url):
        cmdline = self.__youtubedlline + " " + url
        self.__youtubeprocess = subprocess.Popen(
            shlex.split(cmdline), 
            stdout=subprocess.PIPE, 
            stdin=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            close_fds=True)
        while (os.path.isfile(self.__tempfile) is False):
            logging.debug("waiting for filecreation")
            time.sleep(1)
        return self.__tempfile
        
        
    
    def getcmdline(self,url):
        self.startDownload(url)        
        cmdline = self.__playerline + " " + self.__cmdline + " '" + self.__tempfile + "'"
        logging.debug('Youtubeplayer cmdline: ' + cmdline)
        return cmdline
        
    def stop(self):
        super(Youtubeplayer, self).stop()
        if (self.__youtubeprocess is not None):
            try:
                self.__youtubeprocess.terminate()
                logging.debug("waiting for __youtubeprocess to close")
                self.__youtubeprocess.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.__youtubeprocess.kill()
            except ProcessLookupError:
                pass
        if (os.path.isfile(self.__tempfile)):
            os.remove(self.__tempfile)
            
