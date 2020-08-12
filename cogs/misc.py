import discord
from discord.ext import commands
import datetime
import requests

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def ping(self, ctx):
        latency = datetime.datetime.utcnow()-ctx.message.created_at
        await ctx.send(":ping_pong:  Pong! - {0}s".format(latency.total_seconds()))
        
    @commands.command()
    async def quote(self, ctx):
        req = requests.get("http://inspirobot.me/api?generate=true")
        if req.status_code == 200:
            embed = discord.Embed(colour=discord.Colour.green())
            embed.set_footer(text="Created using inspirobot.me")
            embed.set_image(url=req.text)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sadly, an error happened. Please wait a few minutes/hours (?) before getting inspired :pray:")
    
    
def setup(client):
    client.add_cog(Misc(client))