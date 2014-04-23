simpleMediaCenter
=================

simpleMediaCenter aims to provide an easy on Ressources way to use your computer as an Media Center. 

Planned Core Features:
+ Web Interface (jinja + turbogears)
+ omxplayer compability

##TODO 
priority from top to bottom:
+ ~~implement an interface where js or other clients can pull json data from~~
+ ~~use javascript to disable buttons~~
+ ~~move player to the navbar~~
+ ~~split up index page generation from playerstatus~~
+ ~~implement automatic player choosing~~
+ ~~rework Browser~~
   + ~~should use id's to interact with controller, not the actual value, no idea what I was thinking~~
   + ~~couple them with player, i.e. don't let any player use any browser~~
   + implement sendToBrowser in REST Interface 
   + complete TwitchBrowser
   + complete YoutubeBrowser
+ exceptions
   + create exceptionclasses for input/processing errors
   + ~~create space in templates to display exceptiontext~~
   + ~~implement javascript to display exceptions~~
+ implement configparser
+ implement playlist functionality
+ improve documentation 
+ improve comments in code
+ rework omxplayer to use dbus interface
+ feedback for longer loads
   + convince artist to paint a loading please wait image for beer
   + implement 'holding' page while load
+ drag and drop between browser/playlist

##Requirements
+ python3
+ [omxplayer](http://omxplayer.sconde.net/)
+ [TurboGears2](http://turbogears.org/)
+ [jinja2](http://jinja.pocoo.org/)
+ [youtube-dl](https://github.com/rg3/youtube-dl)
    
    for youtube playback
+ [Bootswatch (Bootstrap-Themes)](https://github.com/thomaspark/bootswatch)
    
    cosmo theme is included

##Installation
0. install youtube-dl
1. install omxplayer
2. install Turbogears2 and jinja2 via python-pip
3. clone this repository (on release there will be a package on pypi)
4. navigate to the simpleMediaCenter/simpleMediaCenter directory
5. run simpleMediaCenter.py

Please note that this project is still in heavy development and way of installation/configuration will improve

##Screenshot
![index Screenshot V0.4](./docs/simpleMediaServer_v0_4.PNG)


 
