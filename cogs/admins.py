import discord
from discord.ext import commands
from discord import app_commands
import json
import typing
import os


class Admins(commands.Cog):
    def __init__(self, client):
        self.client = client

    def is_admin():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.guild_permissions.administrator or interaction.user.id in interaction.client.BOT_OWNER_IDS
        return app_commands.check(predicate)

    @app_commands.command(
        description="Changes the guild prefix to the specified one, or showsthe current guild prefix.",
    )
    @is_admin()
    async def prefix(self, interaction: discord.Interaction, prefix: typing.Optional[str] = None):
        with open(os.path.join(self.client.DATA_DIR, "prefixes.json"), "r") as f:
            prefixes = json.load(f)
        if prefix == None:
            await interaction.response.send_message("The current prefix is `{}` (but mentioning me also works!)".format(prefixes[str(interaction.guild.id)]))
        else:
            prefixes[str(interaction.guild.id)] = prefix
            await interaction.response.send_message("New prefix is `{}` (mentioning me also works!)".format(prefix))
            with open(os.path.join(self.client.DATA_DIR, "prefixes.json"), "w") as f:
                json.dump(prefixes, f, indent=4)


async def setup(client: commands.Bot):
    await client.add_cog(Admins(client), guild=discord.Object(id=732683640525553815))
