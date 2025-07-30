import os
import asyncio
import random
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application, CommandHandler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = "https://lkwn.cc/f1c1c45a"

bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

async def send_signal():
    while True:
        sinal = random.choice(["⚪ Branco", "🔴 Vermelho", "🔵 Azul"])
       await bot.send_message(chat_id=CHAT_ID, text=f"🎯 Sinal de volta Bo: ✅ Tudo pronto!")
Entrada: {sinal}
Link: {URL_CADASTRO}")
        await asyncio.sleep(600)

@app.route("/")
def home():
    return "Bot Bac Bo Sinais Online!"

def start():
    loop = asyncio.get_event_loop()
    loop.create_task(send_signal())
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    start()
