from interface.Interface import Interface, ExceptionDisplayHandler
from helpers.twitch import TwitchException
from tg import expose, TGController, AppConfig, redirect, config
from wsgiref.simple_server import make_server
import os
import jinja2
import logging
import json

class WebController(TGController):  
    playerList=None
    playlistList=None
    browserList=None
    statusDict=None
    exceptionDisplayHandler=None

    def __init__(self, playerList=None, playlistList=None, browserList=None ):
        logging.debug("WebInterface init")
        self.playerList=playerList
        self.browserList=browserList
        self.playlistList=playlistList
        self.exceptionDisplayHandler=ExceptionDisplayHandler()
        self.statusDict = {
            'playerArray'  : self.playerList.getArray(),
            'playlistArray'  : self.playlistList.getArray(),
            'browserArray'  : self.browserList.getArray(),
            }
            
    def updateStatus(self):
        #logging.debug("updateStatus")
        if(self.playerList.getActive() is not None):
            self.statusDict.update(self.playerList.getActive().getDict())
        if(self.playlistList.getActive() is not None):
            self.statusDict.update(self.playlistList.getActive().getDict())
        if(self.browserList.getActive() is not None):
            self.statusDict.update(self.browserList.getActive().getDict())
        if(self.exceptionDisplayHandler is not None):
            self.statusDict.update(self.exceptionDisplayHandler.getDict())
            
        
    def parseID(self, id):
        id = int(id)
        return id
    
    #index Page
    @expose('index.html')
    def index(self):
        self.updateStatus()
        logging.debug(self.statusDict)
        return self.statusDict
        
    
    #controls
    @expose()
    def play(self, id=None):
        try:
            id = self.parseID(id)
            logging.debug("trying to play %s" ,self.browserList.getActive().getPlayable(id))
            # TODO implement player select according to playlist.getSupportedPlayers()
            logging.debug("searching for compatible Browser") 
            for supportedPlayer in self.browserList.getActive().getSupportedPlayers():
                playerid = self.playerList.getIDfromName(supportedPlayer)
                if (playerid is not None):
                    break
            if (playerid is None):
                raise Exception('no compatible player found in supportedPlayers')
            self.playerList.getActive().stop()
            self.playerList.setActive(playerid)
            self.playerList.getActive().play(self.browserList.getActive().getPlayable(id))
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in play: ' + repr(e))

        redirect("/")
    
    @expose()
    def stop(self):
        logging.debug("stop called")
        self.playerList.getActive().stop()
        redirect("/")
        
    @expose()
    def pause(self):
        logging.debug("pause called")
        self.playerList.getActive().pause()
        redirect("/")
        
    @expose()
    def change(self,id=None):
        try:
            id = self.parseID(id)
            logging.debug("change called %s", id)
            self.browserList.getActive().setWorkingDir(id)
        except KeyError as e:
            self.exceptionDisplayHandler.setException('KeyError','Passed id not in range: ' + repr(e))
        except TwitchException as e:
            self.exceptionDisplayHandler.setException('TwitchException',repr(e))
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in change: ' + repr(e))
        redirect("/")
        
    @expose()
    def selectPlayer(self, id=None):
        try:
            id = self.parseID(id)
            self.playerList.getActive().stop()
            self.playerList.setActive(id)
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in selectPlayer: ' + repr(e))
        redirect("/")
    
    @expose()
    def selectBrowser(self, id=None):
        try:
            id = self.parseID(id)
            self.browserList.setActive(id)
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in selectBrowser: ' + repr(e))
        redirect("/")
        
    @expose()
    def selectPlaylist(self, id=None):
        try:
            id = self.parseID(id)
            self.playlistList.setActive(id)
        except Exception as e:
            self.exceptionDisplayHandler.setException('Exception','Unhandled Exception in selectPlaylist: ' + repr(e))
        redirect("/")
        
    @expose()
    def clearException(self):
        self.exceptionDisplayHandler.clearException()
        redirect("/")
        
    #ajax interface
    @expose()
    def status(self,_=None):
        self.updateStatus()
        return json.dumps(self.statusDict)
        


class WebInterface(Interface):
    config=None
    httpd=None
    application=None
    keep_running=True
    player=None
    controller=None
    
    def __init__(self, templatePath, staticPath, controller):
        logging.debug("create WebInterface Instance")
  
        logging.debug("setup TurboGears2")
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
        
        self.application = self.config.make_wsgi_app()
        self.httpd = make_server('', 8080, self.application)
        self.httpd.timeout = 5
    
    def run(self):
        logging.debug("start Webserver")
        while(self.keep_running):
            logging.debug("start serve_forever()")
            try:
                #self.httpd.handle_request()
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                self.shutdown()
                
        
    def shutdown(self):
        logging.info("init shutdown")
        self.keep_running=False
        
  