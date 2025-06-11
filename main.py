from bots.telegram_bot import TelegramBot
from bots.whatsapp_bot import WhatsAppBot
from bots.discord_bot import DiscordBot
import threading

def main():
    # Initialize bots
    telegram_bot = TelegramBot("7556909227:AAGBffoAVMnnwRm34VLAN68IWqhhpFO1TTQ")
    whatsapp_bot = WhatsAppBot("+79003018081") 
    discord_bot = DiscordBot("YOUR_DISCORD_BOT_TOKEN")

    # Start bots in separate threads
    threading.Thread(target=telegram_bot.start, daemon=True).start()
    threading.Thread(target=whatsapp_bot.send_updates, daemon=True).start()
    threading.Thread(target=discord_bot.start, daemon=True).start()

if __name__ == "__main__":
    main()