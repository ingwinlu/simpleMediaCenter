'''
    singelton module tohandle player functions, threadable
'''

import logging

__logger=logging.getLogger("interface_service")

playerList = None
playlistList = None
browserList = None

'''
    sets module wide variables
'''
def setup(players, playlists, browsers):
    def _printwarn(variable):
        __logger.warn("variable already set: " + variable)

    global playerList
    global playlistList
    global browserList
    if(playerList == None):
        playerList = players
    else:
        _printwarn("playerList")
    if(playlistList == None):
        playlistList = playlists
    else:
        _printwarn("playlistList")
    if(browserList == None):
        browserList = browsers
    else:
        _printwarn("browserList")


'''
    starts playback
    @param id Integer id to play
'''
def play(id):
    global __logger
    global playerList
    global browserList
    
    __logger.debug("trying to play %s" ,browserList.getActive().getPlayable(id))
    __logger.debug("searching for compatible Browser")
    for supportedPlayer in browserList.getActive().getSupportedPlayers():
        playerid = playerList.getIDfromName(supportedPlayer)
        if (playerid is not None):
            break
    if (playerid is None):
        raise Exception('no compatible player found in supportedPlayers')
    playerList.getActive().stop()
    playerList.setActive(playerid)
    playerList.getActive().play(browserList.getActive().getPlayable(id))

'''
    stops playback
'''
def stop():
    global __logger
    global playerList
    __logger.debug("stop called")
    playerList.getActive().stop()

'''
    pauses playback
'''
def pause():
    global __logger
    global playerList
    __logger.debug("pause called")
    playerList.getActive().pause()

'''
    lowers volume
'''
def volume_down():
    global __logger
    global playerList
    __logger.debug("volume down called")
    playerList.getActive().volumeDown()
    
'''
    raises volume
'''
def volume_up():
    global __logger
    global playerList
    __logger.debug("volume up called")
    playerList.getActive().volumeUp()
    
'''
    change working directory
'''
def change(id):
    global __logger
    global browserList
    __logger.debug("change called %s", id)
    browserList.getActive().setWorkingDir(id)
    
'''
    search something which is then treated as a playable file
'''
def search_file(search):
    global __logger
    global browserList
    __logger.debug("searchFile called: " + search)
    if (browserList.getActive().getDict().get('browserSearch',False)):
        browserList.getActive().setWorkingDir(search, search='File')
    
'''
    search something which is then treated as a browsable directory
'''
def search_dir(search):
    global __logger
    global browserList
    __logger.debug("searchDir called")
    if (browserList.getActive().getDict().get('browserSearch',False)):
        browserList.getActive().setWorkingDir(search, search='Dir')
        
'''
    DEPRECATED: is now done automatically
    selects player via dropdown menu
'''
def select_player(id):
    global playerList
    playerList.getActive().stop()
    playerList.setActive(id)
    
'''
    selects browser via dropdown menu
'''
def select_browser(id):
    global browserList
    browserList.setActive(id)
    
'''
    selects playlist via dropdown menu
'''
def select_playlist(id):
    global playlistList
    playlistList.setActive(id)
