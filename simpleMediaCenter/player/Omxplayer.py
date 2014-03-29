from player.Player import Player
import logging
import subprocess
import shlex
import time

class Omxplayer(Player):
    __cmdline=""
    __playerline="omxplayer"
    __playerstatus="Stopped"
    __process=None

    def __init__(self, cmdline):
        logging.debug("Omxplayer init")
        self.cmdline=cmdline

    def send(self, str):
        logging.debug("Omxplayer send %s", str)
        self.__process.stdin.write(bytes(str, 'UTF-8'))
        self.__process.stdin.flush()

    def play(self, file):
        logging.debug("playing file: %s",file)
        if(self.__process is not None):
            self.stop()
        
        line = self.__playerline + " " + self.__cmdline + " " + file
        self.__process = subprocess.Popen(shlex.split(line), stdout=subprocess.PIPE, stdin=subprocess.PIPE , close_fds=True)
        self.__playerstatus="Playing " + file
        
    def pause(self):
        logging.debug("pause called")
        if(process is not None):
            self.send('p')
            self.__playerstatus="Paused " + file
        
    def stop(self):
        logging.debug("stopping")
        if(self.__process is None):
            logging.debug("nothing to stop")
            return
        self.send('q')
        try:
            logging.debug("waiting for process to close")
            self.__process.wait(timeout=5)
        except TimeoutExpired:
            logging.debug("timeout occured, killing")
            #self.__process.kill()
            subprocess.Popen(shlex.split("killall omxplayer.bin")).wait() ##quickhack
        self.__process = None    
        logging.debug("player stopped")
        self.__playerstatus="Stopped"
        
    def getDict(self):
        tempDict={}
        tempDict['displayPlayer'] = True
        tempDict['playerStatus'] = self.__playerstatus
        return tempDict
        

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
    
    