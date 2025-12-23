import discord
from dotenv import load_dotenv
import os
import json
#Lets use a standard timezone(UTC)
from datetime import datetime, timezone
from discord.ext import tasks, commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True #required to access members

client = discord.Client(intents=intents)

# data = {} # I don't get this

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    load_data()
    channel = client.get_channel(int(os.getenv('UPDATE_CHANNEL_ID')))  #send a message when bot is active for testing
    await channel.send(f'{client.user} is online!')
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
    guild = client.get_guild(int(os.getenv('SERVER_ID'))) # You need server/guild object to access the role
    role = guild.get_role(int(os.getenv('ROLE_ID')))
    channel = client.get_channel(int(os.getenv('UPDATE_CHANNEL_ID')))
    now = datetime.now(timezone.utc)
    log = load_data()
    for member in guild.members:
        if member.bot:
            continue
        then = datetime.fromtimestamp(
            log[str(member.id)]["last_message"]["time"],
            tz=timezone.utc
        )
        difference = now-then
        if difference.days >= 3: # Inactive for 3 days or more
            if role not in member.roles: # Check if already has the role
                try:
                    await member.add_roles(role, reason="Not posted progress for 3 days")
                    await channel.send(f"{member.mention} you have been inactive") #send message pinging that member
                except discord.Forbidden:
                    continue
        else: # Remove the role if member is active
            if role in member.roles:
                try:
                    await member.remove_roles(role, reason="Started posting progress again")
                    await channel.send(f"{member.mention} you have become active again")
                except discord.Forbidden:
                    continue
                
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
    user_id = str(message.author.id)
    if user_id not in data:
        data[user_id] = {"user_name" : str(message.author.name)}
    
    data[user_id]["last_message"] = {"time": ct.timestamp(), "content" : message.content}
        
    if progress == True:
        data[user_id]["progress"] = {
            "procrastinator" : False,
            "time" : ct.timestamp(),
            "content" : message.content
        }
        
    with open('output.json', 'w') as file:
        json.dump(data, file, indent=4)


client.run(os.getenv("BOT_TOKEN"))
