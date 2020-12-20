"""
Quote Bot
Literally just quotes
Version 1.2.0
 coding done by Phoeniix, Annoying Bokoblin, ElectronDev.
"""

"""
CODE TO COPY-PASTE WHEN CREATING A NEW COG:

import discord
from discord.ext import commands

class CogName(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(CogName(client))
"""

import discord
from discord.ext import commands, tasks
import datetime
import json
import sys
import traceback
import os
import sys
from itertools import cycle

# CONSTANT VARIABLES
ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "data")
sys.path.append(ROOT_DIR)
# TOKENS
MAIN_TOKEN = "NzMyNjgzOTgwMzUyMTI3MDM4.Xw4LOg.Rn4JWrKTUQnAllGUtf1E4ASLfiY"
TEST_TOKEN = "NzMyNjg4ODY5OTA0MDg5MjE5.Xw4PuA.99GFI8iJK76_YbbcvO20ZjJk_4E"
# THIS DEFINES WHICH BOT SHOULD RUN, ONLY PUT MAIN_TOKEN IF RELEASING
TOKEN = MAIN_TOKEN
# PLEASE DO BE CAREFUL WITH THAT SHIT YOU HEAR ME
BOT_OWNER_IDS = [285832267216191498, 370951560085372928, 303069460359675905, 362546658048868353]
DEFAULT_PREFIX = "*"
# Channel IDs
ERROR_LOG_ID = 732683641024413851
COMMAND_LOG_ID = 732683641024413852
DM_LOG_ID = 732683641024413853
SERVERS_JOINED_LOG_ID = 732683641024413854
TEST_TEST_ID = 732683641024413848
MAIN_TEST_ID = 732683641024413849
ACTIVITY_TYPES = {"playing":discord.ActivityType.playing, "streaming":discord.ActivityType.streaming, "watching":discord.ActivityType.watching, "listening":discord.ActivityType.listening}
intents = discord.Intents.default()
intents.members = True
class Client(commands.Bot):
    async def on_ready(self):
        #Define all constants which require the bot to be active OR that we need across all cogs here. to call them later, do client.[CONST] or self.client.[CONST] in a cog.
        self.ROOT_DIR = ROOT_DIR
        self.DATA_DIR = DATA_DIR
        self.BOT_OWNER_IDS = BOT_OWNER_IDS
        self.ERROR_LOG = await self.fetch_channel(ERROR_LOG_ID)
        self.COMMAND_LOG = await self.fetch_channel(COMMAND_LOG_ID)
        self.DM_LOG = await self.fetch_channel(DM_LOG_ID)
        self.SERVERS_JOINED_LOG = await self.fetch_channel(SERVERS_JOINED_LOG_ID)
        self.TEST_TEST = await self.fetch_channel(TEST_TEST_ID)
        self.MAIN_TEST = await self.fetch_channel(MAIN_TEST_ID)
        self.starttime = datetime.datetime.utcnow()

        with open(os.path.join(DATA_DIR, "status.json"),"r") as f:
            self.STATUSES = json.load(f)
        if len(self.STATUSES) > 0:
            self.STATUSES = cycle(self.STATUSES)
            statuschange.start(self)
        print("------------------")
        print(self.starttime)
        print("Logged in as: {}".format(self.user))
        print("Default prefix: {}".format(DEFAULT_PREFIX))
        print("-------------------")
        print("Servers: {}".format(len(self.guilds)))
        print("Users: {}".format(len(self.users)))
        print("-------------------")

async def _get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX, "")(client, message)
    with open(os.path.join(DATA_DIR, "prefixes.json"), "r") as f:
        prefixes = json.load(f)
    prefix = prefixes.get(str(message.guild.id), DEFAULT_PREFIX)
    return commands.when_mentioned_or(prefix)(client, message)

client = Client(command_prefix=_get_prefix, case_insensitive=True, owner_ids=BOT_OWNER_IDS, help_command=None,intents=intents)

# EVENTS

