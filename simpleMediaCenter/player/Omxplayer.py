from player.Player import Player
import logging
import subprocess
import shlex
import time

class Omxplayer(Player):
    __cmdline=""
    __playerline="omxplayer"
    __playerstatus=0 # 0 stopped, 1 playing, 2 paused
    __currentfile=""
    __process=None
    

    def __init__(self, cmdline):
        logging.debug("Omxplayer init")
        self.cmdline=cmdline
        
    def __resetplayer(self):
        logging.debug("reset Player")
        self.__playerstatus=0
        self.__currentfile=""
        self.__paused=False
        self.__process=None
        
    def poll(self):
        logging.debug("polling")
        if(self.__process is not None):
            logging.debug("process is not none")
            self.__process.poll()
            if(self.__process.returncode is not None):
                logging.debug("process ended")
                for line in self.__process.stdout:
                    logging.debug("stdout" + line.decode('utf-8'))
                self.__resetplayer()
                
    
    def send(self, str):
        logging.debug("Player send %s", str)
        self.poll()
        if(self.__process is not None):
            self.__process.stdin.write(bytes(str, 'UTF-8'))
            self.__process.stdin.flush()
            
    def getcmdline(self,file):
        return self.__playerline + " " + self.__cmdline + " '" + file + "'"

    def play(self, file):
        self.poll()
        logging.debug("playing: %s",file)
        if(self.__process is not None):
            self.stop()
            
        line = self.getcmdline(file)
        self.__process = subprocess.Popen(shlex.split(line), stdout=subprocess.PIPE, stdin=subprocess.PIPE , close_fds=True)
        self.__playerstatus=1
        self.__currentfile = file
        self.__paused=False
        
    def pause(self):
        self.poll()
        logging.debug("pause called")
        if(self.__process is not None):
            self.send('p')
            if(self.__playerstatus==1):
                self.__playerstatus=2
            else:
                self.__playerstatus=1
        
    def stop(self):
        self.poll()
        logging.debug("stopping")
        if(self.__process is not None):
            self.send('q')
            try:
                logging.debug("waiting for process to close")
                self.__process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logging.debug("timeout occured, killing")
                #self.__process.kill()
                subprocess.Popen(shlex.split("killall omxplayer.bin")).wait() ##quickhack
            self.__resetplayer()
            logging.debug("player stopped")
        
    def getDict(self):
        self.poll()
        tempDict={}
        tempDict['displayPlayerInNav'] = True
        tempDict['playerStatus'] = self.__playerstatus
        tempDict['currentFile'] = self.__currentfile
        tempDict['playerType'] = self.__class__.__name__
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
    
    