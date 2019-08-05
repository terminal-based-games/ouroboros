#!/usr/bin/env python3

import pathlib
import setuptools
from distutils.core import setup

# Directory containing this file
HERE = pathlib.Path(__file__).parent

# Package metadata
NAME = "open-ouroboros"
VERSION = "0.1.1"
DESCRIPTION = "A terminal-based snake game" 
README = (HERE / "README.md").read_text()
URL = "https://github.com/terminal-based-games/ouroboros"
AUTHOR = "Carissa & Mack"
EMAIL = "cwood@pdx.edu"

# Call to setup() which does all the work
setup(
    name=NAME,
    version=VERSION,
    packages=["ouroboros"],
    description=DESCRIPTION,
    long_description=README,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    setup_requires=['wheel'],
    entry_points = {
        "console_scripts": [
            "ouroboros=ouroboros.__main__:main"
            ]
        },
    license="MIT License",
)
