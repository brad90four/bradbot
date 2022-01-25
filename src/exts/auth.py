import os
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key
from loguru import logger
from nextcord import Embed
from nextcord.ext import commands

path = Path(__file__)
parent = path.parents[2]
dotenv_file = parent.joinpath(".env")
load_dotenv(dotenv_file)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")


refresh_url = "https://www.strava.com/api/v3/oauth/token"

refresh_data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN,
}


class RefreshStrava(commands.Cog):
    """Refresh the access code for the strava API."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="refresh_strava",
        aliases=(
            "rs",
            "auth",
        ),
    )
    async def refresh_strava(self, ctx: commands.Context) -> None:
        logger.debug(f"Command `{ctx.invoked_with}` used by {ctx.author}.")
        refresh_code = requests.post(refresh_url, data=refresh_data)
        logger.debug(f"{refresh_code.status_code = }")
        access_code = refresh_code.json()["access_token"]
        set_key(dotenv_file, "ACCESS_CODE", access_code)

        icon = self.bot.user.display_avatar.url
        embed = Embed(
            title="Strava Access Code Refreshed",
            description="Success",
        )

        embed.set_author(name=self.bot.name, icon_url=icon)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Load the RefreshStrava cog."""
    bot.add_cog(RefreshStrava(bot))
