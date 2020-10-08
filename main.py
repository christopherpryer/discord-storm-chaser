import requests
import json
import os
from datetime import datetime, timedelta
import traceback
from dotenv import load_dotenv
import discord
from coordinates import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CHANNEL = int(os.getenv("DISCORD_CHANNEL"))
API_KEY = os.getenv("API_KEY")  # weatherbit api key TODO: rename, dingus

client = discord.Client()


def get_forecast(lat, lon, days):
    endpoint = "http://api.weatherbit.io/v2.0/forecast/daily?"
    q_str = f"lat={lat}&lon={lon}&days={days}&key={API_KEY}"
    response = requests.get(endpoint + q_str)
    return json.loads(response.text)["data"]


def ctf(c):
    """returns fahrenheit from celsius"""
    return round((float(c) * (9 / 5) + 32), 2)


def mmtin(mm):
    """returns inches from mm"""
    return round(float(mm) / 25.4, 2)


def next_day(now, d):
    return (now + timedelta(days=d)).strftime("%m/%d/%y")


def get_message(search_str, forecast):
    now = datetime.now()
    msg_base = (
        "**Date:** %s\t**Temp:** %s F"
        "\n**Snow:** %s in\t**Depth:** %s in\n**Desc:** %s\n"
    )
    msg_li = [
        msg_base
        % (
            next_day(now, i),
            ctf(d["temp"]),
            mmtin(d["snow"]),
            mmtin(d["snow_depth"]),
            d["weather"]["description"],
        )
        for i, d in enumerate(forecast)
    ]
    return "**_**\n**Search:** %s\n%s" % (search_str, "\n".join(msg_li))


@client.event
async def on_ready():
    # guild = discord.utils.get(client.guilds, name=GUILD)
    print(f"{client.user} is running")


@client.event
async def on_message(message):
    if message.content.startswith("!weather "):
        cmd_str = message.content[9:]
        args = [" ".join(cmd_str.split(" ")[:-1]), cmd_str.split(" ")[-1]]
        key = args[0].upper()
        msg = ""

        # weather-bot channel
        channel = client.get_channel(CHANNEL)
        try:
            lat = lookup[key]["lat"]
            lon = lookup[key]["lon"]
            days = int(args[1])
            forecast = get_forecast(lat, lon, days)
            search_str = f"{args[0]}, {args[1]}-day"
            msg = get_message(search_str, forecast)
        except:
            e = (
                "**Error. Please try again.**"
                "\n`user`: %s"
                "\n`failed command`: '%s'"
                "\n`allowed commands`: %s"
                "\n`days options`: %s "
                "\n`example command`: 'jfbb, pa 5'"
            )
            msg = e % (
                message.author,
                cmd_str,
                [l.lower() + " [days]" for l in list(lookup)],
                list(range(1, 17)),
            )
            traceback.print_exc()

        await channel.send(msg)
        print(f"Responded to '{cmd_str}' in channel: {channel}.")


if __name__ == "__main__":
    client.run(TOKEN)
