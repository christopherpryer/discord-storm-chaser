import requests
import json
import os
from datetime import datetime, timedelta
import traceback
from dotenv import load_dotenv
import discord
from coordinates import *
from typing import Dict, List

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

    msg_li = [
        "\n".join(
            [
                f":calendar: **{next_day(now, i)}**    "
                f":thermometer: {ctf(d['temp'])} F, :snowflake: {mmtin(d['snow'])}"
                f" in, :mount_fuji: {mmtin(d['snow_depth'])} in, "
                f":notepad_spiral: {d['weather']['description']}",
            ]
        )
        for i, d in enumerate(forecast)
    ]

    return "\n>> **Search:** %s\n\n%s" % (search_str, "\n".join(msg_li))


def search_lookup_keys(search_str: str) -> str:
    """returns best search result"""
    for k in LOOKUP.keys():
        if search_str in k:

            return k

    return search_str


def parse_days_from_args_remove(args: List[str]) -> (str, List[str]):

    days = 3  # default days = 3
    new_args = args

    if args[-1] in ["d", "day", "days"]:
        days, new_args = args[-2], args[:-2]

    elif args[-1].lower().endswith("d"):
        days, new_args = args[-1][:-1], args[:-1]

    elif args[-1].lower().endswith("-day"):
        days, new_args = args[-1][:-4], args[:-1]

    elif args[-1].lower().endswith("day"):
        days, new_args = args[-1][:-3], args[:-1]

    elif args[-1].isdigit():
        days, new_args = args[-1], args[:-1]

    return int(days), new_args


@client.event
async def on_ready():
    # guild = discord.utils.get(client.guilds, name=GUILD)
    print(f"{client.user} is running")


@client.event
async def on_message(message):
    if message.content.startswith("!weather ") or message.content.startswith("!w "):
        cmd_str = (
            message.content.replace("!weather", "")
            .replace("!w", "")
            .replace(",", "")
            .strip()
        )
        args = cmd_str.split(" ")  # consider each space end of arg position
        days, args = parse_days_from_args_remove(args)

        key = " ".join(args)
        msg = ""

        # weather-bot channel
        channel = client.get_channel(CHANNEL)
        try:
            lat = LOOKUP[search_lookup_keys(key)]["lat"]
            lon = LOOKUP[search_lookup_keys(key)]["lon"]
            forecast = get_forecast(lat, lon, days)
            msg = get_message(key, forecast)
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
                [l.lower() + " [days]" for l in list(LOOKUP)],
                list(range(1, 17)),
            )
            traceback.print_exc()

        await channel.send(msg)
        print(f"Responded to '{cmd_str}' in channel: {channel}.")


if __name__ == "__main__":
    client.run(TOKEN)
