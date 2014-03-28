from Player import Player
import logging
import subprocess
import shlex
import time

class Omxplayer(Player):
    __cmdline=""
    __playerline="omxplayer"
    __process=None

    def __init__(self, cmdline):
        self.cmdline=cmdline

    def send(self, str):
        raise NotImplementedError

    def play(self, file):
        logging.debug("playing file: %s",file)
        if(self.__process is not None):
            self.stop()
        
        line = self.__playerline + " " + self.__cmdline + " " + file
        self.__process = subprocess.Popen(shlex.split(line), stdout=subprocess.PIPE, stdin=subprocess.PIPE , close_fds=True)
        
    def stop(self):
        logging.debug("stopping")
        if(self.__process is None):
            logging.debug("nothing to stop")
            return
        self.__process.stdin.write(bytes('q', 'UTF-8'))
        self.__process.stdin.flush()
        try:
            logging.debug("waiting for process to close")
            self.__process.wait(timeout=5)
        except TimeoutExpired:
            logging.debug("timeout occured, killing")
            #self.__process.kill()
            subprocess.Popen(shlex.split("killall omxplayer.bin")).wait() ##quickhack
        self.__process = None    
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing Omxplayer")
    omxplayer = Omxplayer("");
    omxplayer.stop()
    omxplayer.play("test.mp4")
    logging.debug("sleeping for 10 seconds")
    time.sleep(10)
    logging.debug("done sleeping")
    omxplayer.play("test.mp4")
    logging.debug("sleeping for 10 seconds")
    time.sleep(10)
    logging.debug("done sleeping")
    omxplayer.stop()
    omxplayer.stop()
    
    