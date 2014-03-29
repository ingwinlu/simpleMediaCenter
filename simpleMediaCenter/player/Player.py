from interface.Interface import Displayable

class Player(Displayable):

    def __init__(self, cmdline):
        raise NotImplementedError

    def send(self, str):
        raise NotImplementedError

    def play(self, file):
        raise NotImplementedError
        
    def pause(self):
        raise NotImplementedError
        
    def stop(self):
        raise NotImplementedError
