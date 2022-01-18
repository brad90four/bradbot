from loguru import logger
from nextcord.ext import commands

import exts
from constants import EXTENSIONS


class Extension(commands.Converter):
    """Make sure extension exists."""

    async def convert(self, ctx: commands.Context, argument: str) -> str:
        """Return a valid extension name."""
        argument = argument.lower()
        if argument in EXTENSIONS:
            return argument
        elif (qualified_arg := f"{exts.__name__}.{argument}") in EXTENSIONS:
            return qualified_arg


class Extensions(commands.Cog):
    """Manage extensions running on the bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="extensions", aliases=("ext", "exts", "c", "cogs"), invoke_without_command=True)
    async def extensions_group(self, ctx: commands.Context) -> None:
        """Reload and list extensions."""
        await ctx.send_help(ctx.command)

    @extensions_group.command(name="reload", aliases=("r",), root_aliases=("reload",))
    async def reload_command(self, ctx: commands.Context, extension: Extension) -> None:
        """Reload extension."""
        logger.debug(f"Command `{ctx.invoked_with}` used by {ctx.author}.")
        try:
            logger.debug(f"{extension = }")
            self.bot.reload_extension(extension)
            msg = f":ok_hand: {extension} reloaded."
        # except commands.errors.ExtensionNotLoaded:
        #     self.bot.load_extension(extension)
        except Exception as e:
            logger.debug(f"Extension {extension} failed to reload.")
            logger.exception(e)
            msg = "Error"

        await ctx.send(msg)


def setup(bot: commands.Bot) -> None:
    """Load the Extensions cog."""
    bot.add_cog(Extensions(bot))
