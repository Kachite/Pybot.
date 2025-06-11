import os
import discord
from discord.ext import commands
from fuzzywuzzy import process
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

faq ={"Hi" : "Hi, How can I help you today?",
    "Hello":"Hello, How can I assist you today?",
    "how to open a bank account": "To open a bank account with Tinkoff, you can download our app or visit our website and follow the steps provided.",
    "how to order a card": "To order a card, simply log into the Tinkoff app, go to the 'Cards' section, and follow the instructions to choose and order a card.",
    "how to make a transfer": "To make a transfer, open the Tinkoff app, go to the 'Transfers' section, select the recipient, and enter the amount you want to send.",
    "how to check balance": "You can check your balance directly in the Tinkoff app, or by logging into your account on our website.",
    "how to contact customer support": "To contact customer support, you can use the in-app chat, call us at 8-800-555-77-44, or email support@tinkoff.ru.",
    "how to change my personal information": "To change your personal information, log into the Tinkoff app, go to 'Profile', and select 'Edit Personal Info'.",
    "how to reset my password": "To reset your password, open the Tinkoff app, go to 'Settings', select 'Security', and follow the steps to reset your password.",
    "thank you": "It's a pleasure",
    "okay": "If you have further questions, you can ask"
}

def get_faq_answer(query):
    query_lower = query.lower()
    best_match, score = process.extractOne(query_lower, faq.keys())
    if score > 50:
        return faq[best_match]
    return "Sorry, I couldn't find an answer to your question. Try asking something like 'How to contact customer support' or 'How to reset my password'."

class MyView(discord.ui.View):
    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Hello! I can answer your questions about Tinkoff services. Just ask me anything.", ephemeral=True)

    @discord.ui.button(label="Subscribe", style=discord.ButtonStyle.primary)
    async def subscribe_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Implement your subscribe logic here (e.g., add user to database)
        await interaction.response.send_message(f"{interaction.user.mention}, you have subscribed to automated updates!", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command(name='welcome')
async def welcome(ctx):
    # Sends a message with Start and Subscribe buttons
    await ctx.send("Welcome! Choose an option below:", view=MyView())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if not message.content.startswith('!'):
        answer = get_faq_answer(message.content)
        await message.channel.send(answer)

bot.run(TOKEN)