import importlib
import inspect
import os
import pkgutil
from collections.abc import Iterator
from pathlib import Path
from typing import NoReturn

from dotenv import load_dotenv

import exts

path = Path(__file__)
parent = path.parents[2]
load_dotenv(parent.joinpath(".env"))
GUILD_ID = os.environ.get("GUILD_ID")


SOURCE_HOME_PAGE = "https://github.com/brad90four/bradbot"


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


EXTENSIONS = frozenset(walk_extensions())
