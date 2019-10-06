import requests
import json
import os
from datetime import datetime

from dotenv import load_dotenv
import discord
from coordinates import coordinates

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))
API_KEY = os.getenv('API_KEY') # weatherbit api key

client = discord.Client()

def get_forecast(lat, lon, days):
    endpoint = 'http://api.weatherbit.io/v2.0/forecast/daily?'
    q_str = f'lat={lat}&lon={lon}&days={days}&key={API_KEY}'
    response = requests.get(endpoint+q_str)
    return json.loads(response.text)['data']

def ctf(c):
    """returns fahrenheit from celsius"""
    return round((float(c)*(9/5) + 32), 2)

def mmtin(mm):
    """returns inches from mm"""
    return round(float(mm)/25.4, 2)

def get_message(search_str, forecast):
    msg_base = ('**day:** %s\n**temp:** %s F\t**hi:** %s F\t**lo:** %s F'
        '\n**snow:** %s in\t**depth:** %s in\n**desc:** %s\n')
    msg_li = [msg_base % (i+1, ctf(d['temp']), ctf(d['high_temp']),
        ctf(d['low_temp']), mmtin(d['snow']), mmtin(d['snow_depth']),
        d['weather']['description']) for i, d in enumerate(forecast)]
    return '**_**\n**Search:** %s\n%s' % (search_str, '\n'.join(msg_li))

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to: {guild.name}(id: {guild.id}).')

    # weather-bot channel
    channel = client.get_channel(CHANNEL)
    for geo in coordinates:
        lat = geo['lat']
        lon = geo['lat']
        days = 1
        forecast = get_forecast(lat, lon, days)
        mtn = geo['mtn']
        search_str = f'{mtn}, {days}-day'
        msg = get_message(search_str, forecast)
        await channel.send(msg)
        print(f'Sent {search_str} forecast to channel: {channel}.')


if __name__ == '__main__':
    client.run(TOKEN)
