from loguru import logger
from nextcord import Embed
from nextcord.ext import commands

import util.constants


class Source(commands.Cog):
    "Send an embed to `bradbot`'s github repo."

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="source", aliases=("src",))
    async def source(self, ctx: commands.Context) -> None:
        """Display the github source code."""
        logger.debug(f"Command `{ctx.invoked_with}` used by {ctx.author}.")
        icon = self.bot.user.display_avatar.url
        embed = Embed(
            title="`bradbot`'s source code",
            description=f"Repository home page: [source]({util.constants.SOURCE_HOME_PAGE})",
        )
        embed.set_author(name=self.bot.name, icon_url=icon)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Load the Source cog."""
    bot.add_cog(Source(bot))
