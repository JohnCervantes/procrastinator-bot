import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True # we can track events like on_message()
intents.guild_reactions= True # track reaction events
intents.guilds = True # track guild events like when someone jons or is removed/leaves
intents.members = True #Assign roles to users

#works similar to discord.Client
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = int(os.getenv('UPDATE_CHANNEL_ID'))

@bot.event
async def on_ready():
    #Send a messasge when bot is ready
    print(f"Logged in as {bot.user}")
    try:
        guild = discord.Object(id=int(os.getenv("SERVER_ID")))
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to {guild.id}")
    except Exception as e:
        print(f"Exception has occured : {e}")
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Bot is online!")
    
@bot.event
async def on_message(message):
    # track whenever any message is sent in server
    msg_sampled = message.content.split() # to check if given string is in the message
    #check if it has words "daily progress"
    
    if message.author == bot.user: #checking if message sender is bot itself
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    
    if message.content.startswith("$"):
        await message.reply("Hello") #reply with ping
        return
    if message.content.startswith("!"):
        await message.reply("Hello", mention_author = False)
        return
    
    if message.content.startswith("embed"):
        embeding = discord.Embed(title="Bot Embeddings", description="I don't know honestly", color= discord.Color.brand_green())
        embeding.add_field(name="Last Procrastinator",value="This idiot is a procrastinator")
        embeding.set_footer(text="goodbye!")
        embeding.set_author(name=message.author.name)
                            # , icon_url="I'll set it to somthing")
        await channel.send(embed=embeding)
    
    if "hello" in msg_sampled:
        await message.add_reaction("👋")
        # await message.send("Hello") --> you need channel id to send message
        # await message.channel.send("Hello")
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"Hello {message.author.mention}")
    
GUILD_ID = discord.Object(id=int(os.getenv("SERVER_ID")))
    
# Slash commands
@bot.tree.command(name="hello", description="Says Hello!", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello there {interaction.user}")
    
@bot.tree.command(name="emb", description="Embeds a message!", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction, link: str): #take input from user when using slash commands
    embeding = discord.Embed(title=link, description="", color= 0)
    # embeding.add_field(name="Last Procrastinator",value="This idiot is a procrastinator")
    embeding.set_footer(text="goodbye!")
    embeding.set_author(name=interaction.user.name)
    await interaction.response.send_message(embed=embeding)

# BUTTONS   
class View(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.red, emoji="🔥")#red = danger
    async def test_button(self, button, interaction):
        await button.response.send_message("You clicked on the button!")
    
    @discord.ui.button(label="Okay!", style=discord.ButtonStyle.green, emoji="✅") #green = success
    async def test_button_1(self, button, interaction):
        await button.response.send_message("Everything is alright")
        
    @discord.ui.button(label="Touch me!", style=discord.ButtonStyle.primary, emoji="🌸") #primary = blurple, secondary = gray/invisible
    async def test_button_2(self, button, interaction):
        await button.response.send_message("It wasn't your fault, it does not matter what they say \n It was never your fault")
    
@bot.tree.command(name="button", description="Clickable Buttons", guild=GUILD_ID)
async def my_button(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())
    
# Dropdown

class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Option 1",
                description="Does option 1",
                emoji="✅"
            ),
            discord.SelectOption(
                label="Option 2",
                description="Does option 2",
                emoji="🔥"
            )
        ]
        super().__init__(placeholder="Choose an option", min_values=1, max_values=2, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        await interaction.response.send_message(f"You picked {self.values[0]}")
        
class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())
        
@bot.tree.command(name="menu", description="Clickable Buttons", guild=GUILD_ID)
async def my_button(interaction: discord.Interaction):
    await interaction.response.send_message(view=MenuView())
    

bot.run(os.getenv("BOT_TOKEN"))
