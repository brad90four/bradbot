# extension template
# imports at the top, will follow `isort` to keep the order
from datetime import datetime

from loguru import logger
from nextcord import Colour, Embed
from nextcord.ext import commands


# create a commands.Cog class which will hold the command
class Template(commands.Cog):
    """Example cog for a simple bot command."""

    # initiate the Cog and create an attribute to inherit the bot
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # create a command using the @commands decorator
    @commands.command(name="template")
    async def template(self, ctx: commands.Context) -> None:
        """
        Template command to show a simple extension script setup.

        Args:
            ctx (commands.Context): A variable passed to the command using the context that it was called in.
        """
        # add a log statement to show helpful context items - use only for development
        # ctx attributes: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context
        # args, author, bot, channel, cog, command, command_failed, guild, invoked_parents,
        # invoked_subcommand, invoked_with, kwargs, me, message, prefix, subcommand_passed,
        # valid, voice_client
        logger.debug(f"{ctx.args = }\n{ctx.author = }\n{ctx.channel = }\n{ctx.prefix = }")

        # create an Embed in order to send it to Discord
        # Embed key word paramaters: https://discordpy.readthedocs.io/en/stable/api.html?highlight=embed#embed
        # title, type, description, url, timestamp, color
        embed = Embed(
            title="Template Command - Example Embed",
            type="rich",
            description="An embed to show what parameters can be used.",
            url="https://discordpy.readthedocs.io/en/stable/api.html?highlight=embed#embed",
            timestamp=datetime.now(),
            color=Colour.random,
        )

        # send Embed to the context that invoked it
        await ctx.send(embed=embed)


# define a setup function to indicate that this script is an extension
def setup(bot: commands.Bot) -> None:
    """Load the Template cog."""
    bot.add_cog(Template(bot))
