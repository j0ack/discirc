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
    Discord bot
    -----------

    Discord bot for Torii gateway
"""

import asyncio
import discord
import torii.signals as SIGNALNAMES

from torii.message import Message
from blinker import signal


__author__ = 'TROUVERIE Joachim'


class DiscordWrapper(object):
    """Discord bot wrapper

    :param config: config for bot
    :type config: dict
    """

    def __init__(self, config):
        self.bot = discord.Client()
        self.token = config['discordToken']
        self.channels = config['mappingChannels']
        self.command_chars = config.get('commandChars', [])

        # signals
        self.discord_signal = signal(SIGNALNAMES.DISCORD_MSG)
        self.discord_priv_signal = signal(SIGNALNAMES.DISCORD_PRIV_MSG)
        self.irc_signal = signal(SIGNALNAMES.IRC_MSG)
        self.irc_signal.connect(self.on_irc_message)
        self.irc_priv_signal = signal(SIGNALNAMES.IRC_PRIV_MSG)
        self.irc_priv_signal.connect(self.on_irc_priv_message)

        self.bot.event(self.on_message)

    def run(self):
        """Run discord bot"""
        self.bot.run(self.token)

    async def on_message(self, message):
        """Event on discord message received

        :param message: Discord message
        """
        if str(message.author) != str(self.bot.user):
            full_message = [message.clean_content]
            if not full_message[0]:
                full_message.pop(0)
            for attachment in message.attachments:
                full_message.append(attachment.get('url', ''))

            content = ' '.join(full_message)
            channel = message.channel.name
            source = message.author.name

            # private message
            if not channel:
                if content.startswith('@'):
                    words = content.split()
                    channel = words.pop(0)[1:]
                    content = ' '.join(words)
                    msg = Message(channel, source, content)
                    self.discord_priv_signal.send(self, data=msg)
                else:
                    msg = ('I do not know who you want to contact, please ' +
                           'prefix your message with @User')
                    await self.bot.send_message(message.channel, msg)
            else:
                msg = Message(channel, source, content)
                self.discord_signal.send(self, data=msg)

    def on_irc_message(self, sender, **kwargs):
        """Event on IRC message received

        :param message: IRC message
        """
        maps = {
            irc: discord for discord, irc in self.channels.items()
        }
        message = kwargs['data']
        chan = maps.get(message.channel)
        if chan:
            discord_chan = self._get_channel_by_name(chan)
            if self._is_command(message.content):
                asyncio.async(self.bot.send_message(discord_chan, message.content))
            else:
                msg = '**<{}>** {}'.format(message.source, message.content)
                asyncio.async(self.bot.send_message(discord_chan, msg))

    def on_irc_priv_message(self, sender, **kwargs):
        """Event on IRC message received

        :param message: IRC message
        """
        message = kwargs['data']
        user = self._get_user_by_name(message.channel)
        if user:
            asyncio.async(self.bot.send_message(user, message.content))

    def _get_user_by_name(self, username):
        """Get Discord user by his name

        :param username: User's name
        """
        users = self.bot.get_all_members()
        for user in users:
            if user.name == username:
                return user
        return None

    def _get_channel_by_name(self, channel_name):
        """Get bot channel by its name

        :param channel_name: Channel's name
        """
        channels = self.bot.get_all_channels()
        for chan in channels:
            if chan.name == channel_name:
                return chan
        return None

    def _is_command(self, message):
        """Check if message is a command

        :param message: Message content
        """
        if message:
            for char in self.command_chars:
                if message.startswith(char):
                    return True
        return False
