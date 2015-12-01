from setuptools import setup

setup(
	name='Imager',
	version='0.1',
	py_modules=['imager'],
	install_requires=[
		'Click',
	],
	entry_points='''
		[console_scripts]
		imager=imager:cli
	''',
)
