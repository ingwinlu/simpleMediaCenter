from distutils.core import setup

setup(
	name='simpleMediaCenter',
	version='0.5.4',
	packages=['simpleMediaCenter',
			'simpleMediaCenter.browser',
			'simpleMediaCenter.helpers.twitch',
			'simpleMediaCenter.interface',
			'simpleMediaCenter.player',
			'simpleMediaCenter.playlist'],
    package_data={
            'simpleMediaCenter.interface' : ['templates/*.html','static/*.css','static/*.js'],
            '' : ['LICENSE','README.md']            
    },
    requires = [
        'jinja2',
        'turbogears2'
    ],
	license=open('LICENSE').read(),
	long_description=open('README.md').read(),
	author='winlu',
	author_email='derwinlu+simpleMediaCenter@gmail.com',
)

