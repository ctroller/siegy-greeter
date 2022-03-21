import discord
import logging
import random
import sys
import os
from asyncio import sleep
from pathlib import Path
from dotenv import load_dotenv
from random_even_distributed_list import RandomEvenDistributedList

working_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
debug_mode = bool(sys.argv[2]) if len(sys.argv) > 2 else False
load_dotenv(dotenv_path="{0}/.env{1}".format(working_dir, '.dev' if debug_mode else ''))

status = os.getenv("DISCORD_STATUS").split(",")
SIEGY_ID = int(os.getenv("SIEGY_USER"))
STROBEY_ID = int(os.getenv("STROBEY_USER"))
UELI_ID = int(os.getenv("UELI_USER"))
UELI_CHANNEL = int(os.getenv("UELI_CHANNEL"))

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="{0}/discord.log".format(working_dir), encoding='utf8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.voice_states = True
intents.emojis = True
intents.guild_messages = True
client = discord.Client(intents=intents, activity=discord.Activity(name=random.choice(status).strip(),
                                                                   type=discord.ActivityType.watching))


join_lines = RandomEvenDistributedList(list(Path("{0}/resources/voicelines_join/".format(working_dir)).glob("*.mp3")))
message_lines = RandomEvenDistributedList(list(Path("{0}/resources/voicelines_msg/".format(working_dir)).glob("*.mp3")))
text_files = RandomEvenDistributedList(list(Path("{0}/resources/text_msg/".format(working_dir)).glob("*.txt")))
emojis = RandomEvenDistributedList(os.getenv("REG_REACTIONS").split(","))


def get_random_join_voiceline():
    return join_lines.get_random_item().resolve()


def get_random_text_voiceline():
    return discord.File(message_lines.get_random_item().resolve())


def get_cornhub():
    return Path("{0}/resources/cornhub.mp3".format(working_dir)).resolve()


def get_random_text_message():
    with(open(text_files.get_random_item()), 'r') as f:
        return "".join(f.readlines())


def get_random_reg_emojis():
    return emojis.get_random_item()


async def send_sound(channel, audio_file):
    source = discord.FFmpegPCMAudio(audio_file)
    try:
        channel.play(source)
        while channel.is_playing():
            await sleep(1)
        await channel.disconnect(force=False)
        channel.cleanup()
    except TypeError as err:
        logger.warning("TypeError raised {0}".format(err))
        await send_sound(channel, audio_file)


@client.event
async def on_voice_state_update(member, before, _):
    if before.channel is None and member.id == STROBEY_ID and member.voice.channel is not None:
        channel = await member.voice.channel.connect()
        await send_sound(channel, get_cornhub())
    elif before.channel is None and member.id == SIEGY_ID and member.voice.channel is not None:
        channel = await member.voice.channel.connect()
        await send_sound(channel, get_random_join_voiceline())


random_choice = RandomEvenDistributedList(range(1, 4))


@client.event
async def on_message(message):
    if message.channel.id == UELI_CHANNEL and message.author.id == UELI_ID:
        rng = random_choice.get_random_item()

        if rng == 1:
            pick = get_random_reg_emojis()
            for emoji in pick:
                await message.add_reaction(emoji)
        elif rng == 2:
            text = get_random_text_message()
            await message.channel.send(text.replace("$USER", "<@{0}>".format(UELI_ID)))
        elif rng == 3:
            file = get_random_text_voiceline()
            await message.channel.send(content="<@{0}>".format(UELI_ID), file=file)


if __name__ == '__main__':
    client.run(os.getenv("DISCORD_TOKEN"))
