from distutils.core import setup

setup(
	name='simpleMediaCenter',
	version='0.2',
	packages=['simpleMediaCenter',
			'simpleMediaCenter.fileCrawler',
			'simpleMediaCenter.interface',
			'simpleMediaCenter.player',
			'simpleMediaCenter.playlist'],
	license=open('LICENSE').read(),
	long_description=open('README.md').read(),
	author='winlu',
	author_email='derwinlu+python@gmail.com',
)

