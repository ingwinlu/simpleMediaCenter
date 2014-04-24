import os
import logging
from interface.Interface import Displayable


class Browser(Displayable):
    workingDir = ''
    parentDir = ''
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
        get supported Players, first match gets used to play file returned by getPlayable
    '''
    def getSupportedPlayers(self):
        raise NotImplementedError
    
    '''
        Set new Working Dir 
        @param newWorkingDirKey represents a Key in dirlist
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
    __logger=logging.getLogger(__name__)

    def __init__(self,startDirectory='~'):
        self.__logger.debug('init')
        tempDir = os.path.expanduser(startDirectory)
        tempDir = os.path.abspath(tempDir)
        self.dirlist = {
                0 : tempDir
            }
        self.setWorkingDir(0)
    
    def getPlayable(self, fileKey):
        temp = os.path.join(self.workingDir,self.filelist[fileKey])
        self.__logger.debug('getPlayable:' + temp)
        return temp
        
    def getPath(self, pathKey):
        tempPath = os.path.join(self.workingDir,self.dirlist[pathKey])
        tempPath = os.path.abspath(tempPath)
        self.__logger.debug('getPath:' + tempPath)
        return tempPath
      
    def getSupportedPlayers(self):
        return ['Omxplayer']
      
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
    __logger=logging.getLogger(__name__)
    offset=0
    limit=10
    twitchTV = None
    username = None

    def __init__(self, username=None):
        from helpers.twitch import TwitchTV
        self.twitchTV = TwitchTV(self.__logger)
        
        self.username = username
        self.dirlist = {
                0 : '/'
            }
        self.setWorkingDir(0)
        
    def getPlayable(self, fileKey):
        self.__logger.debug('getPlayable:' + self.filelist[fileKey])
        return self.filelist[fileKey]
       
    def getPath(self, pathKey):
        tempPath = self.dirlist[pathKey]
        self.__logger.debug('getPath, tempPath:' + tempPath)
        if(tempPath=='.'):
            tempPath=self.getWorkingDir()
        elif(tempPath=='..'):
            self.offset=0
            tempPath=self.parentDir
        elif(tempPath=='next Page >'):
            self.offset=self.offset+self.limit
            tempPath=self.getWorkingDir()
        elif(tempPath=='< previous Page'):
            if(self.offset-self.limit>=0):
                self.offset=self.offset-self.limit
            tempPath=self.getWorkingDir()
        self.__logger.debug('getPath, final, tempPath:' + tempPath)
        return tempPath

    def getSupportedPlayers(self):
        return ['Twitchplayer']
    
    def setWorkingDir(self, newWorkingDirID):
        self.__logger.debug('setWorkingDir in TwitchBrowser, ' + str(newWorkingDirID))

        self.workingDir = self.getPath(newWorkingDirID)
        
        dirlistcounter=0
        filelistcounter=0
        self.dirlist = {}
        self.filelist = {}
       
        self.__logger.debug("setWorkingDir, final: " + self.workingDir)

        if (self.workingDir=='/'):
            self.parentDir = '/'
            
            self.dirlist[dirlistcounter] = 'Featured'
            dirlistcounter+=1
            self.dirlist[dirlistcounter] = 'Games'
            dirlistcounter+=1
            self.dirlist[dirlistcounter] = 'Following'
            dirlistcounter+=1
            return True
        elif (self.workingDir=='Featured'):
            self.parentDir = '/'
        
            self.dirlist[dirlistcounter] = '.'
            dirlistcounter+=1
        
            self.dirlist[dirlistcounter] = '..'
            dirlistcounter+=1
            
            featured = self.twitchTV.getFeaturedStream()
            for stream in featured:
                self.filelist[filelistcounter] = stream['stream']['channel']['name']
                filelistcounter+=1
            return True  
        elif (self.workingDir=='Games'):
            self.parentDir = '/'
            
            self.dirlist[dirlistcounter] = '.'
            dirlistcounter+=1
        
            self.dirlist[dirlistcounter] = '..'
            dirlistcounter+=1
            
            self.dirlist[dirlistcounter] = '< previous Page'
            dirlistcounter+=1
            
            self.__logger.debug('offset:' + str(self.offset) + ' limit:' + str(self.limit))
            games = self.twitchTV.getGames(offset=self.offset, limit=self.limit)
            for game in games:
                self.dirlist[dirlistcounter] = game['game']['name']
                dirlistcounter+=1
            self.dirlist[dirlistcounter] = 'next Page >'
            dirlistcounter+=1
            return True  
        elif (self.workingDir=='Following'):
            self.parentDir = '/'
        
            self.dirlist[dirlistcounter] = '.'
            dirlistcounter+=1
        
            self.dirlist[dirlistcounter] = '..'
            dirlistcounter+=1
            
            if(self.username is None):
                return False # temporary workaround if no username is set
            
            following = self.twitchTV.getFollowingStreams(self.username)
            for stream in following['live']:
                self.filelist[filelistcounter] = stream['channel']['name']
                filelistcounter+=1
            return True  
        elif (self.oldWorkingDir=='Games'):
            self.parentDir = '/'
            self.__logger.debug("list channels which play game: " + self.workingDir)
            
            self.dirlist[dirlistcounter] = '.'
            dirlistcounter+=1
        
            self.dirlist[dirlistcounter] = '..'
            dirlistcounter+=1
            
            gamestreams = self.twitchTV.getGameStreams(self.workingDir)
            for stream in gamestreams:
                self.filelist[filelistcounter] = stream['channel']['name']
                filelistcounter+=1
        else:
            raise NotImplementedError
        return False
        
    def setUsername(self, username):
        self.username = username
        
    def getName(self):
        if(self.username is None):
            return self.__class__.__name__
        return self.__class__.__name__ + " user: " + self.username
    
    
