import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import discord  # using discord api
from discord.ext import commands  # for text commands

import nacl  # for connecting to voice channels

from mutagen.mp3 import MP3
from mutagen.id3 import ID3

TOKEN = 'YOUR_BOT_TOKEN'

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = commands.Bot(command_prefix='!', intents=intents)

guildID = SERVER_ID
voiceID = VOICE_CHANNEL_ID
textID = TEXT_CHANNEL_ID


def get_song_info(file_path):

    title = None
    artist = None

    try:
        tags = ID3(file_path)

        if "TIT2" in tags:
            title = str(tags["TIT2"])

        if "TPE1" in tags:
            artist = str(tags["TPE1"])

    except:
        pass

    if not title:
        title = os.path.basename(file_path)

    if not artist:
        artist = "Unknown Artist"

    return title, artist


@client.event
async def on_ready():
     print(f'{client.user} has joined the server.')
     generalText = client.get_channel(textID)
     await generalText.send('Pylocal Music Bot as joined your server')


@client.command(name='join')
async def join(ctx):
    generalVoice = ctx.author.voice.channel
    await generalVoice.connect()


@client.command(name='disconnect')
async def disconnect(ctx):
    voiceClient = ctx.author.guild.voice_client
    await voiceClient.disconnect()


search_cache = {}


@client.command(name='play')
async def play(ctx, *arg):

    voiceClient = ctx.author.guild.voice_client

    if voiceClient.is_paused():
        voiceClient.resume()
        return

    song_words = [w.lower() for w in arg]

    music_folder = "./tracks"

    matches = []

    for root, dirs, files in os.walk(music_folder):

        for file in files:

            if not file.lower().endswith(".mp3"):
                continue

            clean_file = file.lower()

            if all(word in clean_file for word in song_words):

                matches.append(os.path.join(root, file))

    if len(matches) == 0:
        await ctx.send("No songs found.")
        return

    if len(matches) > 1:

        search_cache[ctx.author.id] = matches

        response = "**Multiple songs found:**\n"

        for i, m in enumerate(matches[:10]):
            response += f"{i+1}. {os.path.basename(m)}\n"

        response += "\nUse !pick <number>"

        await ctx.send(response)
        return

    song_path = matches[0]

    title, artist = get_song_info(song_path)

    embed = discord.Embed(
        title="Now Playing",
        description=f"**{title}**\nby **{artist}**",
        color=discord.Color.blue()
    )

    file = discord.File("./assets/no_art.png", filename="no_art.png")

    embed.set_thumbnail(url="attachment://no_art.png")

    voiceClient.play(
        discord.FFmpegPCMAudio(source=song_path)
    )

    await ctx.send(file=file, embed=embed)


@client.command(name='pick')
async def pick(ctx, number: int):

    voiceClient = ctx.author.guild.voice_client

    user_cache = search_cache.get(ctx.author.id)

    if not user_cache:
        await ctx.send("No active search. Use !play first.")
        return

    if number < 1 or number > len(user_cache):
        await ctx.send("Invalid selection number.")
        return

    song_path = user_cache[number - 1]

    title, artist = get_song_info(song_path)

    embed = discord.Embed(
        title="Now Playing",
        description=f"**{title}**\nby **{artist}**",
        color=discord.Color.blue()
    )

    file = discord.File("./assets/no_art.png", filename="no_art.png")

    embed.set_thumbnail(url="attachment://no_art.png")

    voiceClient.play(
        discord.FFmpegPCMAudio(source=song_path)
    )

    voiceClient.play(discord.FFmpegPCMAudio(source=song_path))

    await ctx.send(file=file, embed=embed)

    search_cache.pop(ctx.author.id, None)


@client.command(name='pause')
async def pause(ctx):
    voiceClient = ctx.author.guild.voice_client
    if voiceClient.is_paused == True:
        generalText = client.get_channel(textID)
        await generalText.send('No song to pause.')
    else:
        await voiceClient.pause()


@client.command(name='resume')
async def resume(ctx):
    voiceClient = ctx.author.guild.voice_client
    if voiceClient.is_paused:
        await voiceClient.resume()
    else:
        generalText = client.get_channel(textID)
        await generalText.send('No song to resume.')


@client.command(name='stop')
async def stop(ctx):
    voiceClient = ctx.author.guild.voice_client
    if voiceClient.is_playing:
        voiceClient.stop()
    else:
        generalText = client.get_channel(textID)
        await generalText.send('No song to stop.')


@client.command(name='leave')
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or discord.utils.get(ctx.author.roles, name="musicbot"))
async def shutdown(ctx):

    voiceClient = ctx.author.guild.voice_client

    if voiceClient and voiceClient.is_playing():
        voiceClient.stop()

    await ctx.send("Bot is now leaving.")

    if voiceClient:
        await voiceClient.disconnect()

    await client.close()

    sys.exit()


@shutdown.error
async def shutdown_error(ctx, error):

    if isinstance(error, commands.CheckFailure):
        await ctx.send("I will not listen to you because you do not have permission.")


@client.command(name='count')
async def count(ctx):

    music_folder = "./tracks"

    total = 0

    for root, dirs, files in os.walk(music_folder):

        for file in files:

            if file.lower().endswith(".mp3"):
                total += 1

    await ctx.send(f"I can currently play {total} tracks.")


client.run(TOKEN)
