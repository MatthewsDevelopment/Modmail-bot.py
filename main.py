import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv('.env')
BOTPREFIX=os.getenv("PREFIX")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix=commands.when_mentioned_or(BOTPREFIX), intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.CustomActivity(name="Watching my DMs"))
    print("Modmail-Bot.py [Discord] Bot is Ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.channel.type) == "private":
        modmail_channel = discord.utils.get(client.get_all_channels(), name="modmail")
        await modmail_channel.send(f"**{str(message.author)} | {str(message.author.id)}:** " + message.content)
    elif str(message.channel) == "modmail" and message.content.startswith("<"):
        member_object = message.mentions[0]

        index = message.content.index(" ")
        string = message.content
        mod_message = string[index:]

        await member_object.send("[" + message.author.display_name + "]" + mod_message)

    await client.process_commands(message)



@client.command()
async def help(ctx):
    embed = discord.Embed(title=f"{client.user.name}", description="Here is my list of Commands", color=(58101))
    embed.add_field(name="General", value=f"{BOTPREFIX}help - This message\n{BOTPREFIX}ping - Get the Bot latency\n{BOTPREFIX}setupguide - Instructions on how to setup the modmail system\n{BOTPREFIX}setupmodmail - Setup the Modmail channel.\n{BOTPREFIX}status\n{BOTPREFIX}streamstatus", inline=False)
    embed.add_field(name="Source Code", value="https://codeberg.org/MatthewsDevelopment/Modmail.py\nModmail Bot by Matthews Development", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'PONG!\nLatency: {round(client.latency * 1000)}ms')

@client.command()
@commands.has_permissions(manage_guild=True)
@commands.bot_has_permissions(manage_channels=True)
async def setupmodmail(ctx):
    channel = await guild.create_text_channel('modmail')
    guild = ctx.guild
    channel = discord.utils.get(guild.text_channels, name="modmail")
    role = discord.utils.get(guild.roles, name="@everyone")
    await channel.set_permissions(role, send_messages=False, read_messages=False)
    await ctx.send("The Modmail channel has been set up.")

@setupmodmail.error
async def setupmodmail_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="I need to have the **MANAGE_CHANNELS** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have the **MANAGE_GUILD** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
async def setupguide(ctx):
    embed = discord.Embed(title="Modmail Bot", description="Here is instructions on how to setup the basic modmail system", color=(58101))
    embed.add_field(name="Steps", value="After inviting the bot, create a channel called modmail or run my setupmodmail command and I will set up the channel for you. Note that if you use the command, you need Manage Server permissions and I need Manage channel permissions.", inline=False)
    embed.add_field(name="More info", value="The Github repo has a README file for detailed information: https://codeberg.org/MatthewsDevelopment/Modmail.py", inline=False)
    await ctx.send(embed=embed)

# Change this to your actual Discord user IDs
matthewdevstaff = [815684414045552680, 724723809218723970]

@client.command()
async def status(ctx, value="", *, statustext):
    if ctx.author.id in matthewdevstaff:
        if value == "watch":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
        if value == "listen":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
        if value == "play":
            await client.change_presence(activity=discord.Game(name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
        if value == "custom":
            await client.change_presence(activity=discord.CustomActivity(name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
    else:
        await ctx.send("Only Matthews Development Staff members can use this command")
        return

@client.command()
async def streamstatus(ctx, statusurl, *, statustext):
    if ctx.author.id in matthewdevstaff:
        await client.change_presence(activity = discord.Streaming(name=f"{statustext}", url=f"{statusurl}"))
    else:
        await ctx.send("Only Matthews Development Staff members can use this command")
        return





TOKEN = os.getenv("DISCORDBOTTOKEN")
client.run(TOKEN)
