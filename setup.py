#!/usr/bin/env python

# Lib imports
import os
from setuptools import setup
from setuptools.command.develop import develop

class SetupDevelop(develop):
    """
    'setup.py develop' is augmented to install development tools.
    """

    def run(self):
        """
        Execute command pip for development requirements.
        """

        assert os.getenv('VIRTUAL_ENV'), 'You should be in a virtualenv!'
        develop.run(self)
        self.spawn(('pip', 'install', '--upgrade', '--requirement', 'requirements-dev.txt'))

setup(
    name='Elysian',
    version='0.1',
    packages=[
        'elysian'
    ],
    install_requires=[
        'click==6.2',
        'wheel==0.24.0'
    ],
    entry_points={
        'console_scripts': [
            'elysian=elysian.cli:cli'
        ]
    },
    cmdclass={
        'develop': SetupDevelop,
    }
)
# vim:set ts=4 sw=4 et ft=python:
