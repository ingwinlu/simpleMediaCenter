from distutils.core import setup

setup(
    name='simpleMediaCenter',
    description='simpleMediaCenter aims to provide an easy on ressources way to use your computer as an Media Center. It is primarily designed to act as an alternative to XBMC on the rpi.',
    version='0.5.8',
    url='https://github.com/ingwinlu/simpleMediaCenter',
    packages=['simpleMediaCenter',
            'simpleMediaCenter.browser',
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
    long_description=open('README.md').read(),
    author='winlu',
    author_email='derwinlu+simpleMediaCenter@gmail.com',
)

