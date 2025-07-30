import os
import asyncio
import random
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot

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
        # Monta a mensagem corretamente, com f-string fechada
        mensagem = (
            f"🎯 Sinal de volta Bo: ✅ Tudo pronto!\n"
            f"Entrada: {sinal}\n"
            f"Link: {URL_CADASTRO}"
        )
        await bot.send_message(chat_id=CHAT_ID, text=mensagem)
        await asyncio.sleep(600)  # espera 10 minutos

@app.route("/")
def home():
    return "Bot Bac Bo Sinais Online!"

def start():
    loop = asyncio.get_event_loop()
    # Cria a task de enviar sinais de forma assíncrona
    loop.create_task(send_signal())
    # Roda o Flask
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    start()
