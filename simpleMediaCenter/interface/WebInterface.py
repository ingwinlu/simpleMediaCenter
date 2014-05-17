from simpleMediaCenter.interface.Interface import Interface, ExceptionDisplayHandler
from simpleMediaCenter.helpers.twitch import TwitchException
import simpleMediaCenter.interface.service as service

from tg import expose, TGController, AppConfig, redirect, config
from wsgiref.simple_server import make_server, WSGIServer
from socketserver import ThreadingMixIn
import os
import jinja2
import logging
import json
import threading

class WebController(TGController):  
    __logger=logging.getLogger(__name__)
    statusDict=None
    exceptionDisplayHandler=None
    thread=None

    def __init__(self):
        self.__logger.debug("WebInterface init")
        self.exceptionDisplayHandler=ExceptionDisplayHandler()
        self.statusDict = {
            'playerArray'  : service.playerList.getArray(),
            'playlistArray'  : service.playlistList.getArray(),
            'browserArray'  : service.browserList.getArray(),
            'threadRunning' : 0
            }
            
    def updateStatus(self):
        self.__logger.debug("updateStatus")
        if(service.playerList.getActive() is not None):
            self.statusDict.update(service.playerList.getActive().getDict())
        if(service.playlistList.getActive() is not None):
            self.statusDict.update(service.playlistList.getActive().getDict())
        if(service.browserList.getActive() is not None):
            self.statusDict.update(service.browserList.getActive().getDict())
        if(self.exceptionDisplayHandler is not None):
            self.statusDict.update(self.exceptionDisplayHandler.getDict())
        if(self.thread!=None):
            self.statusDict['threadRunning'] = 1
        else:
            self.statusDict['threadRunning'] = 0
    
    def parseID(self, id):
        id = int(id)
        return id
    
    #index Page
    @expose('index.html')
    def index(self):
        self.__logger.debug('index called')
        if(self.thread!=None): #wait for thread before building page
            self.thread.join()
            self.thread=None
        self.updateStatus()
        self.__logger.debug(self.statusDict)
        return self.statusDict
       
    '''
    #loading parking Page
    @expose('loading.html')
    def loading(self):
        self.__logger.debug('loading called')
        redirect("/")
    '''
    
    #controls
    '''
        play file, auto select suitable player
    '''
    @expose()
    def play(self, id=None):
        try:
            id = self.parseID(id)
            self.thread = threading.Thread(target=service.play,args=(id,))
            self.thread.start()
        except Exception as e:
            self.exceptionDisplayHandler.setException(
                'Exception',
                'Unhandled Exception in play: ' + repr(e))
        redirect("/")
    
    '''
        stop playback
    '''
    @expose()
    def stop(self):
        try:
            service.stop()
        except Exception as e:
            self.exceptionDisplayHandler.setException(
                'Exception',
                'Unhandled Exception in stop: ' + repr(e))
        redirect("/")
      
    '''
        pause playback
    '''
    @expose()
    def pause(self):
        try:
            service.pause()
        except Exception as e:
            self.exceptionDisplayHandler.setException(
                'Exception',
                'Unhandled Exception in pause: ' + repr(e))
        redirect("/")
        
    '''
        reduces player volume
    '''
    @expose()
    def volumedown(self):
        try:
            service.volume_down()
        except Exception as e:
            self.exceptionDisplayHandler.setException(
                'Exception',
                'Unhandled Exception in volumedown: ' + repr(e))
        redirect("/")
        
    '''
        increases player volume
    '''
    @expose()
    def volumeup(self):
        try:
            service.volume_up()
        except Exception as e:
            self.exceptionDisplayHandler.setException(
                'Exception',
                'Unhandled Exception in volumeup: ' + repr(e))
        redirect("/")
        
    '''
        change working directory
    '''
    @expose()
    def change(self,id=None):
        try:
            id = self.parseID(id)
            self.thread = threading.Thread(target=service.change,args=(id,))
            self.thread.start()
        except KeyError as e:
            self.exceptionDisplayHandler.setException('KeyError','Passed id not in range: ' + repr(e))
        except TwitchException as e:
            self.exceptionDisplayHandler.setException('TwitchException',repr(e))
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in change: ' + repr(e))
        redirect("/")
        
        
    '''
        search something which is then treated as a playable file
    '''    
    @expose()
    def searchFile(self, search):
        try:
            self.thread = threading.Thread(target=service.search_file,args=(search,))
            self.thread.start()
        except Exception as e:
            self.exceptionDisplayHandler.setException(
                'Exception',
                'Unhandled Exception in searchFile: ' + repr(e))
        redirect("/")
        
    '''
        search something which is then treated as a browsable directory
    '''
    @expose()
    def searchDir(self, search):
        try:
            self.thread = threading.Thread(target=service.search_dir,args=(search,))
            self.thread.start()
        except Exception as e:
            self.exceptionDisplayHandler.setException(
                'Exception',
                'Unhandled Exception in searchFile: ' + repr(e))
        redirect("/")
      
    '''
        DEPRECATED: is now done automatically
        selects player via dropdown menu
    '''      
    @expose()
    def selectPlayer(self, id=None):
        try:
            id = self.parseID(id)
            service.select_player(id)
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in selectPlayer: ' + repr(e))
        redirect("/")
        
    '''
        selects browser via dropdown menu
    '''
    @expose()
    def selectBrowser(self, id=None):
        try:
            id = self.parseID(id)
            service.select_browser(id)
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in selectBrowser: ' + repr(e))
        redirect("/")
        
    '''
        selects playlist via dropdown menu
    '''
    @expose()
    def selectPlaylist(self, id=None):
        try:
            id = self.parseID(id)
            service.select_playlist(id)
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in selectPlaylist: ' + repr(e))
        redirect("/")
        
    '''
        clears an exception from memory
    '''
    @expose()
    def clearException(self):
        self.exceptionDisplayHandler.clearException()
        redirect("/")
        
    #ajax interface
    @expose()
    def status(self,_=None):
        self.updateStatus()
        return json.dumps(self.statusDict)

        
class ThreadingWSGIServer(ThreadingMixIn, WSGIServer): 
    pass

class WebInterface(Interface):
    __logger=logging.getLogger(__name__)
    config=None
    httpd=None
    application=None
    keep_running=True
    player=None
    controller=None
    
    def __init__(self, templatePath, staticPath, port, controller):
        self.__logger.debug("create WebInterface Instance")
  
        self.__logger.debug("setup TurboGears2")
        self.controller = controller
        self.config = AppConfig(minimal=True, root_controller=self.controller)
        
        #jinja stuff
        self.config.renderers.append('jinja')
        self.config.default_renderer = 'jinja'
        self.config.use_dotted_templatenames = False
        self.config.paths['templates'] = [templatePath]
        
        #statics
        self.config.serve_static = True
        self.config.paths['static_files'] = staticPath
        
        #make wsgi_app
        self.application = self.config.make_wsgi_app()
        
        #make wsgi_server
        self.httpd = make_server('', port, self.application, ThreadingWSGIServer)
        self.httpd.timeout = 5
    
    def run(self):
        self.__logger.debug("run")
        while(self.keep_running):
            self.__logger.info("listening for Requests")
            try:
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                self.shutdown()
    
    def shutdown(self):
        self.__logger.info("init shutdown")
        service.stop()
        self.keep_running=False
