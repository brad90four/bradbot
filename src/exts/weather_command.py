import datetime
import os
from pathlib import Path
from pprint import pprint

import iso3166
import requests
from dotenv import load_dotenv
from loguru import logger
from nextcord import Color, Embed, Interaction, SlashOption, slash_command
from nextcord.ext import commands
from rapidfuzz import process

from util.constants import GUILD_ID

root_dir = Path(__file__).parents[2]
load_dotenv(root_dir.joinpath(".env"))
API_KEY = os.environ.get("WEATHER_API_KEY")
BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
PADDING = 20
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


def _select_weather_display_emoji(weather_id: int) -> str:
    """Add an emoji based on the weather ID.

    Args:
        weather_id (int): Weather ID number given by the API.

    Returns:
        display_emoji (str): The emoji for a given weather ID.
    """
    if weather_id in THUNDERSTORM:
        return "💥"
    elif weather_id in DRIZZLE:
        return "💧"
    elif weather_id in RAIN:
        return "💦"
    elif weather_id in SNOW:
        return "⛄️"
    elif weather_id in ATMOSPHERE:
        return "🌀"
    elif weather_id in CLEAR:
        return "🔆"
    elif weather_id in CLOUDY:
        return "💨"
    else:  # In case the API adds new weather codes
        return "🌈"


def _get_iso_country(input_country: str, debug: bool = False) -> str:
    """Get the ISO country code for a given country name.

    Args:
        input_country (str): Country name from user input.

    Returns:
        str: ISO country code.
    """
    try:
        if input_country.lower() in ("uk", "england"):
            country_code = "GB"
        elif input_country.lower() in ("usa", "united states"):
            country_code = "US"
        else:
            fuzzy_match_country = process.extractOne(input_country, iso3166.countries_by_name.keys())[0]
            if debug:
                logger.debug(f"{fuzzy_match_country = }")
            country_code = iso3166.countries_by_name[fuzzy_match_country].alpha2
        if debug:
            logger.debug(f"Country code: {country_code} for: {input_country}")
    except KeyError:
        logger.error(f"{input_country} is not a valid country.")
    return country_code


def _get_lat_lon(city: str, country: str, debug: bool = False) -> tuple[str]:
    """Get the latitude and longitude for a given city and country.

    Args:
        city (str): City name from user input.
        country (str): Country name from user input.
        debug (bool): Whether to display debug information.

    Returns:
        tuple[str]: Latitude and longitude.
    """
    city = city.replace(" ", "+")
    if country == "":
        geo_url = f"{GEO_URL}?q={city}&limit=5&appid={API_KEY}"
    else:
        geo_url = f"{GEO_URL}?q={city},{country}&limit=5&appid={API_KEY}"
    if debug:
        logger.debug(f"{city = }, {country = }")
        logger.debug(f"{geo_url = }")
    try:
        response = requests.get(geo_url)
    except response.status_code != 200:
        logger.critical(f"Response failed with {response.status_code}")
        raise

    data = response.json()
    if debug:
        logger.debug(data)
    try:
        lat, lon = data[0]["lat"], data[0]["lon"]
    except IndexError:
        logger.error(f"{response.status_code = }, {len(data) = }\n{data = }")
        raise
    return lat, lon


def build_weather_query(lat_lon: tuple[str], count: float = 0, units: str = "imperial") -> str:
    """Builds the url for an API request to OpenWeather's API.

    Args:
        lat_lon (tuple[str]): Latitude and Longitude of the location.
        count (float): Number of days to forecast.
        units (str): Units to use for the query.
        forecast (bool): Display the forecasted weather for the next 5 days.

    Returns:
        str: URL formatted for a call to the OpenWeather's city name endpoint.
    """
    if count > 0:
        hour_stamps = round(8 * count)  # number of 3-hour blocks to use in API call
        url = f"{FORECAST_API_URL}?lat={lat_lon[0]}&lon={lat_lon[1]}" f"&appid={API_KEY}&units={units}&cnt={hour_stamps}"
    else:
        url = f"{BASE_WEATHER_API_URL}?lat={lat_lon[0]}&lon={lat_lon[1]}" f"&appid={API_KEY}&units={units}"
    return url


def get_weather_data(query_url: str, debug: bool = False) -> dict:
    """Makes an API request to a given URL and returns the response.

    Args:
        query_url (str): URL formatted for a call to the OpenWeather's city name endpoint.
        debug (bool): Display additional output for the query.

    Returns:
        dict: JSON response from the API.
    """
    try:
        response = requests.get(query_url)
        data = response.json()
    except response.exceptions.RequestException as error:
        logger.critical(f"Response failed with {response.status_code}")
        logger.error(error)
        raise

    if debug:
        logger.debug(f"{data = }")
    return data


