import discord
from discord.ext import commands
from discord import app_commands
import datetime
import requests
import asyncio


class Misc(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(5)

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        latency = datetime.datetime.now(
            datetime.timezone.utc)-interaction.created_at
        await interaction.response.send_message(":ping_pong:  Pong! - {0}s".format(latency.total_seconds()))

    @app_commands.command()
    async def quote(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            ag = {"User-Agent": "Mozilla/5.0"}
            req = requests.get(
                "http://inspirobot.me/api?generate=true", headers=ag)
            if req.status_code == 200:
                embed = discord.Embed(colour=discord.Colour.green())
                embed.set_footer(text="Created using inspirobot.me")
                embed.set_image(url=req.text)
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("Sadly, an error happened. Please wait a few minutes/hours (?) before getting inspired :pray:")

        except Exception as e:
            await interaction.followup.send("Command failed successfully, please try again!")

    @app_commands.command()
    async def invite(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Invites!", description="Either invite the bot to your server, or join our support server using these links:")
        embed.add_field(name="Add the bot to your server!",
                        value="https://discord.com/api/oauth2/authorize?client_id=732683980352127038&permissions=51201&scope=bot")
        embed.add_field(name="Join our support server!",
                        value="https://discord.gg/mt5wauZTnD")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def support(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Support link!", description="Join our support server using this link:")
        embed.add_field(name="Join our support server!",
                        value="https://discord.gg/mt5wauZTnD")
        await interaction.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(Misc(client))
