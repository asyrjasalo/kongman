#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

from kong import __version__


classifiers = """
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Utilities
""".strip().splitlines()

curdir = dirname(abspath(__file__))
with open(join(curdir, "README.md"), encoding="utf-8") as f:
    readme = f.read()
with open(join(curdir, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.read()

setup(
    name="kong-incubator",
    version=__version__,
    description="Declare and manage Kong resources with yaml",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Anssi Syrjäsalo (aio-kong by Luca Sbardella)",
    author_email="anssi.syrjasalo@gmail.com",
    url="https://github.com/asyrjasalo/kongman",
    license="BSD License",
    platforms="any",
    keywords="kong admin yaml configuration async cli",
    classifiers=classifiers,
    install_requires=requirements,
    packages=find_packages(exclude=["tests", "tests.*"]),
    entry_points={"console_scripts": ["kong-incubator = kong.cli:main"]},
)
