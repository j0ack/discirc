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
    Message class
    -------------

    Wrapper for bots messages
"""

__author__ = 'TROUVERIE Joachim'


class Message(object):
    """Wrapper for bots messages

    :param channel: Message channel
    :param source: Message source
    :param content: Message content
    """
    def __init__(self, channel, source, content):
        self.channel = channel
        self.source = source
        self.content = content
    
