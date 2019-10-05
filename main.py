import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))

client = discord.Client()

def get_message():
    return 'Testing bot messages.'

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print('{client.user} is connected to: {guild.name}(id: {guild.id}).')

    # weather-bot channel
    channel = client.get_channel(CHANNEL)

    msg = get_message()
    await channel.send(msg)
    print('Sent: %s using %s.' % (msg, CHANNEL))

client.run(TOKEN)
