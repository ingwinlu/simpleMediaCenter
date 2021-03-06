simpleMediaCenter
=================
[![Downloads](http://img.shields.io/pypi/dm/simpleMediaCenter.svg)](https://pypi.python.org/pypi/simpleMediaCenter#downloads)
[![Latest Version](http://img.shields.io/pypi/v/simpleMediaCenter.svg)](http://pypi.python.org/pypi/simpleMediaCenter)

simpleMediaCenter aims to provide an easy on ressources way to use your computer as an Media Center. It is primarily designed to act as an alternative to XBMC on the rpi. 

Planned Core Features:
+ Web Interface (jinja + turbogears)
+ omxplayer compatibility
+ file/youtube/twitch.tv playback

##TO-DO and IDEAS
priority from top to bottom:
+ ~~rework Browser~~
   + ~~should use id's to interact with controller, not the actual value, no idea what I was thinking~~
   + ~~couple them with player, i.e. don't let any player use any browser~~
   + ~~implement pagination~~
   + ~~implement sendToBrowser in REST Interface~~
   + complete TwitchBrowser 80%
   + complete YoutubeBrowser 80%
+ multithread interface to implement a loading page 80%
+ implement playlist functionality
+ improve documentation 5%
+ improve comments in code 5%
+ rework omxplayer to use dbus interface
+ feedback for longer loads
   + convince artist to paint a loading please wait image in exchange for beer
   + implement 'holding' page while load
+ add webinterface to change settings
+ drag and drop between browser/playlist

##Requirements
+ python3
+ player (pick one)
    + [omxplayer](http://omxplayer.sconde.net/)
    + mplayer
+ [TurboGears2](http://turbogears.org/)
+ [jinja2](http://jinja.pocoo.org/)
+ [youtube-dl](https://github.com/rg3/youtube-dl)
    for youtube playback
+ [python-twitch](https://github.com/ingwinlu/python-twitch)
    for twitch.tv playback (included)
+ [Bootswatch (Bootstrap-Themes)](https://github.com/thomaspark/bootswatch) (included)

##Installation
###pypi
please note that you have to make sure that omxplayer is available yourself if you install via [pypi](https://pypi.python.org/pypi/simpleMediaCenter).

install via pip:
```
    pip install simpleMediaCenter
```

###installation from github
1. install python3
2. install youtube-dl
3. install omxplayer
4. install Turbogears2 and jinja2 via python-pip
5. clone this repository (on release there will be a package on pypi)
6. navigate to the simpleMediaCenter/simpleMediaCenter directory
7. run ./simpleMC

Please note that this project is still in heavy development and way of installation/configuration will improve.

##Configuration
After the first launch a config file will be generated at ~/.simpleMediaCenter-config.ini which can be edited to customize behaviour.

##Changelog
Sorry I am not doing a changelog at this stage, if you have some coding experience you can check commit messages. If you don't, no problem, I blog about most new features on http://heroicdebugging.biz. Also check the bottom of the readme for recently implemented stuff.

##Screenshot
![index Screenshot V0.4](./docs/simpleMediaServer_v0_5_4.PNG)
![index Screenshot V0.4](./docs/simpleMediaServer_v0_4.PNG)

##Already implemented stuff (just to keep track)
+ ~~implement an interface where js or other clients can pull json data from~~
+ ~~use javascript to disable buttons~~
+ ~~move player to the navbar~~
+ ~~split up index page generation from playerstatus~~
+ ~~implement automatic player choosing~~
+ ~~exceptions~~
   + ~~create exceptionclasses for input/processing errors~~
   + ~~create space in templates to display exceptiontext~~
   + ~~implement javascript to display exceptions~~
+ ~~implement configparser~~
+ ~~flush out mplayer support~~

