import discord
from discord.ext import commands
import json
import os

ACTIVITY_TYPES = {"playing":discord.ActivityType.playing, "streaming":discord.ActivityType.streaming, "watching":discord.ActivityType.watching, "listening":discord.ActivityType.listening}

class BotOwners(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    async def cog_check(self, ctx):
        return ctx.author.id in self.client.BOT_OWNER_IDS

    @commands.command(aliases=['files','data'],help="Sends you a copy of the bot's data files in DM")
    async def downfiles(self, ctx):
        for file in os.scandir(self.client.DATA_DIR):
            await ctx.author.send(file=discord.File(file))

    @commands.command(help="Modify the bot's custom status.",
                      usage="add|remove [<name>|<name> <type> <url>]")
    async def status(self, ctx, option: str, name: str, type: str="", url: str=""):
        with open(os.path.join(self.client.DATA_DIR, "status.json"),"r") as f:
            statuses = json.load(f)
        if option.lower() == "add":
            if len(name) <= 0 or type not in list(ACTIVITY_TYPES):
                raise commands.BadArgument
            statuses.append({"name":name, "type":type, "url":url})
            option += "e"
        elif option.lower() == "remove":
            foundName = False
            for status in statuses:
                if status["name"] == name:
                    foundName = True
                    statuses.remove(status)
            if not foundName:
                await ctx.send("That status does not exist.")
                return
        else:
            raise commands.BadArgument
        with open(os.path.join(self.client.DATA_DIR, "status.json"), "w") as f:
            json.dump(statuses, f)
        self.client.STATUSES = statuses
        await ctx.send("Status {}d successfully.".format(option))
        
    @commands.command(usage="<channel> <content*>",
                      help="Sends a message in a specified channel")
    async def say(self, ctx, location: discord.TextChannel, content):
        await location.send(content)
        await ctx.send("Message sent successfully.")
        
    @commands.command(usage="<user> <content*>",
                      help="Sends a message to a specified user")
    async def dm(self, ctx, user: discord.Member, *, content):
        if not user:
            raise commands.BadArgument
        await user.send(content)
        await ctx.send("DMed {0} successfully.".format(user.name))
    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No message to send was specified")
        elif isinstance(error, discord.HTTPException):
            await ctx.send("Failed to send DM.")        
        elif isinstance(error, commands.BadArgument):
            await ctx.send("I could not find that member.")
            
def setup(client):
    client.add_cog(BotOwners(client))