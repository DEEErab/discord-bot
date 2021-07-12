# Libs
import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import datetime
import os

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# 
secret_file = json.load(open(cwd+'/bot-config/secrets.json'))
bot = commands.Bot(command_prefix='.', case_insensitive=True) # can add owner id if needed
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

# change version number for new bot updates
bot.version = '0.0.2'

#potental colours for bot
bot.colors = {
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

# on ready message that prints in the console
@bot.event
async def on_ready():
    # On ready, print some details to standard out
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: .\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Hi, my names {bot.user.name}.\nUse . to interact with me!")) # This changes the bots 'activity'


# on message event
@bot.event
async def on_message(message):
    #Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    #A way to blacklist users from the bot by not processing commands if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    await bot.process_commands(message)


# tells the bot to load files that end in .py and ignore files starting with _
if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)