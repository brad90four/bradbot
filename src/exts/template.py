# extension template
# imports at the top, will follow `isort` to keep the order
from datetime import datetime
from typing import Optional

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
    # doc info: https://nextcord.readthedocs.io/en/latest/ext/commands/api.html#commands
    @commands.command(name="template")
    async def template(self, ctx: commands.Context, *, user_input: Optional[str] = None) -> None:
        """
        Template command to show a simple extension script setup.

        Args:
            ctx (commands.Context): A variable passed to the command using the context that it was called in.
        """
        # add a log statement to show helpful context items - use only for development
        # ctx attributes: https://nextcord.readthedocs.io/en/latest/ext/commands/api.html#context
        # args, author, bot, channel, cog, command, command_failed, guild, invoked_parents,
        # invoked_subcommand, invoked_with, kwargs, me, message, prefix, subcommand_passed,
        # valid, voice_client
        logger.debug(f"{ctx.args = }\n{ctx.channel = }\n{ctx.prefix = }")

        # can accept user input after the command invocation
        logger.debug(
            f"The user {ctx.author} passed the input "
            f"{user_input if user_input else 'no-input-given'} to the command."
        )

        # create an Embed in order to send it to Discord
        # Embed key word paramaters: https://nextcord.readthedocs.io/en/latest/api.html#embed
        # title, type, description, url, timestamp, color
        embed = Embed(
            title="Template Command - Example Embed",
            type="rich",
            description="An embed to show what parameters can be used.\n"
            f"Optional user_input: `{user_input if user_input else 'no-input-given'}`",
            url="https://nextcord.readthedocs.io/en/latest/api.html#embed",
            timestamp=datetime.now(),
            color=Colour.random(),
        )

        # send Embed to the context that invoked it
        await ctx.send(embed=embed)


# define a setup function to indicate that this script is an extension
def setup(bot: commands.Bot) -> None:
    """Load the Template cog."""
    bot.add_cog(Template(bot))
