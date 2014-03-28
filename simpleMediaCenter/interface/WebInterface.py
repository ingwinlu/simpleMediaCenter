from interface.Interface import Interface
from tg import expose, TGController, AppConfig, redirect, config
from wsgiref.simple_server import make_server
from fileCrawler.FileCrawler import FileCrawler
import os
import jinja2
import logging

class RootController(TGController):  
    player=None
    crawler=None

    def __init__(self, player=None):
        logging.debug("WebInterface init")
        self.player=player
        self.crawler=FileCrawler()
    
    @expose('index.html')
    def index(self):
        logging.debug("workingDir: %s", self.crawler.getWorkingDir())
        logging.debug("dirs: %s", self.crawler.getDirList())
        logging.debug("files: %s", self.crawler.getFileList())
        templateVars = { "workingDir" : self.crawler.getWorkingDir(),
                         "dirs"       : self.crawler.getDirList(),
                         "files"      : self.crawler.getFileList()}
        return templateVars
        
        
    
    #controls
    @expose()
    def play(self, id=None):
        logging.debug("play called %s", id)
        if((self.player is None) or (id is None)):
            logging.info("play failed")
            redirect("/")
        try:
            id = int(id)
        except:
            logging.error("could not convert id")
            redirect("/")
        
        if(id in self.crawler.getFileList()):
            logging.debug("trying to play %s" ,self.crawler.getFileList()[id])
            self.player.play(self.crawler.getFileListPath(id))

        redirect("/")
    
    @expose()
    def stop(self):
        logging.debug("stop called")
        if(self.player is not None):
            self.player.stop()
        redirect("/")
        
    @expose()
    def change(self,id=None):
        logging.debug("change called %s", id)
        try: 
            id = int(id)
        except:
            logging.error("could not convert id")
            redirect("/")
        if(id in self.crawler.getDirList()):
            logging.debug("trying to change into %s" ,self.crawler.getDirListPath(id))
            self.crawler.setWorkingDir(self.crawler.getDirListPath(id))

        redirect("/")

    

class WebInterface(Interface):
    config=None
    httpd=None
    application=None
    keep_running=True
    player=None
    
    def __init__(self, templatePath='./templates/', staticPath='./static/', player=None,):
        logging.debug("create WebInterface Instance")
        self.player=player
  
        logging.debug("setup TurboGears2")
        self.config = AppConfig(minimal=True, root_controller=RootController(player=self.player))
        
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
            logging.debug("wait for request")
            self.httpd.handle_request()
        
    def shutdown(self):
        self.keep_running=False
        

        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing WebInterface")
    webinterface = WebInterface()
    webinterface.run()
    