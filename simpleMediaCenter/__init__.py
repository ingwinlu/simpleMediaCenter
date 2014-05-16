from simpleMediaCenter.interface.WebInterface import WebInterface, WebController
from simpleMediaCenter.interface.Interface import InterfaceListable
from simpleMediaCenter.browser.Browser import YoutubeBrowser
from simpleMediaCenter.playlist.Playlist import Single
import simpleMediaCenter.interface.service as service
import logging
import os
import sys
import configparser
import argparse

class SimpleMediaCenter():
    __logger=logging.getLogger(__name__)
    config_file = os.path.expanduser('~/.simpleMediaCenter-config.ini')
    config = None
    playerlist = None
    browserlist = None
    playlistlist = None
    controller = None
    interface = None
    
    '''
        init simpleMediaCenter, parse config
    '''
    def __init__(self):
        self.__logger.debug('init')
        self.config = configparser.ConfigParser()
        self.__logger.debug('setting default config')
        self.config = self.__setDefaultConfig(self.config)
        self.__logger.debug('trying to read config')
        try:
            self.__logger.info('using config file at ' + self.config_file)
            self.config.read_file(open(self.config_file))
        except FileNotFoundError as e:
            self.__logger.warning('config file not found, using default settings')
            try:
                self.__saveConfig()
            except Exception as e:
                self.__logger.critical('exception while saving config file: ' + repr(e))
        #parse config 
        self.__logger.info('parsing config')
        ##init players
        self.__logger.debug('parse players')
        array=[]
        try:
            if (self.config.getboolean('OMXPLAYER','use')):
                from simpleMediaCenter.player.Omxplayer import Omxplayer
                omxplayer = Omxplayer(self.config.get('OMXPLAYER','cmdline'))
                array.append(omxplayer)
            if (self.config.getboolean('TWITCHPLAYER','use')):
                from simpleMediaCenter.player.Twitchplayer import Twitchplayer
                twitchplayer = Twitchplayer(self.config.get('TWITCHPLAYER','cmdline'))
                array.append(twitchplayer)
            if (self.config.getboolean('YOUTUBEPLAYER','use')):
                from simpleMediaCenter.player.Youtubeplayer import Youtubeplayer
                youtubeplayer = Youtubeplayer(self.config.get('YOUTUBEPLAYER','cmdline'))
                array.append(youtubeplayer)
            if (self.config.getboolean('MPLAYER','use')):
                from simpleMediaCenter.player.MPlayer import MPlayer
                mplayer = MPlayer()
                array.append(mplayer)
        except ValueError as e:
            self.__logger.critical('value error while parsing players in config file: ' + repr(e))
            self.__logger.exception(e)
            return
        self.playerlist = InterfaceListable(array)
        ##init browsers
        self.__logger.debug('parse browsers')
        array=[]
        try:
            if (self.config.getboolean('FILEBROWSER','use')):
                from simpleMediaCenter.browser.Browser import FileBrowser
                fileBrowser = FileBrowser()
                array.append(fileBrowser)
            if (self.config.getboolean('TWITCHBROWSER','use')):
                from simpleMediaCenter.browser.Browser import TwitchBrowser
                for username in self.config.get('TWITCHBROWSER','usernames').split(','):
                    tb = TwitchBrowser(username)
                    array.append(tb)
            if (self.config.getboolean('YOUTUBEBROWSER','use')):
                from simpleMediaCenter.browser.Browser import YoutubeBrowser
                youtubeBrowser = YoutubeBrowser()
                for favorite in self.config.get('YOUTUBEBROWSER','favorites').split(','):
                    youtubeBrowser.addFavorite(favorite)
                array.append(youtubeBrowser)            
        except ValueError as e:
            self.__logger.critical('value error while parsing browsers in config file: ' + repr(e))
            self.__logger.exception(e)
            return
        self.browserlist = InterfaceListable(array)
        ##init playlists
        self.__logger.debug('parse playlists')
        array=[]
        try:
            if (self.config.getboolean('SINGLEPLAYLIST','use')):
                playList = Single()
                array.append(playList)          
        except ValueError as e:
            self.__logger.critical('value error while parsing playlists in config file: ' + repr(e))
            self.__logger.exception(e)
            return
        self.playlistlist = InterfaceListable(array)
        ##create controller
        ##init webinterface
        self.__logger.debug('parse interface')
        try:
            if (self.config.getboolean('WEBINTERFACE','use')):
                pathToTemplates = self.config.get('WEBINTERFACE','templatePath')
                pathToStatic = self.config.get('WEBINTERFACE','staticPath')
                #TODO check if paths are valid
                port = self.config.getint('WEBINTERFACE', 'port')
                
                self.__logger.info('creating interface service')
                service.setup(
                    players=self.playerlist,
                    playlists=self.playlistlist,
                    browsers=self.browserlist)
                
                self.__logger.info('creating controller')
                self.controller = WebController()
                self.__logger.info('creating webinterface')
                self.interface = WebInterface(
                    pathToTemplates,
                    pathToStatic, 
                    port,
                    self.controller)
        
        except ValueError as e:
            self.__logger.critical('value error while parsing webinterface in config file: ' + repr(e))
            self.__logger.exception(e)
            return
        except Exception as e:
            self.__logger.critical('error while parsing webinterface in  config file: ' + repr(e))
            self.__logger.exception(e)
            return
        #finished parsing
        
    '''
        run the media center by starting the previously setup interface
    '''
    def run(self):
        self.interface.run()

    def __setDefaultConfig(self, input_config):
        output_config = input_config
        
        #webinterface
        output_config['WEBINTERFACE'] = {
                'use'          : 'yes',
                'templatePath' : self.__getWebInterfacePath('templates/'),
                'staticPath'   : self.__getWebInterfacePath('static/'),    
                'port'         : '8080'
            }
        #players
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
        output_config['MPLAYER'] = {
                'use'     : 'no'
            }
        #browser
        output_config['FILEBROWSER'] = {
                'use'   : 'yes'
            }
        output_config['TWITCHBROWSER'] = {
                'use'   : 'no',
                'usernames' : 'user1,user2'
            }
        output_config['YOUTUBEBROWSER'] = {
                'favorites' : 'MrSuicideSheep,Escapist,TopGear',
                'use'   : 'no'
            }
        #playlists
        output_config['SINGLEPLAYLIST'] = {
                'use'   : 'no'
            }
        
        return output_config
        
    def __saveConfig(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
            
    def __getWebInterfacePath(self, subdir):
        path = os.path.abspath(os.path.dirname(sys.modules[WebInterface.__module__].__file__))
        path = os.path.abspath(os.path.join(path, subdir))
        logging.debug('getWebInterfacePath:' + path)
        return path
        
'''
    argument parsing
'''
def parseArgs():
    parser = argparse.ArgumentParser(
        description="simpleMediaCenter aims to provide an easy on ressources way to use your computer as an Media Center. It is primarily designed to act as an alternative to XBMC on the rpi.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-D', '--debug', action='store_const',
                        const=logging.DEBUG, dest='verbosity',
                        help='Show all messages, including DEBUG')
    return parser.parse_args()
