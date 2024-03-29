import feedparser
from loguru import logger
from nextcord import Embed
from nextcord.ext import commands


class TrailStatus(commands.Cog):
    """Send an embed about the bot's ping."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="trail_status", aliases=("trails", "trailstatus", "ts"))
    async def trail_status(self, ctx: commands.Context) -> None:
        """Get the current trail status."""
        logger.debug(f"Command `{ctx.invoked_with}` used by {ctx.author}.")
        try:
            esnp_rss = feedparser.parse(
                "https://parks.hamiltontn.gov/RSSFeed.aspx?ModID=63&CID=Enterprise-South-Nature-Park-Bike-Trails-8"
            )
            if len(esnp_rss["entries"]) == 0:
                embed = Embed(
                    title="Trail Status for ESNP :man_mountain_biking:",
                    description="No updates.",
                )

                await ctx.send(embed=embed)
                logger.error("RSS feed does not have an entry")
                return
        except Exception as e:
            logger.debug("Error occured while fetching ESNP RSS.")
            logger.exception(e)
            return

        logger.debug(esnp_rss["entries"])
        updated_date = esnp_rss["entries"][0]["published"]
        status = esnp_rss["entries"][0]["title"]
        # logger.debug(f"{updated_date = }\n{status = }")

        embed = Embed(
            title="Trail Status for ESNP :man_mountain_biking:",
            description=f"Updated: {updated_date}\nStatus: {status}",
        )

        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Load the TrailStatus cog."""
    bot.add_cog(TrailStatus(bot))
