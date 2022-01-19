# strava vis
# http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,activity:read_all
# curl -X POST https://www.strava.com/oauth/token -F client_id=YOURCLIENTID -F client_secret=YOURCLIENTSECRET -F code=AUTHORIZATIONCODE -F grant_type=authorization_code # noqa: E501
import json
import os
from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
from loguru import logger
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# import nextcord

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

    logger.debug(f"{response.status_code = }")
    pprint(response.json())


def list_activities():
    """List athlete activities."""
    list_activities_url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(list_activities_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    activities = response.json()
    for i in range(len(activities)):
        activity_id = response.json()[i]["id"]
        activity_description = response.json()[i]["name"]
        print(f"{activity_description : <35}: {activity_id}")


def get_distance(activity_id):
    """Get distance data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=distance&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    logger.debug(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["distance"]["data"]


def get_altitude(activity_id):
    """Get altitude data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=altitude&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    logger.debug(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["altitude"]["data"]


def get_latlong(activity_id):
    """Get latitude and longitude from activity."""
    latlong_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=latlng&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(latlong_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["latlng"]["data"]


def write_data(path, dist_data, alt_data, latlng_data):
    """Write activity data to a json file."""
    with open(f"{path.parents[0]}/strava_data.json", "w") as f:
        json.dump(dist_data, f)
        f.write("\n")
        json.dump(alt_data, f)
        f.write("\n")
        json.dump(latlng_data, f)
        f.write("\n")


def read_data():
    """
    Read activity data from a json file.

    Currently not in use for running locally.
    """
    pass


def main():
    """Command line interaction for listing activity, then plotting in 3D."""
    list_activities()
    activity = input("Enter target activity id: ")
    altitude = {"altitude": get_altitude(activity)}
    lat_long = {"lat_long": get_latlong(activity)}
    # distance = {"distance": []}
    # write_data(path, distance, altitude, lat_long)
    X = [x[1] for x in lat_long["lat_long"]]
    Y = [y[0] for y in lat_long["lat_long"]]
    Z = [z for z in altitude["altitude"]]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    def init():
        ax.plot(X, Y, Z)
        return (fig,)

    def animate(i):
        ax.view_init(elev=30.0, azim=i)
        return (fig,)

    anim = FuncAnimation(fig, animate, init_func=init, frames=360, interval=20, blit=True)
    save_name = f"strava_vis_{activity}.gif"
    anim.save(save_name, writer=PillowWriter(fps=30))
    # ax.plot(X, Y, Z)
    # plt.show()
    logger.debug("Finished writing")


def testing():
    """Test `main` with a static activity ID."""
    altitude = {"altitude": get_altitude(6492923259)}
    lat_long = {"lat_long": get_latlong(6492923259)}
    # distance = {"distance": get_distance(6492923259)}
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
    # ax.plot(X, Y, Z)
    # plt.show()

    def init():
        ax.plot(X, Y, Z)
        return (fig,)

    def animate(i):
        ax.view_init(elev=30.0, azim=i)
        return (fig,)

    anim = FuncAnimation(fig, animate, init_func=init, frames=360, interval=20, blit=True)
    save_name = "strava_vis.gif"
    anim.save(save_name, writer=PillowWriter(fps=30))


if __name__ == "__main__":
    main()
    # testing()
