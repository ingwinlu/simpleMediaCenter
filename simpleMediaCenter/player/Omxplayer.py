from Player import Player
import logging
import subprocess

class Omxplayer(Player):
    __cmdline=""

    def __init__(self, cmdline):
        self.cmdline=cmdline

    def send(self, str):
        raise NotImplementedError

    def play(self):
        raise NotImplementedError
        
    def stop(self):
        raise NotImplementedError

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing Omxplayer")
    