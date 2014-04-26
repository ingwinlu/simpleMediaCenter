from distutils.core import setup

setup(
    name='simpleMediaCenter',
    version='0.5.6',
    packages=['simpleMediaCenter',
            'simpleMediaCenter.browser',
            'simpleMediaCenter.helpers.twitch',
            'simpleMediaCenter.helpers.youtube',
            'simpleMediaCenter.interface',
            'simpleMediaCenter.player',
            'simpleMediaCenter.playlist'],
    package_data={
            'simpleMediaCenter.interface' : ['templates/*.html','static/*.css','static/*.js'],
            '' : ['LICENSE','README.md','simpleMC']
    },
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

