import discord
from discord.ext import commands
import datetime
import requests
import socket
ip = "192.168.1.141"
port = 30201
externalserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
externalserver.bind((ip,port))
class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
    def updateserver(self):
        while True:
            externalserver.settimeout(60)
            try:
                externalserver.listen()
                conn, addr = externalserver.accept() 
            except:continue
            stmessage="Bot Online | Uptime: {}".format(str(datetime.datetime.utcnow()-self.client.starttime).replace(str(datetime.datetime.utcnow()-self.client.starttime)[-7:],""))
            conn.send(stmessage).encode()
    @commands.command()
    async def on_ready(self, ctx):
        usthread=threading.Thread(target=Misc.updateserver,args=(self,))
        await asyncio.sleep(5)
        usthread.start()
    @commands.command()
    async def ping(self, ctx):
        latency = datetime.datetime.utcnow()-ctx.message.created_at
        await ctx.send(":ping_pong:  Pong! - {0}s".format(latency.total_seconds()))
        
    @commands.command()
    async def quote(self, ctx):
        await ctx.trigger_typing()
        try:
            ag = {"User-Agent":"Mozilla/5.0"}
            req = requests.get("http://inspirobot.me/api?generate=true",headers=ag)
            if req.status_code == 200:
                embed = discord.Embed(colour=discord.Colour.green())
                embed.set_footer(text="Created using inspirobot.me")
                embed.set_image(url=req.text)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Sadly, an error happened. Please wait a few minutes/hours (?) before getting inspired :pray:")
        except:
            await ctx.send("Command failed successfully, please try again!")
            
    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invites!", description="Either invite the bot to your server, or join our support server using these links:")
        embed.add_field(name="Add the bot to your server!", value="https://discord.com/api/oauth2/authorize?client_id=732683980352127038&permissions=51201&scope=bot")
        embed.add_field(name="Join our server!", value="https://discord.gg/GZFsWrm")
        await ctx.send(embed=embed)
    
    
def setup(client):
    client.add_cog(Misc(client))
