from interface.Interface import Interface
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

    def __init__(self, playerList=None, playlistList=None, browserList=None ):
        logging.debug("WebInterface init")
        self.playerList=playerList
        self.browserList=browserList
        self.playlistList=playlistList
        self.statusDict = {
            'playerArray'  : self.playerList.getArray(),
            'playlistArray'  : self.playlistList.getArray(),
            'browserArray'  : self.browserList.getArray()
            }
            
    def updateStatus(self):
        logging.debug("updateStatus")
        self.statusDict.update(self.playerList.getActive().getDict())
        self.statusDict.update(self.playlistList.getActive().getDict())
        self.statusDict.update(self.browserList.getActive().getDict())
    
    #index Page
    @expose('index.html')
    def index(self):
        self.updateStatus()
        logging.debug(self.statusDict)
        return self.statusDict
        
    
    #controls
    @expose()
    def play(self, id=None):
        logging.debug("play called %s", id)
        if(id is None):
            logging.info("play failed")
            redirect("/")
            return
        try:
            id = int(id)
        except:
            logging.error("could not convert id")
        if(id in self.browserList.getActive().getFileList()):
            logging.debug("trying to play %s" ,self.browserList.getActive().getFileList()[id])
            self.playerList.getActive().play(self.browserList.getActive().getFileListPath(id))
        else:
            logging.error("id not in FileList")

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
        if(id is None):
            logging.warning("id is None")
            redirect("/")
            return
        logging.debug("change called %s", id)
        try: 
            id = int(id)
        except:
            logging.error("could not convert id")
        if(id in self.browserList.getActive().getDirList()):
            logging.debug(
                "trying to change into %s" ,
                self.browserList.getActive().getDirListPath(id)
                )
            self.browserList.getActive().setWorkingDir(
                self.browserList.getActive().getDirListPath(id)
                )
        else:
            logging.error("id not in DirList")
        redirect("/")
        
    #TODO implement new change controls
        
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
        
  