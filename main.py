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
URL_CADASTRO = os.getenv("URL_CADASTRO")

# Inicializa bot do Telegram e Flask
bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

# Função assíncrona para enviar sinais a cada 10 minutos
async def send_signal():
    while True:
        sinal = random.choice(["⚪ Branco", "🔴 Vermelho", "🔵 Azul"])
        mensagem = (
            f"🎯 *SINAL BAC BO AUTOMÁTICO*\n\n"
            f"✅ Tudo pronto!\n"
            f"🎰 Entrada: {sinal}\n"
            f"🎁 Bônus de boas-vindas já disponível!\n"
            f"➡️ Cadastre-se: {URL_CADASTRO}"
        )
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="Markdown")
        except Exception as e:
            print(f"Erro ao enviar sinal: {e}")
        await asyncio.sleep(600)  # 10 minutos

@app.route("/")
def home():
    return "✅ Bot Bac Bo Sinais Online!"

# Inicia o loop de eventos e o servidor Flask (sem deprecated)
def start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(send_signal())
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    start()
