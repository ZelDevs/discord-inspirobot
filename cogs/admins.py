import discord
from discord.ext import commands
import json
import typing
import os

class Admins(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.id in self.client.BOT_OWNER_IDS
    
    @commands.command(aliases=['setprefix'],
                      help="Changes the guild prefix to the specified one, if there is no prefix specified then it just returns the current guild prefix.",
                      usage="(<prefix>)")
    async def prefix(self, ctx, prefix=None):
        with open(os.path.join(self.client.DATA_DIR, "prefixes.json"), "r") as f:
            prefixes = json.load(f)
        if prefix==None:
            await ctx.send("The current prefix is `{}` (but mentioning me also works!)".format(prefixes[str(ctx.guild.id)]))
        else:
            prefixes[str(ctx.guild.id)] = prefix
            await ctx.send("New prefix is `{}` (mentioning me also works!)".format(prefix))
            with open(os.path.join(self.client.DATA_DIR, "prefixes.json"), "w") as f:
                json.dump(prefixes, f, indent=4)
            
def setup(client):
    client.add_cog(Admins(client))