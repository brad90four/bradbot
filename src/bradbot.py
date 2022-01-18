import importlib
import inspect
import os
import pkgutil
from collections.abc import Iterator
from pathlib import Path
from typing import NoReturn

import nextcord
from dotenv import load_dotenv
from loguru import logger
from nextcord.ext import commands

import exts

path = Path(__file__)
parent = path.parents[1]
load_dotenv(parent.joinpath(".env"))
DEV_LOG = os.environ.get("DEV_LOG")


class Bradbot(commands.Bot):
    """
    Bradbot core.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Bradbot"
        self.dev_log = int(DEV_LOG)

    def add_cog(self, cog: commands.Cog) -> None:
        """
        Delegate to super to register `cog`.
        This only serves to make the info log, so that extensions don't have to.
        """
        super().add_cog(cog)
        logger.info(f"Cog loaded: {cog.qualified_name}")


bot = Bradbot(command_prefix="~", DEV_LOG=DEV_LOG)


@bot.event
async def on_ready():
    logger.info("'on_ready' event hit")

    devlog = bot.get_channel(bot.dev_log)
    embed = nextcord.Embed(title="Bradbot", description="A small, personal Bradbot")
    await devlog.send(embed=embed)


def unqualify(name: str) -> str:
    """Return an unqualified name given a qualified module/package `name`."""
    return name.rsplit(".", maxsplit=1)[-1]


def walk_extensions() -> Iterator[str]:
    """Yield extension names from the bot.exts subpackage."""

    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)  # pragma: no cover

    for module in pkgutil.walk_packages(exts.__path__, f"{exts.__name__}.", onerror=on_error):
        if unqualify(module.name).startswith("_"):
            # Ignore module/package names starting with an underscore.
            continue

        if module.ispkg:
            imported = importlib.import_module(module.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                # If it lacks a setup function, it's not an extension.
                continue

        yield module.name


for ext in walk_extensions():
    bot.load_extension(ext)


token = os.environ.get("TOKEN")
bot.run(token)
