# strava vis
import os
from pathlib import Path
from pprint import pprint

import requests
from dotenv import load_dotenv

# import nextcord
# from loguru import logger
# from nextcord.ext import commands


path = Path(__file__)
parent = path.parents[2]
load_dotenv(parent.joinpath(".env"))
STRAVA_TOKEN = os.environ.get("STRAVA_TOKEN")


def get_athlete():
    """Get athlete data"""
    athlete_url = "https://www.strava.com/api/v3/athlete"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(athlete_url, headers=headers)

    print(f"{response.status_code = }")
    pprint(response.text)


def list_activities():
    """List athlete activities."""
    list_activities_url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(list_activities_url, headers=headers)

    print(f"{response.status_code = }")
    pprint(response.text)


def get_distance(activity_id):
    """Get distance data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=distance&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    print(f"{response.status_code = }")
    # pprint(response.text)
    return response.text["distance"]["data"]


def get_altitude(activity_id):
    """Get altitude data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=altitude&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    print(f"{response.status_code = }")
    # pprint(response.text)
    return response.text["altitude"]["data"]


def get_latlong(activity_id):
    """Get latitude and longitude from activity."""
    latlong_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=latlng&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(latlong_url, headers=headers)

    print(f"{response.status_code = }")
    # pprint(response.text)
    return response.text["latlng"]["data"]


# get_athlete()
# list_activities()
distance = get_distance(6492923259)
altitude = get_altitude(6492923259)
lat_long = get_latlong(6492923259)

print(f"{distance = }\n*5{altitude = }\n*5{lat_long = }")
# Traceback (most recent call last):
#   File "/mnt/c/Users/Brad/Desktop/python/programming/bradbot/src/exts/strava.py", line 73, in <module>
#     distance = get_distance(6492923259)
#   File "/mnt/c/Users/Brad/Desktop/python/programming/bradbot/src/exts/strava.py", line 48, in get_distance
#     return response.text["distance"]["data"]
# TypeError: string indices must be integers
