import os
import asyncio
import random
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot

# Carrega variáveis do .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = "https://lkwn.cc/f1c1c45a"

# Inicializa bot do Telegram e Flask
bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

# Função assíncrona para enviar sinais a cada 10 minutos
async def send_signal():
    while True:
        sinal = random.choice(["⚪ Branco", "🔴 Vermelho", "🔵 Azul"])
        mensagem = (
            f"🎯 Sinal de volta Bo: ✅ Tudo pronto!\n"
            f"Entrada: {sinal}\n"
            f"Link: {URL_CADASTRO}"
        )
        await bot.send_message(chat_id=CHAT_ID, text=mensagem)
        await asyncio.sleep(600)  # Espera 10 minutos

@app.route("/")
def home():
    return "✅ Bot Bac Bo Sinais Online!"

# Inicializa o loop de eventos e roda o servidor
def start():
    loop = asyncio.get_event_loop()
    loop.create_task(send_signal())
    app.run(host="0.0.0.0", port=10000)

if __name
