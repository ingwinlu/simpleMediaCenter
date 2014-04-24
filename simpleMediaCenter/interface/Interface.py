import logging

class Interface():
    pass
    #no idea what i need to abstract here, need to revisit when adding console interface
    
'''
    provides an interface for objects to be queried by the UI
'''
class Displayable():
    def getDict(self):
        raise NotImplementedError
        
    def getName(self):
        return self.__class__.__name__
        
        
'''
    provides feedback to the user if an exception occurs
'''
class ExceptionDisplayHandler(Displayable):
    __logger=logging.getLogger(__name__)
    __head=""
    __body=""
    __status=0

    def __init__(self):
        pass
        
    '''
        set an Exception that is to be displayed by javascript in a client window
        @param head Header of the Exception
        @body body text of th eException
    '''
    def setException(self, head, body):
        self.__logger.info('setException with head: ' + head + ' and body: ' + body)
        self.__head=head
        self.__body=body
        self.__status=1
        
    '''
        clears the Exception from the System
    '''
    def clearException(self):
        self.__logger.info('clearing Exception')
        self.__head=""
        self.__body=""
        self.__status=0
        
    #@override
    def getDict(self):
        tempDict={}
        tempDict['exceptionStatus'] = self.__status
        tempDict['exceptionTitle'] = self.__head
        tempDict['exceptionBody'] = self.__body
        return tempDict
        
'''
    lists in the interface, for example players/playlists/browsers
'''
class InterfaceListable():
    __array=None
    __current=None

    def __init__(self, array):
        if(array is None):
            raise TypeError('array is not allowed to be None')
            
        if(len(array)<0):
            raise TypeError('array is not allowed to be smaller then 0')
            
        if(len(array)<=0):
            self.__array=None
            self.__current=None
        else:
            self.__array=array
            self.__current=0
        
    def setActive(self, id):
        if(self.__array is None):
            return None
        if(0<=id<len(self.__array)):
            self.__current=id
        else:
            raise TypeError('id not in range of playerArray with size ' + len(self.__array))
            
    def getActive(self):
        if(self.__array is None):
            return None
        return self.__array[self.__current]
        
    def getIDfromName(self, name):
        tempid=0
        for entry in self.getArray():
            if(entry==name):
                return tempid
            else:
                tempid = tempid + 1
        return None
        
    def getArray(self):
        if(self.__array is None):
            return None
        temparray = []
        for i in self.__array:
            temparray.append(i.getName())
        return temparray
