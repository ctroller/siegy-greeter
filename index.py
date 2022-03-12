import discord
import logging
import random
import sys
import os
from asyncio import sleep
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path="%s/.env" % working_dir)
working_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

status = os.getenv("DISCORD_STATUS").split(",")
SIEGY_ID = os.getenv("SIEGY_USER")

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="%s/discord.log" % working_dir, encoding='utf8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents, activity=discord.Activity(name=random.choice(status).strip(), type=discord.ActivityType.watching))

sound_files = list(Path("%s/resources/" % working_dir).glob("*.mp3"))


async def send_sound(channel):
    source = discord.FFmpegPCMAudio(random.choice(sound_files).resolve())
    try:
        channel.play(source)
        while channel.is_playing():
            await sleep(1)
        await channel.disconnect(force=False)
        channel.cleanup()
    except TypeError as err:
        logger.warning("TypeError raised {0}".format(err))
        await send_sound(channel)


@client.event
async def on_voice_state_update(member, before, _):
    if before.channel is None and member.id == SIEGY_ID and member.voice.channel is not None:
        channel = await member.voice.channel.connect()
        await send_sound(channel)


client.run(os.getenv("DISCORD_TOKEN"))