class YoutubeBrowser(Browser):
    __logger=logging.getLogger(__name__)
    urllist = {}
    yt = None

    def __init__(self):
        from helpers.youtube import Youtube
        self.yt = Youtube()
        self.dirlist = {
                0 : '/'
            }
        self.setWorkingDir(0)
        
    def getPlayable(self, fileKey):
        return self.urllist[fileKey]
        
    def getPath(self, pathKey):
        tempPath = self.dirlist[pathKey]
        if(tempPath=='.'):
            tempPath=self.getWorkingDir()
        elif(tempPath=='..'):
            tempPath='/' # needs to be refined
        return tempPath

    def getSupportedPlayers(self):
        return ['Youtubeplayer']
    
    def setWorkingDir(self, newWorkingDirID):
        self.__logger.debug('setWorkingDir in YoutubeBrowser, ' + str(newWorkingDirID))
        self.workingDir = self.getPath(newWorkingDirID)
        
        dirlistcounter=0
        filelistcounter=0
        self.dirlist = {}
        self.filelist = {}
        self.urllist = {}
       
        self.__logger.debug("setWorkingDir, final: " + self.workingDir)
        
        if (self.workingDir=='/'):
            self.dirlist[dirlistcounter] = 'MrSuicideSheep' #TODO 
            dirlistcounter+=1
            return 
        elif (self.workingDir=='MrSuicideSheep'):
            self.dirlist[dirlistcounter] = '.'
            dirlistcounter+=1
            
            self.dirlist[dirlistcounter] = '..'
            dirlistcounter+=1
            
            self.__logger.debug('getting videolist')
            videos = self.yt.listChannelVideos('MrSuicideSheep')
            self.__logger.debug('searching videolist')
            for video in videos.findall('Atom:entry', namespaces=self.yt.NAMESPACES):
                self.urllist[filelistcounter] = video.find(
                    ".//Atom:link[@rel='alternate']", 
                    namespaces=self.yt.NAMESPACES).get('href')
                self.filelist[filelistcounter] = video.find(
                    'Atom:title',
                    namespaces=self.yt.NAMESPACES).text
                filelistcounter+=1
            return   
        raise NotImplementedError
        
   