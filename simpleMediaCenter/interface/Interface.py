class Interface():
    pass
    #no idea what i need to abstract here, need to revisit when adding console interface
    
class Displayable():
    def getDict(self):
        raise NotImplementedError
        
    def getName(self):
        raise NotImplementedError
    
class InterfaceListable():
    __array=None
    __current=0

    def __init__(self, array):
        if(array is None):
            raise TypeError('array is not allowed to be None')
            
        if(len(array)<=0):
            raise TypeError('array is not allowed to be of size 0 or smaller')
            
        self.__array=array
        self.__current=0
        
    def setActive(self, id):
        if(0<=id<len(self.__array)):
            self.__current=id
        else:
            raise TypeError('id not in range of playerArray with size ' + len(self.__array))
            
    def getActive(self):
        return self.__array[self.__current]
        
    def getArray(self):
        temparray = []
        for i in self.__array:
            temparray.append(i.getName())
            
        return temparray
