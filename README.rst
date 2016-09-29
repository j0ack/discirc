Torii
=====

**Torii** is a bot that syncs messages between `Discord <https://discordapp.com/>`_ and `IRC <http://www.irc.org/>`_. It's written in Python using the `discord.py <https://github.com/Rapptz/discord.py>`_ and `bottom <https://github.com/numberoverzero/bottom>`_ libraries.

Installation
------------

You can install it simply using `pip`::

  $ pip install torii

Use
---

Launch
******

You first need to configure torii thanks to a config file. By default **Torii** tries to load a `~/.toriirc` file, if not present you need to give it to the app with the `-- config` option.

To create a valid config file please see the `example <https://github.com/j0ack/blob/master/config-example.json>`_.

Then simply run **Torii** thanks to the available command::

  $ torii

Private messages
****************

**Torii** handles private messages. You need to prefix your message with a `@User` when sent from **Discord** and with `User:` from IRC. 
