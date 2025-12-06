# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

data = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    load_data()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == int(os.getenv('UPDATE_CHANNEL_ID')):
        save_data(message)


def load_data():
    global data
    try:
        with open('./output.json', 'r') as file:      
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
def save_data(message): 
    global data     
    ct = datetime.now()

    data[str(message.author.id)] = ct.timestamp() 

    with open('output.json', 'w') as file:
        json.dump(data, file, indent=4)


client.run(os.getenv("BOT_TOKEN"))