class Weather(commands.Cog):
    """Weather command."""

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @slash_command(guild_ids=[int(GUILD_ID)], description="Weather command")
    async def get_weather(
        self,
        interaction: Interaction,
        city: str = SlashOption(required=True),
        verbosity: bool = SlashOption(description="To turn on humidity and rainfall informaion", default=False),
        debug: bool = False,
        forecast_days: float = SlashOption(
            description="Number of days to forecast",
            required=False,
            default=0,
            choices=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
        ),
        units: str = SlashOption(
            description="Which units to use for display", default="imperial", choices=["imperial", "metric"]
        ),
        country: str = False,
    ):
        """Get the weather with some options"""

        logger.debug(f"Command `{interaction.application_command}` used by {interaction.user}.")
        _country = _get_iso_country(country, debug) if country else ""
        lat_lon = _get_lat_lon(city, _country, debug)
        query_url = build_weather_query(lat_lon, forecast_days, units)
        weather_data = get_weather_data(query_url, debug)
        logger.info(f"{'Got weather data' if weather_data else 'Empty weather data'}")

        if debug:
            logger.debug(f"{city = }, {verbosity = }, {debug = }, {forecast_days = }, {units = }, {country = }")
            pprint(weather_data)

        if forecast_days:
            city = weather_data["city"]["name"]
            weather_embed = Embed(title=f"Weather forecast information for {city}", description="")
            forecast_data = {}
            for datestamp in weather_data["list"]:
                local_time = datetime.datetime.fromtimestamp(datestamp["dt"]).strftime("%m/%d/%Y %H %p")
                forecast_data[local_time] = {
                    "temp": datestamp["main"]["temp"],
                    "weather_type": datestamp["weather"][0]["description"],
                    "weather_id": datestamp["weather"][0]["id"],
                    "humidity": datestamp["main"]["humidity"],
                    "wind_speed": datestamp["wind"]["speed"],
                }
                try:
                    forecast_data[local_time]["rain"] = round(datestamp["rain"]["3h"] * 0.0393701, 2)
                except KeyError:  # for when there is no rain
                    pass

            for datestamp in forecast_data:
                temp = forecast_data[datestamp]["temp"]
                weather_type = forecast_data[datestamp]["weather_type"]
                weather_emoji = _select_weather_display_emoji(forecast_data[datestamp]["weather_id"])
                if verbosity:
                    humidity = forecast_data[datestamp]["humidity"]
                    wind_speed = forecast_data[datestamp]["wind_speed"]
                    try:
                        rainfall = forecast_data[datestamp]["rain"]
                    except KeyError:
                        rainfall = 0
                    weather_embed.add_field(
                        name=f"{datestamp:<{PADDING}} {weather_emoji}",
                        value=f"{weather_type.capitalize():<{PADDING}}{temp}°{'F' if units == 'imperial' else 'C'}, "
                        f"{rainfall}in rain, {humidity}% humidity, {wind_speed} mph",
                        inline=False,
                    )
                else:
                    weather_embed.add_field(
                        name=f"{datestamp:<{PADDING}}",
                        value=f"{weather_emoji} {weather_type.capitalize():<{PADDING}}{temp}°"
                        f"{'F' if units == 'imperial' else 'C'}",
                        inline=False,
                    )
        else:
            city = weather_data["name"]
            temp = weather_data["main"]["temp"]
            weather_id = weather_data["weather"][0]["id"]
            weather_emoji = _select_weather_display_emoji(weather_id)
            weather_type = weather_data["weather"][0]["description"]
            if verbosity:
                weather_embed = Embed(
                    color=Color.blue(),
                    title=f"Weather for {city if city else lat_lon}",
                    description=f"{weather_emoji} "
                    f"{weather_type.capitalize():<{PADDING}}{temp}°{'F' if units == 'imperial' else 'C'}"
                    f"{rainfall}in rain, {humidity}% humidity, {wind_speed} mph",
                )
            else:
                weather_embed = Embed(
                    color=Color.blue(),
                    title=f"Weather for {city if city else lat_lon}",
                    description=f"{weather_emoji} "
                    f"{weather_type.capitalize():<{PADDING}}{temp}°{'F' if units == 'imperial' else 'C'}",
                )
        await interaction.response.send_message(embed=weather_embed)


def setup(bot: commands.Bot) -> None:
    """Load the Weather cog."""
    bot.add_cog(Weather(bot))
