import telebot
from fuzzywuzzy import process
import schedule
import time
import threading

import os
from dotenv import load_dotenv
import telebot
from fuzzywuzzy import process

# Load environment variables
load_dotenv()

# Get the token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Store user chat IDs for notifications
subscribed_users = set()

# Dictionary of Tinkoff FAQs and answers
faq = {
    "Hi" : "Hi, How can I help you today?",
    "Hello":"Hello, How can I assist you today?",
    "how to open a bank account": "To open a bank account with Tinkoff, you can download our app or visit our website and follow the steps provided.",
    "how to order a card": "To order a card, simply log into the Tinkoff app, go to the 'Cards' section, and follow the instructions to choose and order a card.",
    "how to make a transfer": "To make a transfer, open the Tinkoff app, go to the 'Transfers' section, select the recipient, and enter the amount you want to send.",
    "how to check balance": "You can check your balance directly in the Tinkoff app, or by logging into your account on our website.",
    "how to contact customer support": "To contact customer support, you can use the in-app chat, call us at 8-800-555-77-44, or email support@tinkoff.ru.",
    "how to change my personal information": "To change your personal information, log into the Tinkoff app, go to 'Profile', and select 'Edit Personal Info'.",
    "how to reset my password": "To reset your password, open the Tinkoff app, go to 'Settings', select 'Security', and follow the steps to reset your password.",
    "Thank you": "It's a pleasure",
    "Okay": "If you have further questions, you can ask"
}

# Create keyboard markup with buttons
def main_menu_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Start"),
        telebot.types.KeyboardButton("Subscribe"),
        telebot.types.KeyboardButton("Unsubscribe")
    )
    return markup

# Command to start the bot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I can answer your questions about Tinkoff services. Just ask me anything. Use the buttons below to subscribe or unsubscribe.", reply_markup=main_menu_keyboard())
    subscribed_users.add(message.chat.id)

# Handle button clicks and text input
@bot.message_handler(func=lambda message: True)
def handle_buttons_and_questions(message):
    text = message.text

    if text == "Start":
        send_welcome(message)
    elif text == "Subscribe":
        subscribe(message)
    elif text == "Unsubscribe":
        unsubscribe(message)
    else:
        # Treat as question
        user_question = message.text
        answer = get_faq_answer(user_question)
        bot.reply_to(message, answer, reply_markup=main_menu_keyboard())

# Command to subscribe to notifications
def subscribe(message):
    chat_id = message.chat.id
    if chat_id not in subscribed_users:
        subscribed_users.add(chat_id)
    bot.reply_to(message, "You have subscribed to automated updates!", reply_markup=main_menu_keyboard())

# Command to unsubscribe
def unsubscribe(message):
    chat_id = message.chat.id
    if chat_id in subscribed_users:
        subscribed_users.discard(chat_id)
    bot.reply_to(message, "You have unsubscribed from automated updates!", reply_markup=main_menu_keyboard())

# Function to match user queries with FAQs using fuzzy matching
def get_faq_answer(query):
    query_lower = query.lower()
    best_match, score = process.extractOne(query_lower, faq.keys())
    if score > 50:
        return faq[best_match]
    return "Sorry, I couldn't find an answer to your question. Maybe you can try asking something like: 'How to contact customer support' or 'How to reset my password'."

# Run the bot
bot.polling()