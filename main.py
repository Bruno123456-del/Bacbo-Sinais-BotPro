import os
import asyncio
import random
import threading
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

# --- Carregando variáveis do ambiente ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO")

if not TOKEN or not CHAT_ID or not URL_CADASTRO:
    raise ValueError("❌ Variáveis BOT_TOKEN, CHAT_ID ou URL_CADASTRO não foram definidas.")

# --- Inicialização ---
bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

# --- Função principal de envio de sinais ---
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
            print(f"[{datetime.now().strftime('%d/%m %H:%M:%S')}] ✅ Sinal enviado: {sinal}")
        except TelegramError as e:
            print(f"❌ Erro ao enviar sinal: {e}")

        await asyncio.sleep(600)  # 10 minutos

# --- Rota web do Flask ---
@app.route("/")
def home():
    return "✅ Bot Bac Bo Sinais Online!"

# --- Executa Flask em thread separada ---
def run_flask():
    app.run(host="0.0.0.0", port=10000)

# --- Inicia o bot e o servidor ---
def start():
    threading.Thread(target=run_flask).start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_signal())

if __name__ == "__main__":
    start()
