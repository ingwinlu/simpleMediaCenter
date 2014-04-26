#!/usr/bin/env python3

from interface.WebInterface import WebInterface, WebController
from interface.Interface import InterfaceListable
from browser.Browser import YoutubeBrowser
from playlist.Playlist import Single
import logging
import os
import configparser

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
        self.config = self.__setDefaultConfig(self.config)
        try:
            self.__logger.info('using config file at ' + self.config_file)
            self.config.read_file(open(self.config_file))
        except FileNotFoundError as e:
            self.__logger.warning('config file not found, using default settings')
        #parse config 
        self.__logger.info('parse config')
        ##logging settings
        self.__logger.debug('parse logging settings')
        try:
            self.__logger.setLevel(self.config.getint('LOGGING','level'))
        except Exception as e:
            self.__logger.critical('value error while parsing logging settings in  config file: ' + repr(e))
        ##init players
        self.__logger.debug('parse players')
        array=[]
        try:
            if (self.config.getboolean('OMXPLAYER','use')):
                from player.Omxplayer import Omxplayer
                omxplayer = Omxplayer(self.config.get('OMXPLAYER','cmdline'))
                array.append(omxplayer)
            if (self.config.getboolean('TWITCHPLAYER','use')):
                from player.Twitchplayer import Twitchplayer
                twitchplayer = Twitchplayer(self.config.get('TWITCHPLAYER','cmdline'))
                array.append(twitchplayer)
            if (self.config.getboolean('YOUTUBEPLAYER','use')):
                from player.Youtubeplayer import Youtubeplayer
                youtubeplayer = Youtubeplayer(self.config.get('YOUTUBEPLAYER','cmdline'))
                array.append(youtubeplayer)            
        except ValueError as e:
            self.__logger.critical('value error while parsing players in  config file: ' + repr(e))
        self.playerlist = InterfaceListable(array)
        ##init browsers
        self.__logger.debug('parse browsers')
        array=[]
        try:
            if (self.config.getboolean('FILEBROWSER','use')):
                from browser.Browser import FileBrowser
                fileBrowser = FileBrowser()
                array.append(fileBrowser)
            if (self.config.getboolean('TWITCHBROWSER','use')):
                from browser.Browser import TwitchBrowser
                for username in self.config.get('TWITCHBROWSER','usernames').split(','):
                    tb = TwitchBrowser(username)
                    array.append(tb)
            if (self.config.getboolean('YOUTUBEBROWSER','use')):
                from browser.Browser import YoutubeBrowser
                youtubeBrowser = YoutubeBrowser()
                for favorite in self.config.get('YOUTUBEBROWSER','favorites').split(','):
                    youtubeBrowser.addFavorite(favorite)
                array.append(youtubeBrowser)            
        except ValueError as e:
            self.__logger.critical('value error while parsing players in  config file: ' + repr(e))
        self.browserlist = InterfaceListable(array)
        ##init playlists
        self.__logger.debug('parse playlists')
        array=[]
        try:
            if (self.config.getboolean('SINGLEPLAYLIST','use')):
                playList = Single()
                array.append(playList)          
        except ValueError as e:
            self.__logger.critical('value error while parsing players in  config file: ' + repr(e))
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
                
                self.__logger.info('creating controller')
                self.controller = WebController(
                    playerList=self.playerlist, 
                    playlistList=self.playlistlist, 
                    browserList=self.browserlist)
                self.__logger.info('creating webinterface')
                self.interface = WebInterface(
                    pathToTemplates,
                    pathToStatic, 
                    port,
                    self.controller)
        
        except ValueError as e:
            self.__logger.critical('value error while parsing webinterface in  config file: ' + repr(e))
        except Exception as e:
            self.__logger.critical('error while parsing webinterface in  config file: ' + repr(e))
        #finished parsing
        
    '''
        run the media center by starting the previously setup interface
    '''
    def run(self):
        self.interface.run()
        try:
            self.__saveConfig()
        except Exception as e:
            self.__logger.critical('exception while saving config file: ' + repr(e))

    def __setDefaultConfig(self, input_config):
        output_config = input_config
        output_config['LOGGING'] = {
                'level' : logging.DEBUG
            }
        output_config['WEBINTERFACE'] = {
                'use'          : 'yes',
                'templatePath' : os.path.abspath('./interface/templates/'),
                'staticPath'   : os.path.abspath('./interface/static/'),
                'port'         : '8080'
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
                'favorites' : 'MrSuicideSheep,Escapist,TopGear',
                'use'   : 'no'
            }
            
        output_config['SINGLEPLAYLIST'] = {
                'use'   : 'no'
            }
            
        return output_config
        
    def __saveConfig(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Please run ./simpleMC instead')
    logging.shutdown()

