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


def get_forecast(lat: float, lon: float, days: int) -> object:
    lat = str(lat)
    lat = str(lon)
    lat = str(days)

    response = requests.get(
        "http://api.weatherbit.io/v2.0/forecast/daily?"
        f"lat={lat}&lon={lon}&days={days}&key={API_KEY}"
    )
    forecast = json.loads(response.text)["data"]

    return forecast


def celsius_to_fahrenheit(c: float) -> float:
    """returns fahrenheit from celsius"""
    return round((float(c) * (9 / 5) + 32), 2)


def millimeters_to_inches(mm: float) -> float:
    """returns inches from mm"""
    return round(float(mm) / 25.4, 2)


def day_to_next_day(now: str, d: int) -> str:
    return (now + timedelta(days=d)).strftime("%m/%d/%y")


def create_msg(search: str, forecast: list) -> str:
    msg_li = [
        "\n".join(
            [
                f":calendar: **{day_to_next_day(datetime.now(), i)}**    "
                f":thermometer: {celsius_to_fahrenheit(d['temp'])} F, "
                f":snowflake: {millimeters_to_inches(d['snow'])} "
                f"in, :mount_fuji: {millimeters_to_inches(d['snow_depth'])} in, "
                f":notepad_spiral: {d['weather']['description']}",
            ]
        )
        for i, d in enumerate(forecast)
    ]

    return "\n>> **Search:** %s\n\n%s" % (search, "\n".join(msg_li))


def search_lookup_keys(search: str) -> str:
    """returns best search result"""
    for k in LOOKUP.keys():
        if search in k:

            return k

    return search


def parse_days_from_args_remove(args: List[str]) -> (str, List[str]):

    days = 3  # default days = 3
    new_args = args

    if len(args):
        return int(days), new_args

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


def parse_msg_args(msg: object) -> List[str]:
    args = (
        msg.content.replace("!forecast", "")
        .replace("!f", "")
        .replace(",", "")
        .strip()
        .split(" ")  # consider each space end of arg position
    )

    return args


def parse_msg_inputs(msg: object) -> dict:
    args = parse_msg_args(msg)
    days, args = parse_days_from_args_remove(args)
    search = " ".join(args)
    inputs = {"search": search, "days": days, "args": args}

    return inputs


def handle_exception(msg: object) -> str:
    e = (
        "**Error. Please try again.**"
        "\n`user`: %s"
        "\n`failed command`: '%s'"
        "\n`allowed commands`: %s"
        "\n`days options`: %s "
        "\n`example command`: 'jfbb, pa 5'"
    )

    msg = e % (
        msg.author,
        msg.content,
        [_.lower() + " [days]" for _ in list(LOOKUP)],
        list(range(1, 17)),
    )

    traceback.print_exc()

    return msg


@client.event
async def on_message(message):
    if message.content.startswith("!forecast ") or message.content.startswith("!f "):

        try:
            inputs = parse_msg_inputs(message)
        
        except:
            fmsg = handle_exception(message)

        # weather-bot channel
        channel = client.get_channel(CHANNEL)

        try:
            lat = LOOKUP[search_lookup_keys(inputs["search"])]["lat"]
            lon = LOOKUP[search_lookup_keys(inputs["search"])]["lon"]
            forecast = get_forecast(lat, lon, inputs["days"])
            fmsg = create_msg(inputs["search"], forecast)

        except:
            fmsg = handle_exception(message)

        await channel.send(fmsg)

        print(f"Responded to '{message.content}' in channel: {channel}.")


if __name__ == "__main__":
    client.run(TOKEN)
