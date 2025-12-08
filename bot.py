import discord
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from discord.ext import tasks, commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

data = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    load_data()
    if not hourly_check.is_running():
        hourly_check.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == int(os.getenv('UPDATE_CHANNEL_ID')):
        save_data(message)

@tasks.loop(hours=1)
async def hourly_check():
    channel = client.get_channel(int(os.getenv('UPDATE_CHANNEL_ID')))
    now = datetime.now()
    if channel:
        load_data()
        for user_data in data:
            then = datetime.fromtimestamp(data[user_data])
            difference = now - then
            if difference.days == 3: #inactive for 3 days
                # TODO: add punishment role to the user
                continue
                

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
