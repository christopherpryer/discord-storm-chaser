import requests
import json
import os
from datetime import datetime

from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))
API_KEY = os.getenv('API_KEY') # weatherbit api key

client = discord.Client()

def get_forecast(city, state, days):
    endpoint = 'http://api.weatherbit.io/v2.0/forecast/daily?'
    q_str = f'city={city},{state}&days={days}&key={API_KEY}'
    response = requests.get(endpoint+q_str)
    return json.loads(response.text)['data']

def get_message(search_str, forecast):
    now = datetime.now()
    msg_base = 'day: %s\nhigh: %s\nlow: %s\nwind speed: %s\ndesc: %s\n'
    msg_li = [msg_base % (i+1, d['high_temp'], d['low_temp'], d['wind_spd'],
        d['weather']['description']) for i, d in enumerate(forecast)]
    return '[%s] Search: %s\n%s' % (now, search_str, '\n'.join(msg_li))

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to: {guild.name}(id: {guild.id}).')

    # weather-bot channel
    channel = client.get_channel(CHANNEL)
    city = 'Stowe'
    state = 'VT'
    days = 10
    forecast = get_forecast(city, state, days)
    search_str = f'{city}, {state}, {days}-day'
    msg = get_message(search_str, forecast)
    await channel.send(msg)
    print(f'Sent to channel: {channel}.')


if __name__ == '__main__':
    client.run(TOKEN)
