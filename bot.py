# bot.py
import os

import discord
from dotenv import load_dotenv

import urllib.parse
import requests
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('DEEP_DREAM_API_KEY')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f'message: {message.content}')

    m = re.search('^https?://[^ ]+', message.content)

    if m == None:
        return

    print(f'match: {m}')

    input_url = m.group(0)

    print(f'input url: {input_url}')

    #curl \
    #     -F 'image=YOUR_IMAGE_URL' \
    #     -H 'api-key:quickstart-QUdJIGlzIGNvbWluZy4uLi4K' \
    #     https://api.deepai.org/api/deepdream

    url = 'https://api.deepai.org/api/deepdream'
    r = requests.post(url, data = { 'image': input_url }, headers = { 'api-key': API_KEY })

    print(f'status: {r.status_code}')

    if r.status_code != 200:
        return

    print(r.content)

    result = r.json()

    await message.channel.send(result['output_url'])

client.run(TOKEN)
