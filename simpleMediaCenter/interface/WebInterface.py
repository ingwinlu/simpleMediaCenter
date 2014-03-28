from Interface import Interface
from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server
import os
import jinja2
import logging


class RootController(TGController):  
    def __init__(self):
        pass
    
    @expose('index.html')
    def index(self):
        templateVars = { "title" : "Test Example",
                        "description" : "A simple inquiry of function.",
                        "files" : ["file1", "file2","file3"]}
        return templateVars

class WebInterface(Interface):
    config=None
    httpd=None
    application=None
    keep_running=True

    def __init__(self):
        logging.debug("create WebInterface Instance")

        ##temporary
        logging.debug("setup TurboGears2")
        self.config = AppConfig(minimal=True, root_controller=RootController())
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
    webinterface = WebInterface();
    