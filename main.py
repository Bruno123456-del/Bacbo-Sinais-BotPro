from telegram import Bot
import os

# Pegando variáveis do .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
FREE_CHAT_ID = int(os.getenv("FREE_CHAT_ID"))
VIP_CHAT_ID = int(os.getenv("VIP_CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

# Teste canal FREE
bot.send_message(chat_id=FREE_CHAT_ID, text="Teste canal FREE ✅")

# Teste canal VIP
bot.send_message(chat_id=VIP_CHAT_ID, text="Teste canal VIP ✅")
