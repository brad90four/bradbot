# strava vis
# http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,activity:read_all
# curl -X POST https://www.strava.com/oauth/token -F client_id=YOURCLIENTID -F client_secret=YOURCLIENTSECRET -F code=AUTHORIZATIONCODE -F grant_type=authorization_code # noqa: E501
import json
import os
from pathlib import Path
from pprint import pprint
from typing import Optional

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


def get_athlete() -> None:
    """Get athlete data"""
    athlete_url = "https://www.strava.com/api/v3/athlete"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(athlete_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    pprint(response.json())


def list_activities() -> dict:
    """List athlete activities."""
    list_activities_url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(list_activities_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    activities = response.json()
    for i in range(len(activities)):
        activity_id = activities[i]["id"]
        activity_description = activities[i]["name"]
        print(f"{activity_description : <35}: {activity_id}")


def get_activities() -> dict:
    """List athlete activities."""
    list_activities_url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(list_activities_url, headers=headers)

    logger.debug(f"{response.status_code = }")

    return response.json()


def get_distance(activity_id: str) -> dict[str, list[float]]:
    """Get distance data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=distance&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    logger.debug(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["distance"]["data"]


def get_altitude(activity_id: str) -> dict[str, list[float]]:
    """Get altitude data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=altitude&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(activity_stream, headers=headers)

    logger.debug(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["altitude"]["data"]


def get_latlong(activity_id: str) -> dict[str, list[list[float, float]]]:
    """Get latitude and longitude from activity."""
    latlong_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=latlng&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {STRAVA_TOKEN}"}
    response = requests.get(latlong_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    # pprint(response.json())
    return response.json()["latlng"]["data"]


def write_data(path: str, dist_data: dict, alt_data: dict, latlng_data: dict) -> None:
    """Write activity data to a json file."""
    with open(f"{path.parents[0]}/strava_data.json", "w") as f:
        json.dump(dist_data, f)
        f.write("\n")
        json.dump(alt_data, f)
        f.write("\n")
        json.dump(latlng_data, f)
        f.write("\n")


def read_data() -> None:
    """
    Read activity data from a json file.

    Currently not in use for running locally.
    """
    pass


def latlng_to_feet(latlng: float) -> float:
    """Convert latitude or longitude to feet."""
    return latlng * 364488


def feet_to_latlng(feet: float) -> float:
    """Convert feet to decimal latitude / longitude."""
    return feet / 364488


def plotter(data: tuple[list[float], list[float], list[float]]) -> None:
    """Function for plotting data in 3D"""
    X, Y, Z = data
    x_lim = min(X), max(X)
    y_lim = min(Y), max(Y)
    z_lim = min(Z), max(Z)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(X, Y, Z)
    ax.set_zlim3d(z_lim)
    ax.set_box_aspect((1, 1, feet_to_latlng(1) * 100000))
    ax.plot(X, Y, Z)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude")
    ax.set_xticks(list(x_lim))
    ax.set_yticks(list(y_lim))
    ax.ticklabel_format(useOffset=False)
    plt.show()


def animator(data: tuple[list[float], list[float], list[float]], id_number: str) -> None:
    """Animate a 3D plot based on the input data and save with the id_number."""
    logger.debug(f"Animator starting for : {id_number}")
    X, Y, Z = data
    x_lim = min(X), max(X)
    y_lim = min(Y), max(Y)
    z_lim = min(Z), max(Z)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_zlim3d(z_lim)
    ax.set_box_aspect((1, 1, feet_to_latlng(1) * 100000))
    ax.plot(X, Y, Z)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude")
    ax.set_xticks(list(x_lim))
    ax.set_yticks(list(y_lim))
    ax.ticklabel_format(useOffset=False)

    def init():
        ax.plot(X, Y, Z)
        return (fig,)

    def animate(i):
        ax.view_init(elev=30.0, azim=i)
        return (fig,)

    anim = FuncAnimation(fig, animate, init_func=init, frames=360, interval=20, blit=True)
    save_name = f"strava_vis_{id_number}.gif"
    anim.save(save_name, writer=PillowWriter(fps=30))
    plt.close()
    logger.debug("Animator finished")


def main() -> None:
    """Command line interaction for listing activity, then plotting in 3D."""
    logger.debug("`main` starting")
    list_activities()
    activity = input("Enter target activity id: ")
    altitude = {"altitude": get_altitude(activity)}
    lat_long = {"lat_long": get_latlong(activity)}
    # distance = {"distance": get_distance(activity)}
    # write_data(path, distance, altitude, lat_long)
    X = [x[1] for x in lat_long["lat_long"]]
    Y = [y[0] for y in lat_long["lat_long"]]
    Z = [z for z in altitude["altitude"]]
    animator((X, Y, Z), activity)
    plotter((X, Y, Z))

    logger.debug("`main` finished")


def testing(debug_option: Optional[bool] = False) -> None:
    """Test `main` with a static activity ID."""
    logger.debug("Running test mode")
    altitude = {"altitude": get_altitude(6492923259)}
    lat_long = {"lat_long": get_latlong(6492923259)}
    # distance = {"distance": get_distance(6492923259)}
    # write_data(path, distance, altitude, lat_long)
    X = [x[1] for x in lat_long["lat_long"]]
    Y = [y[0] for y in lat_long["lat_long"]]
    Z = [z for z in altitude["altitude"]]

    if debug_option:
        x_lim = min(X), max(X)
        y_lim = min(Y), max(Y)
        z_lim = min(Z), max(Z)
        print(f"{X[:11] = }")
        print(f"{Y[:11] = }")
        print(f"{Z[:11] = }")
        print(f"{x_lim = }: {y_lim = }")
        print(f"x_range= {max(X) - min(X)}, y_range= {max(Y) - min(Y)}")
        print(f"{z_lim = }")
        print(f"z_range= {max(Z) - min(Z)}")
        print(f"{len(X) = }\n{len(Y) = }\n{len(Z) = }")

    animator((X, Y, Z), "test")
    plotter((X, Y, Z))

    logger.debug("`testing` finished")


def all_rides() -> None:
    """Plot all of the rides."""
    logger.debug("`all_rides` starting")
    all_activities = get_activities()
    for i in range(len(all_activities)):
        name = all_activities[i]["name"].replace(" ", "_")
        logger.debug(f"Making vis for {name}")
        activity = all_activities[i]["id"]
        altitude = {"altitude": get_altitude(activity)}
        lat_long = {"lat_long": get_latlong(activity)}
        X = [x[1] for x in lat_long["lat_long"]]
        Y = [y[0] for y in lat_long["lat_long"]]
        Z = [z for z in altitude["altitude"]]
        animator((X, Y, Z), name)

    logger.debug("`all_rides` finished")


if __name__ == "__main__":
    main()
    # testing(debug_option=True)
    # all_rides()
