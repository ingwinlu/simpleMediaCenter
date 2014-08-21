from distutils.core import setup

upstream = 'https://github.com/ingwinlu/simpleMediaCenter'
devblog = 'http://heroicdebugging.biz'

setup(
    name='simpleMediaCenter',
    description='simpleMediaCenter aims to provide an easy on ressources way to use your computer as an Media Center. It is primarily designed to act as an alternative to XBMC on the rpi.',
    version='0.6.5',
    url=upstream,
    packages=['simpleMediaCenter',
            'simpleMediaCenter.browser',
            'simpleMediaCenter.helpers',
            'simpleMediaCenter.helpers.twitch',
            'simpleMediaCenter.helpers.youtube',
            'simpleMediaCenter.interface',
            'simpleMediaCenter.player',
            'simpleMediaCenter.playlist'],
    package_data={
            'simpleMediaCenter.interface' : ['templates/*.html','static/*.css','static/*.js'],
            '' : ['LICENSE','README.md']
    },
    scripts=['simpleMC'],
    requires = [
        'jinja2',
        'turbogears2',
        'youtube_dl'
    ],
    license='GPLv3',
    long_description='For a longer description, please have a look at ' + upstream + ' or the development blog at ' + devblog,
    author='winlu',
    author_email='derwinlu+simpleMediaCenter@gmail.com',
)

