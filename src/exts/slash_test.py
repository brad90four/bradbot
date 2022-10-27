from loguru import logger
from nextcord import Interaction, slash_command
from nextcord.ext import commands

from util.constants import GUILD_ID


class SlashTester(commands.Cog):
    """Testing slash command implementation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[int(GUILD_ID)], description="Echo command")
    async def slash_echo(self, interaction: Interaction, arg: str):
        """Testing a slash echo command"""
        logger.debug(f"Echoing: {arg}")
        await interaction.response.send_message(f"{arg}")


def setup(bot: commands.Bot) -> None:
    """Load the SlashTester cog."""
    bot.add_cog(SlashTester(bot))
