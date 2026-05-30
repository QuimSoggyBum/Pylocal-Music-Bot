# Pylocal Music Bot

Want to listen to your totally legal (not pirated) songs in Discord? Using the Discord.py API, our bot lets you stream local MP3 files. Wanna try a new way of bumping rad tunes? This bot is for you!

# Commands

* !join - Connects bot to voice channel so you can play the music commands

* !disconnect - [MUST BE CONNECTED TO VOICE] Disconnects the bot from the voice channel

* !play - [MUST BE CONNECTED TO VOICE] Plays a song in the music directory of the user issuing command with a song name specified after the command

* !pick - [MUST BE CONNECTED TO VOICE] This will play the track you have picked from play when there is more then one song matching that song

* !pause - [MUST BE CONNECTED TO VOICE] Pauses the song that is currently playing

* !resume - [MUST BE CONNECTED TO VOICE] Resumes the song that was paused

* !stop - [MUST BE CONNECTED TO VOICE] Stops the voice client

* !leave - [MUST BE CONNECTED TO VOICE] Disconnects the bot from the voice channel

* !count - Will count the songs in the folder it can currently play

* !version - Will return the version of the of the script (SOON)


# Install
make sure you have installed Python, discord.py we don't include this, this
was and is built on Linux.

when installing your libs, install them in to your root bot folder /lib, this fixed problems with
some locked down version of linux this script already loads from the /lib folder.


`pip3 install --target=./lib discord.py`

`pip3 install --target=./lib davey`




# Credits
This project was based on [Keyboard Warriors Music Bot](https://github.com/MarkKneblik/Keyboard-Warriors-Music-Bot) for windows, Python, Discord.py & Davry
