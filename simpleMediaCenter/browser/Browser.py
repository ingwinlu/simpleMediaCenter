#needs rework, pathing needs to be done via a full path, not just parent dir
#similar to a rest interface would be best 
#/ marks root
#/Games/Game Name/1 could display the first page and so on <- workingDir
'''
>>> path = "/Games/Garry's Mod/1"
>>> path.split('/')
['', 'Games', "Garry's Mod", '1']
>>> sp = path.split('/')
>>> '/'.join(sp)
"/Games/Garry's Mod/1"
>>>

'''

import os
import logging
from simpleMediaCenter.interface.Interface import Displayable


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
        tempDict['browserSearch'] = False
        return tempDict
    
    def getName(self):
        return self.__class__.__name__
        

class Pagination():
    minimum = 0
    offset = 0
    limit = 0
    nextPageString = 'next Page >'
    prevPageString = '< previous Page'

    def __init__(self, startoffset, limit):
        self.offset = startoffset
        self.minimum = startoffset
        self.limit = limit
        
    def increase(self):
        self.offset = self.offset + self.limit
        
    def decrease(self):
        if(self.offset - self.limit >= self.minimum):
            self.offset = self.offset - self.limit
            
    def reset(self):
        self.offset = self.minimum


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
        return ['Omxplayer', 'MPlayer']
      
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
    pagination = None
    twitchTV = None
    username = None
    
    def __init__(self, username=None):
        from simpleMediaCenter.helpers.twitch import TwitchTV
        self.twitchTV = TwitchTV(self.__logger)
        self.pagination = Pagination(startoffset=0,limit=10)
        
        self.username = username
        self.dirlist = {
                0 : '.'
            }
        self.setWorkingDir(0)
        
    def getPlayable(self, fileKey):
        self.__logger.debug('getPlayable:' + self.filelist[fileKey])
        return self.filelist[fileKey]
        
    def splitPath(self, path):# take away root / and split by '/', return empty array if on root
        if(path=='/'):
            return []
        if(path==''):
            return []
        return path[1:].split('/')
        
    def buildPath(self, patharray):
        return '/' + '/'.join(patharray)
       
    '''
        returns a split path array 
        >>> tempPath
        ['menu','submenu']
        ['']
    '''
    def getPath(self, pathKey):
        tempPath = self.dirlist[pathKey]
        oldWorkingDir = self.splitPath(self.getWorkingDir())
        self.__logger.debug("oldWorkingDir: " + self.getWorkingDir())
        self.__logger.debug('getPath, tempPath:' + tempPath)
        if(tempPath=='.'):
            tempPath=oldWorkingDir
        elif(tempPath=='..'):
            if(len(oldWorkingDir)>0): # check if not on top level
                del oldWorkingDir[-1] # delete last element in list
            else:
                oldWorkingDir = []
            tempPath = oldWorkingDir
            self.pagination.reset()
        elif(tempPath==self.pagination.nextPageString):
            self.pagination.increase()
            tempPath=oldWorkingDir
        elif(tempPath==self.pagination.prevPageString):
            self.pagination.decrease()
            tempPath=oldWorkingDir
        else:
            tempPath = oldWorkingDir + [tempPath]
            self.pagination.reset()
        return tempPath

    def getSupportedPlayers(self):
        return ['Twitchplayer']
    
    def setWorkingDir(self, newWorkingDirID):
        self.__logger.debug('setWorkingDir id: ' + repr(newWorkingDirID))
        
        pathArray = self.getPath(newWorkingDirID)
        
        dirlistcounter=0
        filelistcounter=0
        self.dirlist = {}
        self.filelist = {}
       
        self.__logger.debug("setWorkingDir, | seperated: " + "|".join(pathArray))

        '''
            parse every element of path array to find destination
        '''
        if (len(pathArray)==0):
            self.dirlist[dirlistcounter] = 'Featured'
            dirlistcounter+=1
            self.dirlist[dirlistcounter] = 'Channels'
            dirlistcounter+=10
            self.dirlist[dirlistcounter] = 'Games'
            dirlistcounter+=1
            self.dirlist[dirlistcounter] = 'Following'
            dirlistcounter+=1
            
        elif (len(pathArray)>=1):
            if (pathArray[0]=='Featured'):
                self.dirlist[dirlistcounter] = '.'
                dirlistcounter+=1
            
                self.dirlist[dirlistcounter] = '..'
                dirlistcounter+=1
                
                featured = self.twitchTV.getFeaturedStream()
                for stream in featured:
                    self.filelist[filelistcounter] = stream['stream']['channel']['name']
                    filelistcounter+=1
                    
            elif (pathArray[0]=='Channels'):
                if(len(pathArray)==1):
                    self.dirlist[dirlistcounter] = '.'
                    dirlistcounter+=1
                
                    self.dirlist[dirlistcounter] = '..'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.prevPageString
                    dirlistcounter+=1
                    
                    self.__logger.debug('offset:' + str(self.pagination.offset) + ' limit:' + str(self.pagination.limit))
                    channels = self.twitchTV.getChannels(offset=self.pagination.offset, limit=self.pagination.limit)
                    for channel in channels:
                        self.filelist[filelistcounter] = channel['channel']['name']
                        filelistcounter+=1
                    self.dirlist[dirlistcounter] = self.pagination.nextPageString
                    dirlistcounter+=1
                else:
                    self.__logger.critical('no suiting menu found workingDir: ' + "|".join(self.workingDir))
                    raise NotImplementedError
            elif (pathArray[0]=='Games'):
                if(len(pathArray)==1):
                    self.dirlist[dirlistcounter] = '.'
                    dirlistcounter+=1
                
                    self.dirlist[dirlistcounter] = '..'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.prevPageString
                    dirlistcounter+=1
                    
                    self.__logger.debug('offset:' + str(self.pagination.offset) + ' limit:' + str(self.pagination.limit))
                    games = self.twitchTV.getGames(offset=self.pagination.offset, limit=self.pagination.limit)
                    for game in games:
                        self.dirlist[dirlistcounter] = game['game']['name']
                        dirlistcounter+=1
                    self.dirlist[dirlistcounter] = self.pagination.nextPageString
                    dirlistcounter+=1
                elif(len(pathArray)==2):
                    self.__logger.debug("list channels which play game: " + pathArray[1])
                    
                    self.dirlist[dirlistcounter] = '.'
                    dirlistcounter+=1
                
                    self.dirlist[dirlistcounter] = '..'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.prevPageString
                    dirlistcounter+=1
                    
                    gamestreams = self.twitchTV.getGameStreams(gameName=pathArray[1], offset=self.pagination.offset, limit=self.pagination.limit)
                    for stream in gamestreams:
                        self.filelist[filelistcounter] = stream['channel']['name']
                        filelistcounter+=1
                        
                    self.dirlist[dirlistcounter] = self.pagination.nextPageString
                    dirlistcounter+=1
                
            elif (pathArray[0]=='Following'):
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

            else:
                self.__logger.critical('no suiting menu found workingDir: ' + "|".join(self.workingDir))
                raise NotImplementedError
            
        
        self.workingDir = self.buildPath(pathArray)
        self.__logger.debug("setWorkingDir to: " + self.workingDir)

        
    def setUsername(self, username):
        self.username = username
        
    def getName(self):
        if(self.username is None):
            return self.__class__.__name__
        return self.__class__.__name__ + " user: " + self.username
    
    
