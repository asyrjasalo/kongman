#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

CLASSIFIERS = '''
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Utilities
'''.strip().splitlines()

CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, 'kong', '__init__.py'), encoding="utf-8") as f:
    VERSION = re.search("__version__ = '(.*)'", f.read()).group(1)
with open(join(CURDIR, 'README.md'), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()
with open(join(CURDIR, 'requirements.txt'), encoding="utf-8") as f:
    REQUIREMENTS = f.read()

setup(
    name             = 'kong-incubator',
    version          = VERSION,
    description      = 'Declare the Kong you want in yaml (fork of aio-kong)',
    long_description = LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    author           = 'Anssi Syrjäsalo (aio-kong by Luca Sbardella)',
    author_email     = 'anssi.syrjasalo@gmail.com',
    url              = 'https://github.com/asyrjasalo/kongman',
    license          = 'BSD',
    keywords         = 'kong config setup cli yaml async aiohttp',
    classifiers      = CLASSIFIERS,
    install_requires = REQUIREMENTS,
    packages         = find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        "console_scripts": [
            "kong-incubator = kong.cli:main"
        ]
    }
)