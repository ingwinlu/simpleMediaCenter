from simpleMediaCenter.interface.Interface import Displayable

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
        
    def volumeUp(self):
        raise NotImplementedError
        
    def volumeDown(self):
        raise NotImplementedError
    
    def getName(self):
        return self.__class__.__name__

'''    
overwrite init and check for arraycontent for type=Player
class PlayerList(InterfaceListable):
    self.__playerArray=None
    __currentPlayer=0

    def __init__(self, playerArray):
        if(playerArray is None):
            raise AttributeError('playerArray is not allowed to be None')
            
        if(len(playerArray)<=0):
            raise AttributeError('playerArray is not allowed to be of size 0 or smaller')
            
        self.__PlayerArray=playerArray
        self.__currentPlayer=0
        
    def setActive(self, id):
        if(0<=id<len(self.__playerArray)):
        
        else:
            raise AttributeError('id not in range of playerArray with size ' + len(self.__playerArray))
            
    def getActive(self):
        return self.__playerArray[self.__currentPlayer]
'''