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
    IRC bot
    -------

    IRC bot for DiscIRC app
"""

import bottom
import random
import discirc.signals as SIGNALNAMES

from asyncblink import signal
from discirc.message import Message


__author__ = 'TROUVERIE Joachim'


class IRCBot(bottom.Client):
    """IRC bot wrapper

    :param config: config for bot
    :type config: dict
    """

    COLOR_PREF = '\x03'
    CANCEL = '\u000F'

    def __init__(self, config):
        super(IRCBot, self).__init__(
            host=config['ircServer'],
            port=config.get('ircPort', 6667),
            ssl=config.get('ircSsl', False)
        )
        self.nick = config.get('ircNick', 'discirc')
        self.channels = config['mappingChannels']
        self.password = config.get('ircPass')
        self.channelPass = config['channelPass']

        self.on('CLIENT_CONNECT', self.on_connect)
        self.on('PING', self.on_ping)
        self.on('PRIVMSG', self.on_irc_message)
        self.on('RPL_ENDOFMOTD', self.on_motddone)
        self.on('ERR_NOMOTD', self.on_motddone)

        self.users = dict()

        # signals
        self.discord_signal = signal(SIGNALNAMES.DISCORD_MSG)
        self.discord_signal.connect(self.on_discord_message)
        self.irc_signal = signal(SIGNALNAMES.IRC_MSG)

    def on_connect(self):
        """On connect event"""
        self.send('NICK', nick=self.nick)
        self.send('USER', user=self.nick, realname='Discord gateway')
        if self.password:
            self.send('PASS', password=self.password)

    def on_motddone(self, message):
        """checking if Message Of The Day is done because it may interfere with joining channels"""
        for chan in self.channels.values():
            if chan not in self.channelPass:
                self.send('JOIN', channel=chan)
            else:
                self.send('JOIN', channel=chan, key=self.channelPass[chan])

    def on_ping(self, message, **kwargs):
        """Keep alive server"""
        self.send('PONG', message=message)

    def on_irc_message(self, nick, target, message, **kwargs):
        """On IRC message event

        :param nick: Message author nick
        :param target: Message target (priv or channel)
        :param message: Message content
        """
        if nick == self.nick:
            return

        data = Message(target, nick, message)

        if target != self.nick:
            self.irc_signal.send(self, data=data, private=False)
        else:
            words = message.split(':')
            target = words.pop(0)
            content = ' '.join(words)
            data = Message(target, nick, content)
            self.irc_signal.send(self, data=data, private=True)

    def on_discord_message(self, sender, **kwargs):
        """On Discord message event callback

        :param sender: Message sender
        """
        message = kwargs['data']
        private = kwargs['private']
        source = message.source
        content = message.content
        if not private:
            target = self.channels.get(message.channel)
        else:
            target = message.channel

        for msg in content.split('\n'):
            # set a color for this author
            if source not in self.users:
                self.users[source] = self.COLOR_PREF + str(random.randint(2, 15))
            format_msg = '<{}{}{}> {}'.format(
                self.users[source],
                source,
                self.CANCEL,
                msg
            )
            self.send('PRIVMSG', target=target, message=format_msg)
