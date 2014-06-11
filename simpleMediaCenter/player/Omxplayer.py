from simpleMediaCenter.player.Player import Player
import logging
import subprocess
import shlex
import time

class Omxplayer(Player):
    __logger=logging.getLogger(__name__)
    __cmdline="-o both"
    __playerline="omxplayer -b"
    __playerstatus=0 # 0 stopped, 1 playing, 2 paused
    __currentfile=""
    __process=None
    
    keymapping = {
        'pause' : 'p',
        'quit'  : 'q',
        'volume': {
                    'up'   : '+',
                    'down' : '-'
                  }
        }
    

    def __init__(self, cmdline = "-o both"):
        self.__logger.debug("Omxplayer init")
        self.cmdline=cmdline
        
    def __resetplayer(self):
        self.__logger.debug("reset Player")
        self.__playerstatus=0
        self.__currentfile=""
        self.__paused=False
        self.__process=None
        
    def poll(self):
        self.__logger.debug("polling")
        if(self.__process is not None):
            self.__logger.debug("process is not none")
            self.__process.poll()
            if(self.__process.returncode is not None):
                self.__logger.debug("process ended")
                for line in self.__process.stdout:
                    self.__logger.debug("stdout" + line.decode('utf-8'))
                self.__resetplayer()
                
    
    def send(self, str):
        self.__logger.debug("Player send %s", str)
        self.poll()
        if(self.__process is not None):
            self.__process.stdin.write(bytes(str, 'UTF-8'))
            self.__process.stdin.flush()
            
    def getcmdline(self,file):
        finished_cmdline = self.__playerline + " " + self.__cmdline + " '" + file + "'"
        self.__logger.debug('omxplayer cmdline: ' + finished_cmdline)
        return self.__playerline + " " + self.__cmdline + " '" + file + "'"

    def play(self, file):
        self.poll()
        self.__logger.debug("playing: %s",file)
        if(self.__process is not None):
            self.stop()
            
        line = self.getcmdline(file)
        self.__process = subprocess.Popen(
            shlex.split(line), 
            stdout=subprocess.PIPE, 
            stdin=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            close_fds=True)
        self.__playerstatus=1
        self.__currentfile = file
        self.__paused=False
        
    def pause(self):
        self.poll()
        self.__logger.debug("pause called")
        if(self.__process is not None):
            self.send(self.keymapping['pause'])
            if(self.__playerstatus==1):
                self.__playerstatus=2
            else:
                self.__playerstatus=1
        
    def stop(self):
        self.poll()
        self.__logger.debug("stopping")
        if(self.__process is not None):
            self.send(self.keymapping['quit'])
            try:
                self.__logger.debug("waiting for process to close")
                self.__process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.__logger.debug("timeout occured, killing")
                #self.__process.kill()
                subprocess.Popen(shlex.split("killall omxplayer.bin")).wait() ##quickhack
            self.__resetplayer()
            self.__logger.debug("player stopped")
            
    def volumeUp(self):
        self.poll()
        self.__logger.debug("increase vol")
        if(self.__process is not None):
            self.send(self.keymapping['volume']['up'])
        
    def volumeDown(self):
        self.poll()
        self.__logger.debug("decrease vol")
        if(self.__process is not None):
            self.send(self.keymapping['volume']['down'])
        
    def getDict(self):
        self.poll()
        tempDict={}
        tempDict['activePlayer'] = self.getName()
        tempDict['playerStatus'] = self.__playerstatus
        tempDict['currentFile'] = self.__currentfile
        return tempDict
    
