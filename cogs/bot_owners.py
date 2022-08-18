import discord
from discord.ext import commands
from discord import app_commands
import json
import os

ACTIVITY_TYPES = {"playing": discord.ActivityType.playing, "streaming": discord.ActivityType.streaming,
                  "watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening}


class BotOwners(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    def is_owner():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id in interaction.client.BOT_OWNER_IDS
        return app_commands.check(predicate)

    # aliases=['files', 'data'],
    @app_commands.command(description="Sends you a copy of the bot's data files in DM")
    @is_owner()
    async def downfiles(self, interaction: discord.Interaction):
        for file in os.scandir(self.client.DATA_DIR):
            await interaction.user.send(file=discord.File(file))
    # .", usage="add|remove [<name>|<name> <type> <url>]"

    async def option_autocomplete(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=option, value=option) for option in ["add", "remove"]]

    async def activity_autocomplete(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=option, value=option) for option in ACTIVITY_TYPES.keys()]

    @app_commands.command(description="Modify the bot's custom status")
    @is_owner()
    @app_commands.autocomplete(option=option_autocomplete, activity_type=activity_autocomplete)
    async def status(self, interaction, option: str, name: str, activity_type: str = "", url: str = ""):
        with open(os.path.join(self.client.DATA_DIR, "status.json"), "r") as f:
            statuses: list = json.load(f)
        if option.lower() == "add":
            if len(name) <= 0 or activity_type not in list(ACTIVITY_TYPES):
                raise commands.BadArgument
            statuses.append({"name": name, "type": activity_type, "url": url})
            option += "e"
        elif option.lower() == "remove":
            foundName = False
            for status in statuses:
                if status["name"] == name:
                    foundName = True
                    statuses.remove(status)
            if not foundName:
                await interaction.response.send_message("That status does not exist.")
                return
        else:
            raise commands.BadArgument
        with open(os.path.join(self.client.DATA_DIR, "status.json"), "w") as f:
            json.dump(statuses, f)
        self.client.STATUSES = statuses
        await interaction.response.send_message("Status {}{}d successfully.".format(option, "e" if option.lower() == "add" else ""))

    # usage="<channel> <content*>",
    @app_commands.command(description="Sends a message in a specified channel")
    async def say(self, interaction, location: discord.TextChannel, content: str):
        location = location.replace("<#", "")
        location = location.replace(">", "")
        try:
            channel = await self.client.fetch_channel(location)
        except:
            raise commands.BadArgument
        await channel.send(content)
        await interaction.response.send_message("Sent in {0} successfully.".format(channel.name))

    @app_commands.command(description="Sends a message to a specified user")
    async def dm(self, ctx, user: discord.User, *, content: str):
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


async def setup(client):
    await client.add_cog(BotOwners(client), guild=client.SUPPORT_GUILD)
