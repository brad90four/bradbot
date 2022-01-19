# strava vis
import json
import os
from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

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
    pprint(response.json())


def list_activities():
    """List athlete activities."""
    list_activities_url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(list_activities_url, headers=headers)

    print(f"{response.status_code = }")
    pprint(response.json())


def get_distance(activity_id):
    """Get distance data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=distance&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    print(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["distance"]["data"]


def get_altitude(activity_id):
    """Get altitude data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=altitude&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    print(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["altitude"]["data"]


def get_latlong(activity_id):
    """Get latitude and longitude from activity."""
    latlong_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=latlng&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(latlong_url, headers=headers)

    print(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["latlng"]["data"]


# Testing activity ID
# distance = {"distance": json.dumps(get_distance(6492923259))}
# altitude = {"altitude": json.dumps(get_altitude(6492923259))}
# lat_long = {"lat_long": json.dumps(get_latlong(6492923259))}


def write_data(path, dist_data, alt_data, latlng_data):
    with open(f"{path.parents[0]}/strava_data.json", "w") as f:
        json.dump(dist_data, f)
        f.write("\n")
        json.dump(alt_data, f)
        f.write("\n")
        json.dump(latlng_data, f)
        f.write("\n")


def read_data():
    pass


def main():
    # get_athlete()
    list_activities()
    activity = input("Enter target activity id: ")
    distance = {"distance": json.dumps(get_distance(activity))}
    altitude = {"altitude": json.dumps(get_altitude(activity))}
    lat_long = {"lat_long": json.dumps(get_latlong(activity))}
    write_data(path, distance, altitude, lat_long)


def testing():
    # distance = {"distance": get_distance(6492923259)}
    altitude = {"altitude": get_altitude(6492923259)}
    lat_long = {"lat_long": get_latlong(6492923259)}
    # write_data(path, distance, altitude, lat_long)
    X = [x[1] for x in lat_long["lat_long"]]
    Y = [y[0] for y in lat_long["lat_long"]]
    Z = [z for z in altitude["altitude"]]
    print(X[:11])
    print(Y[:11])
    print(Z[:11])
    print(f"{len(X) = }\n{len(Y) = }\n{len(Z) = }")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(X, Y, Z)
    plt.show()


if __name__ == "__main__":
    # main()
    testing()
