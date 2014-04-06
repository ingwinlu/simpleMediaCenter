import os
import logging
from interface.Interface import Displayable

class FileBrowser(Displayable):
    workingDir=''
    dirlist = {}
    filelist = {}

    def __init__(self,startDirectory='~'):
        self.setWorkingDir(os.path.expanduser(startDirectory))
        
    def getDirList(self):
        return self.dirlist
        
    def getDirListPath(self, key):
        if(key in self.dirlist):
            return os.path.join(self.workingDir,self.dirlist[key])
        return None
    
    def getFileList(self):
        return self.filelist
        
    def getFileListPath(self, key):
        if(key in self.filelist):
            return os.path.join(self.workingDir,self.filelist[key])
        return None
        
    def getWorkingDir(self):
        return self.workingDir
        
    def getPath(list,key):
        return os.path.join(self.workingDir,list[key])
        
    def setWorkingDir(self, newWorkingDir):
        if(os.path.isdir(newWorkingDir)):
            dirlistcounter=0
            filelistcounter=0
            self.dirlist = {}
            self.filelist = {}
        
            self.workingDir = os.path.abspath(newWorkingDir)
            list = os.listdir(self.workingDir)

            self.dirlist[dirlistcounter] = '.'
            dirlistcounter+=1
            
            self.dirlist[dirlistcounter] = '..'
            dirlistcounter+=1
            
            for entry in list:
                testentry = os.path.join(self.workingDir,entry)
                #logging.debug(testentry + " " + str(os.path.isfile(testentry)))
                if(os.path.isfile(testentry)):
                    self.filelist[filelistcounter] = entry
                    filelistcounter+=1
                else:
                    self.dirlist[dirlistcounter] = entry
                    dirlistcounter+=1
        else:
            return False
        return True
        
    def getDict(self):
        tempDict={}
        tempDict['browserWorkingDir'] = self.workingDir
        tempDict['browserDirs'] = self.dirlist
        tempDict['browserFiles']= self.filelist
        tempDict['activeBrowser'] = self.getName()
        return tempDict
    
    def getName(self):
        return self.__class__.__name__
