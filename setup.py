#!/usr/bin/env python
from pathlib import Path
from setuptools import setup

setup(
    name='openid_wargaming',
    version=Path('VERSION').read_text().strip(),
    description=Path('README.md').read_text(),
    author='Miguel Angel Curiel',
    setup_requires=['setuptools>=17.1'],
    install_requires=['requests>=2.18.3'],
    packages=['openid_wargaming'],
)
