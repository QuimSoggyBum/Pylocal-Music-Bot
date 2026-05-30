# Pylocal Music Bot

Want to listen to your totally legal (not pirated) songs in Discord? Using the Discord.py API, our bot lets you stream local MP3 files. Wanna try a new way of bumping rad tunes? This bot is for you!

# Commands

* !join - connects bot to voice channel of user issuing the command

* !play - plays a song in the music directory of the user issuing command with a song name specified after the command

* !pause - pauses the song that is currently playing

* !resume - resumes the song that was paused

* !stop - stops the voice client

* !leave - disconnects the bot from the voice channel


# Install
make sure you have installed Python, discord.py we don't include this, this
was and is built on Linux.

when installing your libs, install them in to your root bot folder /lib, this fixed problems with
some locked down version of linux this script already loads from the /lib folder.


`pip3 install --target=./lib discord.py`

`pip3 install --target=./lib davey`
