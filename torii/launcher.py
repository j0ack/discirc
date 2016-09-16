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

"""
    Torii launcher
    --------------

    Launcher for torii app
"""

import click
import asyncio
import os.path as op
import sys
import json

from torii.discord_bot import DiscordWrapper
from torii.irc_bot import IRCBot


__author__ = 'TROUVERIE Joachim'


@click.command()
@click.option('-c', '--config', type=click.Path(),
              help='Alternate config file (default to ~/.toriirc)')
def main(config):
    if not config:
        config = op.expanduser('~/.toriirc')
    if not op.exists(config):
        sys.exit(1, 'No config file found')

    with open(config, 'r') as fi:
        conf = json.load(fi)

    irc = IRCBot(conf)
    disc = DiscordWrapper(conf)

    loop = asyncio.get_event_loop()
    loop.create_task(irc.connect())
    loop.create_task(disc.run())
    loop.run_forever()
