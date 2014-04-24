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

class SimpleMediaCenter():
    __logger=logging.getLogger(__name__)
    config_file = os.path.expanduser('~/.simpleMediaCenter-config.ini')
    config = None
    
    '''
        init simpleMediaCenter, parse config
    '''
    def __init__(self):
        self.__logger.debug('init')
        self.config = configparser.ConfigParser()
        self.config = self.__setDefaultConfig(self.config)
        try:
            self.config.read_file(open(self.config_file))
        except FileNotFoundError as e:
            self.__logger.warning('config file not found, using default settings')
        #parse config 
        

    def __setDefaultConfig(self, input_config):
        output_config = input_config
        output_config['LOGGING'] = {
                'level' : logging.DEBUG
            }
        output_config['WEBINTERFACE'] = {
                'use'          : 'yes',
                'templatePath' : os.path.abspath('./interface/templates/'),
                'staticPath'   : os.path.abspath('./interface/static/')
            }
        output_config['OMXPLAYER'] = {
                'use'     : 'yes',
                'cmdline' : '-o both'
            }
        output_config['TWITCHPLAYER'] = {
                'use'     : 'no',
                'cmdline' : '-o both'
            }
        output_config['YOUTUBEPLAYER'] = {
                'use'     : 'no',
                'cmdline' : '-o both'
            }
            
        output_config['FILEBROWSER'] = {
                'use'   : 'yes'
            }
            
        output_config['TWITCHBROWSER'] = {
                'use'   : 'no',
                'usernames' : 'user1,user2'
            }
            
        output_config['YOUTUBEBROWSER'] = {
                'use'   : 'no'
            }
            
        output_config['SINGLEPLAYLIST'] = {
                'use'   : 'no'
            }
            
        return output_config
        
    def __saveConfig(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
    
    '''
        run the media center
    '''
    def run(self):
        try:
            self.__saveConfig()
        except Exception as e:
            self.__logger.critical('exception while saving config file: ' + repr(e))

        
    
if __name__ == "__main__":
    smc = SimpleMediaCenter()
    smc.run()
    pass
'''
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
'''

