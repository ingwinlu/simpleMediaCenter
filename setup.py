from distutils.core import setup

setup(
	name='simpleMediaCenter',
	version='0.2',
	packages=['simpleMediaCenter',
			'simpleMediaCenter.fileCrawler',
			'simpleMediaCenter.interface',
			'simpleMediaCenter.player',
			'simpleMediaCenter.playlist'],
    package_data={
            'simpleMediaCenter.interface' : ['templates/*.html','static/*.css'],
            '' : ['LICENSE','README.md']            
    },
    requires = [
        'jinja2',
        'turbogears2'
    ],
	license=open('LICENSE').read(),
	long_description=open('README.md').read(),
	author='winlu',
	author_email='derwinlu+python@gmail.com',
)

