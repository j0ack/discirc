DiscIRC
=======

|build|

**DiscIRC** is a bot that syncs messages between `Discord <https://discordapp.com/>`_ and `IRC <http://www.irc.org/>`_. It's written in Python using the `discord.py <https://github.com/Rapptz/discord.py>`_ and `bottom <https://github.com/numberoverzero/bottom>`_ libraries.

Installation
------------

You can install it simply using `pip`::

  $ pip install discirc

Use
---

Launch
******

You first need to configure **DiscIRC** thanks to a config file. By default **DiscIRC** tries to load a `~/.discirc` file, if not present you need to give it to the app with the `-- config` option.

To create a valid config file please see the `example <https://raw.githubusercontent.com/j0ack/discirc/master/config-example.json>`_.

Then simply run **DiscIRC** thanks to the available command::

  $ discirc

Private messages
****************

**DiscIRC** handles private messages. You need to prefix your message with a `@User` when sent from **Discord** and with `User:` from IRC.

.. |build| image:: https://drone.joakode.fr/api/badges/joack/discirc/status.svg
