from Player import Player
import logging
import subprocess
import shlex
import time

class Omxplayer(Player):
    __cmdline=""
    __playerline="omxplayer"
    __process=None
    __stdin=None
    __stdout=None

    def __init__(self, cmdline):
        self.cmdline=cmdline

    def send(self, str):
        raise NotImplementedError

    def play(self, file):
        logging.debug("playing file: %s",file)
        if(self.__process is not None):
            self.stop()
        
        line = self.__playerline + " " + self.__cmdline + " " + file
        self.__process = subprocess.Popen(shlex.split(line), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        
    def stop(self):
        logging.debug("stopping")
        if(self.__process is None):
            logging.debug("nothing to stop")
            return
        self.__process.terminate()
        try:
            self.__process.wait(timeout=5)
        except TimeoutExpired:
            self.__process.kill()
        self.__process = None    
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing Omxplayer")
    omxplayer = Omxplayer("");
    omxplayer.stop()
    omxplayer.play("test.mp4")
    time.sleep(10)
    omxplayer.play("test.mp4")
    time.sleep(10)
    omxplayer.stop()
    omxplayer.stop()
    
    