class YoutubeBrowser(Browser):
    __logger=logging.getLogger(__name__)
    favorites = []
    pagination = None
    urllist = {}
    yt = None

    def __init__(self):
        from simpleMediaCenter.helpers.youtube import Youtube
        self.yt = Youtube()
        self.pagination = Pagination(startoffset=1,limit=10)
        self.dirlist = {
                0 : '.'
            }
        self.setWorkingDir(0)
    
    def getPlayable(self, fileKey):
        return self.urllist[fileKey]
        
    def getPath(self, pathKey):
        tempPath = self.dirlist[pathKey]
        oldWorkingDir = self.splitPath(self.getWorkingDir())
        self.__logger.debug("oldWorkingDir: " + self.getWorkingDir())
        self.__logger.debug('getPath, tempPath:' + tempPath)
        if(tempPath=='.'):
            tempPath=oldWorkingDir
        elif(tempPath=='..'):
            if(len(oldWorkingDir)>0): # check if not on top level
                del oldWorkingDir[-1] # delete last element in list
            else:
                oldWorkingDir = []
            tempPath = oldWorkingDir
            self.pagination.reset()
        elif(tempPath==self.pagination.nextPageString):
            self.pagination.increase()
            tempPath=oldWorkingDir
        elif(tempPath==self.pagination.prevPageString):
            self.pagination.decrease()
            tempPath=oldWorkingDir
        elif(tempPath=='/'):
            tempPath = []
        else:
            tempPath = oldWorkingDir + [tempPath]
            self.pagination.reset()
        return tempPath

    def getSupportedPlayers(self):
        return ['Youtubeplayer']
        
    def splitPath(self, path):# take away root / and split by '/', return empty array if on root
        if(path=='/'):
            return []
        if(path==''):
            return []
        return path[1:].split('/')
        
    def buildPath(self, patharray):
        return '/' + '/'.join(patharray)
    
    def setWorkingDir(self, newWorkingDirID, search=None):
        self.__logger.debug('setWorkingDir in YoutubeBrowser, ' + repr(newWorkingDirID))
        if(search==None):
            pathArray = self.getPath(newWorkingDirID)
        else:
            pathArray = ['search',search,newWorkingDirID]
        
        dirlistcounter=0
        filelistcounter=0
        self.dirlist = {}
        self.filelist = {}
        self.urllist = {}
       
       
       
        self.__logger.debug("setWorkingDir, final: " + self.workingDir)
        
        if (len(pathArray)==0):
            self.dirlist[dirlistcounter] = 'Favorites' #TODO 
            dirlistcounter+=1
        
        elif (len(pathArray)>=1):
            if (pathArray[0]=='Favorites'):
                if(len(pathArray)==1):
                    self.dirlist[dirlistcounter] = '..'
                    dirlistcounter+=1
                    
                    for fav in self.favorites:
                        self.dirlist[dirlistcounter] = fav
                        dirlistcounter+=1

                elif(len(pathArray)==2):
                    self.dirlist[dirlistcounter] = '.'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = '..'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.prevPageString
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.nextPageString
                    dirlistcounter+=1
                    
                    self.__logger.debug('getting videolist')
                    videos = self.yt.listChannelVideos(pathArray[1], offset=self.pagination.offset, limit=self.pagination.limit)
                    self.__logger.debug('searching videolist')
                    for video in videos.findall('Atom:entry', namespaces=self.yt.NAMESPACES):
                        self.urllist[filelistcounter] = video.find(
                            ".//Atom:link[@rel='alternate']", 
                            namespaces=self.yt.NAMESPACES).get('href')
                        self.filelist[filelistcounter] = video.find(
                            'Atom:title',
                            namespaces=self.yt.NAMESPACES).text
                        filelistcounter+=1
                else:
                    self.__logger.critical('no suiting menu found workingDir: ' + "|".join(self.workingDir))
                    raise NotImplementedError

            elif (pathArray[0]=='search'):
                if(len(pathArray)==3):
                    self.__logger.debug("search for " + pathArray[1] + " " + pathArray[2])
                    self.dirlist[dirlistcounter] = '.'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = '/'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.prevPageString
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.nextPageString
                    dirlistcounter+=1
                    
                    if(pathArray[1]=='File'):                    
                        videos = self.yt.searchVideo(pathArray[2], offset=self.pagination.offset, limit=self.pagination.limit)
                        for video in videos.findall('Atom:entry', namespaces=self.yt.NAMESPACES):
                            self.urllist[filelistcounter] = video.find(
                                ".//Atom:link[@rel='alternate']", 
                                namespaces=self.yt.NAMESPACES).get('href')
                            title = video.find('Atom:title',namespaces=self.yt.NAMESPACES).text
                            title = title + " - Channel:" + video.find('Atom:author/Atom:name',namespaces=self.yt.NAMESPACES).text
                            self.filelist[filelistcounter] = title
                            filelistcounter+=1
               
                    elif (pathArray[1]=='Dir'):    
                        channels = self.yt.searchChannel(pathArray[2], offset=self.pagination.offset, limit=self.pagination.limit)
                        for channel in channels.findall('Atom:entry', namespaces=self.yt.NAMESPACES):
                            statistics = channel.find('yt:channelStatistics', namespaces=self.yt.NAMESPACES).attrib
                            authorName = channel.find('Atom:author/Atom:name',namespaces=self.yt.NAMESPACES).text
                            authorUri = channel.find('Atom:author/Atom:uri',namespaces=self.yt.NAMESPACES).text
                            userId = channel.find('Atom:author/yt:userId',namespaces=self.yt.NAMESPACES).text
                            authorChannel = authorUri.split("/")[-1]
                            if(userId==authorChannel):#skip if channel name not set
                                continue 
                            else:
                                title = authorChannel
                                self.dirlist[dirlistcounter] = title
                                dirlistcounter+=1
                    else:
                        self.__logger.critical('no suiting menu found workingDir: ' + "|".join(self.workingDir))
                        raise NotImplementedError
                elif(len(pathArray)==4):
                    self.__logger.info('getting videolist for ' + pathArray[-1])
                    self.dirlist[dirlistcounter] = '.'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = '..'
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.prevPageString
                    dirlistcounter+=1
                    
                    self.dirlist[dirlistcounter] = self.pagination.nextPageString
                    dirlistcounter+=1
                    
                    self.__logger.debug('getting videolist')
                    videos = self.yt.listChannelVideos(pathArray[-1], offset=self.pagination.offset, limit=self.pagination.limit)
                    self.__logger.debug('searching videolist')
                    for video in videos.findall('Atom:entry', namespaces=self.yt.NAMESPACES):
                        self.urllist[filelistcounter] = video.find(
                            ".//Atom:link[@rel='alternate']", 
                            namespaces=self.yt.NAMESPACES).get('href')
                        self.filelist[filelistcounter] = video.find(
                            'Atom:title',
                            namespaces=self.yt.NAMESPACES).text
                        filelistcounter+=1
                else:
                    self.__logger.critical('no suiting menu found workingDir: ' + "|".join(self.workingDir))
                    raise NotImplementedError
            else:
                self.__logger.critical('no suiting menu found workingDir: ' + "|".join(self.workingDir))
                raise NotImplementedError
        else:
            self.__logger.critical('no suiting menu found workingDir: ' + "|".join(self.workingDir))
            raise NotImplementedError
                
            
        self.workingDir = self.buildPath(pathArray)
        self.__logger.debug("setWorkingDir to: " + self.workingDir)
        
    def addFavorite(self, newFavorite):
        self.favorites.append(newFavorite)
       
    def getDict(self):
        tempDict=super().getDict()
        tempDict['browserSearch'] = True
        return tempDict