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
        
    def getArray(self):
        if(self.__array is None):
            return None
        temparray = []
        for i in self.__array:
            temparray.append(i.getName())
        return temparray
