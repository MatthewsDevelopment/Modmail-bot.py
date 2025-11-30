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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="My DMs"))
    print("Modmail-Bot is Ready")

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
    embed = discord.Embed(title="Modmail Bot by Matthews Development", description="Here is my list of Commands", color=(58101))
    embed.add_field(name="General", value=f"{BOTPREFIX}help - This message\n{BOTPREFIX}ping - Get the Bot latency\n{BOTPREFIX}setupguide - Instructions on how to setup the modmail system\n{BOTPREFIX}setupmodmail - Setup the Modmail channel.", inline=False)
    embed.add_field(name="Source Code", value="https://gitlab.com/MatthewsDevelopment/modmailpy", inline=False)
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
        await ctx.send("AN ERROR HAS OCCURED\nI do not have permissions to manage channels. Please make sure I have the **MANAGE_CHANNELS** permission and try again")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('AN ERROR HAS OCCURED\nYou need to have the **MANAGE_GUILD** permission to use this command.')
    else:
        raise error

@client.command()
async def setupguide(ctx):
    embed = discord.Embed(title="Modmail Bot", description="Here is instructions on how to setup the basic modmail system", color=(58101))
    embed.add_field(name="Steps", value="After inviting the bot, create a channel called modmail or run my setupmodmail command and I will set up the channel for you. Note that if you use the command, you need Manage Server permissions and I need Manage channel permissions.", inline=False)
    embed.add_field(name="More info", value="The Github repo has a README file for detailed information: https://gitlab.com/MatthewsDevelopment/modmailpy", inline=False)
    await ctx.send(embed=embed)





TOKEN = os.getenv("DISCORDBOTTOKEN")
client.run(TOKEN)
