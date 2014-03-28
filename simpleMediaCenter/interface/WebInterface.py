from Interface import Interface
from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server
import jinja2
import logging


class RootController(TGController):
    
    def __init__(self):
        pass
    
    @expose('index.html')
    def index(self):
        templateVars = { "title" : "Test Example",
                        "description" : "A simple inquiry of function." }
        return templateVars

class WebInterface(Interface):
    config=None
    httpd=None
    application=None

    def __init__(self):
        logging.debug("create WebInterface Instance")

        ##temporary
        logging.debug("setup TurboGears2")
        self.config = AppConfig(minimal=True, root_controller=RootController())
        self.config.renderers.append('jinja')
        self.config.default_renderer = 'jinja'
        self.config.use_dotted_templatenames = False
        self.application = self.config.make_wsgi_app()
        self.httpd = make_server('', 8080, self.application)
        logging.debug("start Webserver")
        self.httpd.serve_forever()
        ##temporary end
        
    def shutdown(self):
        pass
        

                
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing WebInterface")
    webinterface = WebInterface();
    