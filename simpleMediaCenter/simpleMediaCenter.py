from interface.WebInterface import WebInterface, WebController
from interface.Interface import InterfaceListable
from player.Omxplayer import Omxplayer
from player.Twitchplayer import Twitchplayer
from player.Youtubeplayer import Youtubeplayer
from browser.Browser import *
from playlist.Playlist import Single
import logging
import os
import configparser

class simpleMediaCenter():
    __logger=logging.getLogger(__name__)
    config_file = os.path.expanduser('~/.simpleMediaCenter-config.ini')
    config = None
    
    '''
        init simpleMediaCenter, parse config
    '''
    def __setDefaultConfig(self, input_config):
        output_config = input_config
        output_config['LOGGING'] =
            {
                'level' : logging.DEBUG
            }
        output_config['WEBINTERFACE'] =
            {
                'templatePath' : os.path.abspath('./interface/templates/'),
                'staticPath' : os.path.abspath('./interface/static/')
            }
            
            
        return output_config
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config = self.__setDefaultConfig(self.config)
        pass
        
    '''
        run a setup media center class
    '''
    def run(self):
        pass
        # save current config to file
        
    
if __name__ == "__main__":
    pass
#config = configparser.ConfigParser()
#config_file = 'simpleMediaCenter-config.ini'
#load config sections over modules

pathToTemplates=os.path.abspath('./interface/templates/')
pathToStatic=os.path.abspath('./interface/static/')

logging.basicConfig(level=logging.DEBUG)

logging.info("creating player objects")
omxplayer = Omxplayer("-o both")
twitchplayer = Twitchplayer("-o both")
youtubeplayer = Youtubeplayer("-o both")
playerlist = InterfaceListable([omxplayer,twitchplayer, youtubeplayer])

logging.info("creating browser objects")
fileBrowser = FileBrowser()
twitchWinluBrowser = TwitchBrowser('winlu')
twitchKillerkakaduBrowser = TwitchBrowser('killerkakadu')
youtubeBrowser = YoutubeBrowser()
browserlist = InterfaceListable([fileBrowser,twitchWinluBrowser,twitchKillerkakaduBrowser,youtubeBrowser])

#logging.info("creating playlist objects")
#playList = Single()
#playlistlist = InterfaceListable([playList])
playlistlist = InterfaceListable([])

logging.info("creating controller")
controller = WebController(playerList=playerlist, playlistList=playlistlist, browserList=browserlist)

logging.info("creating webinterface")
interface = WebInterface(
    pathToTemplates,
    pathToStatic, 
    controller
    )
    
interface.run()


