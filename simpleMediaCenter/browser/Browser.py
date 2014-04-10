import os
import logging
from interface.Interface import Displayable
from helpers.twitch import *

class Browser(Displayable):
    workingDir = ''
    dirlist = {}
    filelist = {}
    
    def __init__(self, startDirectory):
        self.setWorkingDir(startDirectory)
       
    '''
        Returns a String that can be interpreted by a Player to play a ressource 
        (filePath for omxplayer, channelname for twitchplayer,...)
    '''    
    def getPlayable(self, fileKey):
        raise NotImplementedError
        
    ''' 
        Returns a String that represents a Path (Directory, or menu level)
    '''    
    def getPath(self, pathKey):
        raise NotImplementedError
    
    '''
        Set new Working Dir 
        @ param newWorkingDirKey represents a Key in dirlist
    '''    
    def setWorkingDir(self, newWorkingDirKey):
        raise NotImplementedError
        
    def getWorkingDir(self):
        return self.workingDir
        
    def getPathList(self):
        return self.dirlist
        
    def getFileList(self):
        return self.filelist
        
    def getDict(self):
        tempDict={}
        tempDict['browserWorkingDir'] = self.getWorkingDir()
        tempDict['browserDirs'] = self.getPathList()
        tempDict['browserFiles']= self.getFileList()
        tempDict['activeBrowser'] = self.getName()
        return tempDict
    
    def getName(self):
        return self.__class__.__name__


class FileBrowser(Browser):
    def __init__(self,startDirectory='~'):
        tempDir = os.path.expanduser(startDirectory)
        tempDir = os.path.abspath(tempDir)
        self.dirlist = {
                0 : tempDir
            }
        self.setWorkingDir(0)
    
    def getPlayable(self, fileKey):
        return os.path.join(self.workingDir,self.filelist[fileKey])
        
    def getPath(self, pathKey):
        tempPath = os.path.join(self.workingDir,self.dirlist[pathKey])
        tempPath = os.path.abspath(tempPath)
        return tempPath
      
    def setWorkingDir(self, newWorkingDirID):
        self.workingDir = self.getPath(newWorkingDirID)
        list = os.listdir(self.workingDir)
        
        dirlistcounter=0
        filelistcounter=0
        self.dirlist = {}
        self.filelist = {}
        
        self.dirlist[dirlistcounter] = '.'
        dirlistcounter+=1
        
        self.dirlist[dirlistcounter] = '..'
        dirlistcounter+=1
        
        for entry in list:
            testentry = os.path.join(self.workingDir,entry)
            if(os.path.isfile(testentry)):
                self.filelist[filelistcounter] = entry
                filelistcounter+=1
            else:
                self.dirlist[dirlistcounter] = entry
                dirlistcounter+=1

                
class TwitchBrowser(Browser):
    twitchTV = TwitchTV(logging)

    def __init__(self):
        self.dirlist = {
                0 : '/'
            }
        self.setWorkingDir(0)
        
    def getPlayable(self, fileKey):
        return self.filelist[fileKey]
        
    def getPath(self, pathKey):
        tempPath = self.dirlist[pathKey]
        if(tempPath=='.'):
            tempPath=self.getWorkingDir()
        elif(tempPath=='..'):
            tempPath='/' # needs to be refineda
        return tempPath
    
    def setWorkingDir(self, newWorkingDirID):
        logging.debug('setWorkingDir in TwitchBrowser, ' + newWorkingDir)
        self.workingDir = self.getPath(newWorkingDirID)
        
        dirlistcounter=0
        filelistcounter=0
        self.dirlist = {}
        self.filelist = {}
       
        logging.debug("setWorkingDir, final: " + self.workingDir)

        if (self.workingDir=='/'):
            self.dirlist[dirlistcounter] = 'Featured'
            dirlistcounter+=1
            #self.dirlist[dirlistcounter] = 'Following'
            #dirlistcounter+=1
            return True
        elif (self.workingDir=='Featured'):
            self.dirlist[dirlistcounter] = '.'
            dirlistcounter+=1
        
            self.dirlist[dirlistcounter] = '..'
            dirlistcounter+=1
            
            featured = self.twitchTV.getFeaturedStream()
            for stream in featured:
                self.filelist[filelistcounter] = stream['stream']['channel']['name']
                filelistcounter+=1
            return True  
        else:
            raise NotImplementedError
        return False
    