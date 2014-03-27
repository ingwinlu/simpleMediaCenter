import os
import logging
from Playlist import Playlist
from collections import deque

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
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # test subclass
    logging.debug("creating FiFo object")
    fifo = FiFo()
    logging.debug("adding file")
    fifo.add('testfile.mp3')
    fifo.add('testfile2.mp3')
    logging.debug("getting file")
    logging.debug(fifo.getNext())
    logging.debug(fifo.getNext())
    