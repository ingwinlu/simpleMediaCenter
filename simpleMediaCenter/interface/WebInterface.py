from interface.Interface import Interface
from tg import expose, TGController, AppConfig, redirect
from wsgiref.simple_server import make_server
import os
import jinja2
import logging


class RootController(TGController):  
    player=None

    def __init__(self, player=None):
        logging.debug("WebInterface init")
        self.player=player
    
    @expose('index.html')
    def index(self):
        templateVars = { "title" : "Test Example",
                        "description" : "A simple inquiry of function.",
                        "files" : ["file1", "file2","file3"]}
        return templateVars
        
        
    
    #controls
    @expose()
    def play(self):
        logging.debug("play called")
        if(player is not None):
            player.play()
        redirect("/")
    
    @expose()
    def stop(self):
        logging.debug("stop called")
        if(player is not None):
            player.stop()
        redirect("/")
    

class WebInterface(Interface):
    config=None
    httpd=None
    application=None
    keep_running=True
    player=None
    
    def __init__(self, player=None):
        self.player=player
    
        logging.debug("create WebInterface Instance")

        ##temporary
        logging.debug("setup TurboGears2")
        self.config = AppConfig(minimal=True, root_controller=RootController(player=self.player))
        #jinja stuff
        self.config.renderers.append('jinja')
        self.config.default_renderer = 'jinja'
        self.config.use_dotted_templatenames = False
        #self.config.paths['templates'] = os.path.abspath('./templates/') # how to move templates in to a subdirectory?
        #statics
        self.config.serve_static = True
        self.config.paths['static_files'] = 'static'
        self.application = self.config.make_wsgi_app()
        self.httpd = make_server('', 8080, self.application)
        self.httpd.timeout = 5
    
    def run(self):
        logging.debug("start Webserver")
        while(self.keep_running):
            logging.debug("wait for request")
            self.httpd.handle_request()
        ##temporary end
        
    def shutdown(self):
        self.keep_running=False
        

        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing WebInterface")
    webinterface = WebInterface()
    webinterface.run()
    