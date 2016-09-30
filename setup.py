#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

__author__ = 'TROUVERIE Joachim'
__version__ = '0.1'
__appname__ = 'discirc'
__email__ = 'joachim.trouverie@linoame.fr'


requirements = []
for line in open('REQUIREMENTS.txt', 'r'):
    requirements.append(line)

setup(
    name=__appname__,
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email=__email__,
    description='A Discord to IRC gateway', 
    long_description=open('README.rst').read(),
    install_requires=requirements,
    include_package_data=True,
    url='http://pythonhosted.org/discirc/',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",        
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
    ],
    entry_points={
        'console_scripts': [
            'discirc = discirc.launcher:main',
        ],
    },
)

