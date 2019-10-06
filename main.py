import os

from dotenv import load_dotenv
import discord

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
    print(f'{client.user} is connected to: {guild.name}(id: {guild.id}).')

    # weather-bot channel
    channel = client.get_channel(CHANNEL)

    msg = get_message()
    await channel.send(msg)
    print(f'Sent: \'{msg}\' using channel id: {CHANNEL}.')


if __name__ == '__main__':
    client.run(TOKEN)
