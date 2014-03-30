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
    __paused=False

    def __init__(self, cmdline):
        logging.debug("Omxplayer init")
        self.cmdline=cmdline
        
    def poll(self):
        logging.debug("polling")
        if(self.__process is not None):
            logging.debug("process is not none")
            self.__process.poll()
            if(self.__process.returncode is not None):
                logging.debug("process ended")
                # read sterr or stdout maybe before setting to None
                self.__playerstatus="Stopped"
                self.__paused=False
                self.__process=None
        

    def send(self, str):
        logging.debug("Omxplayer send %s", str)
        self.poll()
        if(self.__process is not None):
            self.__process.stdin.write(bytes(str, 'UTF-8'))
            self.__process.stdin.flush()

    def play(self, file):
        self.poll()
        logging.debug("playing file: %s",file)
        if(self.__process is not None):
            self.stop()
            
        line = self.__playerline + " " + self.__cmdline + " " + file
        self.__process = subprocess.Popen(shlex.split(line), stdout=subprocess.PIPE, stdin=subprocess.PIPE , close_fds=True)
        self.__playerstatus="Playing " + file
        self.__paused=False
        
    def pause(self):
        self.poll()
        logging.debug("pause called")
        if(self.__process is not None):
            self.send('p')
            if(self.__paused==False):
                self.__playerstatus="Paused"
                self.__paused=True
            else:
                self.__playerstatus="Unpaused"
                self.__paused=False
        
    def stop(self):
        self.poll()
        logging.debug("stopping")
        if(self.__process is not None):
            self.send('q')
            try:
                logging.debug("waiting for process to close")
                self.__process.wait(timeout=5)
            except TimeoutExpired:
                logging.debug("timeout occured, killing")
                #self.__process.kill()
                subprocess.Popen(shlex.split("killall omxplayer.bin")).wait() ##quickhack
            self.__process = None    
            self.__paused=False
            self.__playerstatus="Stopped"
            logging.debug("player stopped")
        
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
    
    