async def _msglog(msg):
    embed=discord.Embed(title=f"DM from {msg.author}", colour=discord.Colour.blue(), description=f"```{msg.content}```")
    embed.set_thumbnail(url=msg.author.avatar_url)
    embed.set_footer(text=f"User ID: {msg.author.id}")
    embed.timestamp = datetime.datetime.utcnow()
    await client.DM_LOG.send(embed=embed)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    elif TOKEN == MAIN_TOKEN:
        if not msg.guild:
            await _msglog(msg)
            await client.process_commands(msg)
        elif not msg.channel.id == TEST_TEST_ID:
            await client.process_commands(msg)
        else:
            return
    elif TOKEN == TEST_TOKEN:
        if msg.channel and msg.channel.id == TEST_TEST_ID:
            await client.process_commands(msg)
        else:
            return

@client.event
async def on_guild_join(guild):
    if TOKEN == MAIN_TOKEN:
        try:
            guild_url = await guild.create_invite(unique=False, reason="Created for bot logging purposes.")
        except:
            guild_url = None
        if guild_url:
            embed = discord.Embed(
                title="\N{INBOX TRAY} Server Joined: {}".format(guild.name),
                colour=discord.Colour.green(),
                description="```We now have a total of {0} servers and {1} users ({2} users gained).```".format(len(client.guilds), len(client.users), len(guild.members)),
                url=guild_url)
        else:
            embed = discord.Embed(
                title="\N{INBOX TRAY} Server Joined: {}".format(guild.name),
                colour=discord.Colour.green(),
                description="```We now have a total of {0} servers and {1} users ({2} users gained).```".format(len(client.guilds), len(client.users), len(guild.members)))
        embed.set_footer(text="Server ID: {}".format(guild.id))
        embed.set_thumbnail(url=guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        await client.SERVERS_JOINED_LOG.send(embed=embed)
        # Guild prefix add
        with open(os.path.join(DATA_DIR, "prefixes.json"), "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = DEFAULT_PREFIX
        with open(os.path.join(DATA_DIR, "prefixes.json"), "w") as f:
            json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    if TOKEN == MAIN_TOKEN:
        embed = discord.Embed(
            title="\N{OUTBOX TRAY} Server Left: {}".format(guild.name),
            colour=discord.Colour.red(),
            description="```We now have a total of {0} servers and {1} users ({2} users lost).```".format(len(client.guilds), len(client.users), len(guild.members)))
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text="Server ID: {}".format(guild.id))
        embed.timestamp = datetime.datetime.utcnow()
        await client.SERVERS_JOINED_LOG.send(embed=embed)
        # Guild prefix remove
        with open(os.path.join(DATA_DIR, "prefixes.json"), "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open(os.path.join(DATA_DIR, "prefixes.json"), "w") as f:
                json.dump(prefixes, f, indent=4)

@client.event
async def on_command_completion(ctx):
    # Increase total commands counter
    with open(os.path.join(DATA_DIR, "counters.json"), "r") as f:
        counters = json.load(f)
    counters["commands_since_creation"] += 1
    with open(os.path.join(DATA_DIR, "counters.json"), "w") as f:
        json.dump(counters, f, indent=4)
    # Command log
    if not ctx.guild:
        embed = discord.Embed(title=f"DM command used", colour=discord.Colour.orange(), description=f"```{ctx.message.content}```")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Command context", value=f"""```Author: {ctx.message.author} ({ctx.message.author.id})```""")
        embed.set_footer(text="Total commands used: {0}".format(counters["commands_since_creation"]))
        embed.timestamp = datetime.datetime.utcnow()
        await client.COMMAND_LOG.send(embed=embed)
    else:
        try:
            guild_url = await ctx.channel.create_invite(unique=False, reason="Created for bot error logging purposes.")
        except:
            guild_url = "Missing permissions"
        embed = discord.Embed(title=f"Command used", colour=discord.Colour.orange(), description=f"```{ctx.message.content}```", url=ctx.message.jump_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Command context", value=f"""```Author: {ctx.message.author} ({ctx.message.author.id})\nChannel: #{ctx.channel.name} ({ctx.channel.id})\nServer: "{ctx.guild.name}" ({ctx.guild.id})\nServer invite: {guild_url}```""")
        embed.set_footer(text="Total commands used: {0}".format(counters["commands_since_creation"]))
        embed.timestamp = datetime.datetime.utcnow()
        await client.COMMAND_LOG.send(embed=embed)

@client.event
async def on_command_error(ctx, error):

    # if isinstance(error, commands.CheckFailure):
    #     embed = discord.Embed(title="You cannot use this command.")
    #     await ctx.send(embed=embed)
    # elif isinstance(error, commands.MissingRequiredArgument):
    #     embed = discord.Embed(title=f"Incorrect command usage: A required argument is missing. \nTry using `{ctx.prefix}help`")
    #     await ctx.send(embed=embed)
    # elif isinstance(error, commands.TooManyArguments):
    #     embed = discord.Embed(title=f"Incorrect command usage: Too many arguments passed. \nTry using `{ctx.prefix}help`")
    #     await ctx.send(embed=embed)
    # elif isinstance(error, commands.BadArgument):
    #     embed = discord.Embed(title=f"Incorrect command usage: An argument was not passed properly. \nTry using `{ctx.prefix}help`")
    #     await ctx.send(embed=embed)
    # else:
    print(error, file=sys.stderr)
    if TOKEN==MAIN_TOKEN:
        channel_to_use = client.ERROR_LOG
    else:
        channel_to_use = ctx
    try:
        guild_url = await ctx.channel.create_invite(unique=False, reason="Created for bot error logging purposes.")
    except:
        guild_url = "Missing permissions"
    embed=discord.Embed(title="Traceback exception", colour=discord.Colour.red(), description="```{}```".format(ctx.message.content), url=ctx.message.jump_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name="Context Info", value=f"""```Author: {ctx.message.author} ({ctx.message.author.id})\nChannel: #{ctx.channel.name} ({ctx.channel.id})\nServer: "{ctx.guild.name}" ({ctx.guild.id})\nServer invite: {guild_url}```""", inline=False, )
    embed.add_field(name="Traceback info", value="```py\n{}```".format(error), inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await channel_to_use.send(embed=embed)

# TASK LOOPS

@tasks.loop(seconds=15)
async def statuschange(client):
    if isinstance(client.STATUSES, list):
        if len(client.STATUSES) <= 0:
            statuschange.cancel()
        client.STATUSES = cycle(client.STATUSES)
    status = next(client.STATUSES)
    await client.change_presence(activity=discord.Activity(name=status["name"], type=ACTIVITY_TYPES[status["type"]], url=(status["url"] or "https://zelquest.com/")))

# HELP COMMAND

@client.command(help="Shows a list of commands and detailed command descriptions.",
                usage="(<cog>|<command>)")
async def help(ctx):
    help_embed = discord.Embed(title="Help Menu", colour=discord.Colour.green())
    help_embed.add_field(name=f"{ctx.prefix}quote", value="Generates a random AI-generated quote from the awesome inspirobot.me!", inline=False)
    help_embed.add_field(name=f"{ctx.prefix}invite", value="Sends an invite for the bot")
    help_embed.add_field(name=f"{ctx.prefix}prefix [new]", value="Changes the guild prefix of the bot (admins only)")
    help_embed.add_field(name=f"{ctx.prefix}ping", value="You know what that does already, don't you?")
    await ctx.send(embed=help_embed)
    


for filename in os.listdir(os.path.join(ROOT_DIR, "cogs")):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.is_owner()
async def load(ctx, cog):
    client.load_extension(f"cogs.{cog}")
    embed=discord.Embed(title=f"The `{cog}` cog has been loaded")
    await ctx.send(embed=embed)
@client.command()
@commands.is_owner()
async def unload(ctx, cog):
    client.unload_extension(f"cogs.{cog}")
    embed=discord.Embed(title=f"The `{cog}` cog has been unloaded")
    await ctx.send(embed=embed)
@client.command(aliases=["r","re"])
@commands.is_owner()
async def reload(ctx, cog):
    client.reload_extension(f"cogs.{cog}")
    embed=discord.Embed(title=f"The `{cog}` cog has been reloaded")
    await ctx.send(embed=embed)

client.run(TOKEN)
