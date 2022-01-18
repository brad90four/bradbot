import asyncio
import pkgutil
import importlib
import os
import inspect
import socket
from aiohttp import AsyncResolver, ClientSession, TCPConnector
from pathlib import Path
from dotenv import load_dotenv
from collections.abc import Iterator
from typing import NoReturn

import nextcord

from nextcord.ext import commands
from loguru import logger

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
        # self.http_session = ClientSession(
        #     connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET)
        # )
        self.name = "Bradbot"
        self.dev_log = int(DEV_LOG)
        logger.debug(f"{self.dev_log = }")
        #self.loop.create_task(self.send_log(title=self.name, details="Connected!"))


    # async def send_log(self, title: str, details: str = None) -> None:
    #     """Send an embed message to the devlog channel."""

    #     devlog = self.get_channel(int(self.dev_log))
    #     logger.debug(f"{devlog = }")
    #     if not devlog:
    #         logger.debug(f"'dev_log' channel not found: {self.dev_log}")
    #         try:
    #             devlog = await self.fetch_channel(os.environ.get("DEV_LOG"))
    #         except nextcord.HTTPException as discord_exc:
    #             logger.exception("Fetch failed", exc_info=discord_exc)
    #             return


    #     embed = nextcord.Embed(description=details)
    #     embed.set_author(name=title)

    #     await devlog.send(embed=embed)

    def add_cog(self, cog: commands.Cog) -> None:
        """
        Delegate to super to register `cog`.
        This only serves to make the info log, so that extensions don't have to.
        """
        super().add_cog(cog)
        logger.info(f"Cog loaded: {cog.qualified_name}")
    



bot = Bradbot(command_prefix="!", DEV_LOG=DEV_LOG)


@bot.event
async def on_ready():
    logger.debug("'on_ready' event hit")
    logger.debug(f"{bot = }")

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