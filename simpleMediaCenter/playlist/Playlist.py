import os
import logging
from collections import deque
from simpleMediaCenter.interface.Interface import Displayable

class Playlist(Displayable):
    #list of some sort
    def __init__(self):
        pass

    def add(self, filePath):
        raise NotImplementedError
        
    def getNext(self ):
        raise NotImplementedError

class FiFo(Playlist):
    queue = deque([])
    
    def __init__(self):
        pass

    def add(self, filePath):
        logging.debug("try to add: %s", filePath)
        if(os.path.isfile(filePath)):
            self.queue.append(filePath)
        else:
            raise Exception
        
    def getNext(self):
        logging.debug("getNext called")
        if(len(self.queue) > 0):
            return self.queue.popleft()
        else:
            raise Exception
    
    def getDict(self):
        raise NotImplementedError
            
class Single(Playlist):
    filePath = None
    
    def __init__(self):
        pass
    
    def add(self, filePath):
        self.filePath=filePath
        
    def getNext(self):
        return None
  
    def getDict(self):
        tempDict={}
        tempDict['activePlaylist'] = self.getName()
        tempDict['playlistFiles'] = [self.filePath]
        return tempDict
        
    def getName(self):
        return self.__class__.__name__
        
