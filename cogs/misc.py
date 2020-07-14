import discord
from discord.ext import commands
import datetime

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(help="Use this command to make sure the bot is alive. Sends the bot's reaction time.")
    async def ping(self, ctx):
        latency = datetime.datetime.utcnow()-ctx.message.created_at
        await ctx.send(":ping_pong:  Pong! - {0}s".format(latency.total_seconds()))
    
def setup(client):
    client.add_cog(Misc(client))