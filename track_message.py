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
    channel = client.get_channel(int(os.getenv('UPDATE_CHANNEL_ID')))  #send a message when bot is active for testing
    await channel.send(f'{client.user} is online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    CHANNEL_ID = int(os.getenv('UPDATE_CHANNEL_ID'))
    channel = client.get_channel(CHANNEL_ID)

    if message.content.startswith("prev"):
        prev = load_data()
        user_id = str(message.author.id)
        await channel.send(prev[user_id]["last message"]["content"])
        

    if message.channel.id == CHANNEL_ID: #only save messages for specified channel
        if "daily progress" in message.content: #simple logic
            print("Found!")
            save_data(message, progress=True)
        else:
            print("Not Found!")
            save_data(message)


def load_data():
    global data
    try:
        with open('./output.json', 'r') as file:      
            data = json.load(file)
            return data
    except FileNotFoundError:
        data = {}
        return
    
def save_data(message, progress=False): 
    global data     
    ct = datetime.now()
    
    data[str(message.author.id)]["last message"] = {"time": ct.timestamp(), "content" : message.content}
        # "user name" : str(message.author.name)
        
    if progress == True:
        data[str(message.author.id)]["progress"] = {
            "procrastinator" : False,
            "time" : ct.timestamp(),
            "content" : message.content
        }
        

    with open('output.json', 'w') as file:
        json.dump(data, file, indent=4)


client.run(os.getenv("BOT_TOKEN"))
