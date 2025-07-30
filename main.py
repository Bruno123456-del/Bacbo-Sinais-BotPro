# -*- coding: utf-8 -*-
import os
import asyncio
import random
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot

# === 1. CARREGAMENTO DO AMBIENTE ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = "https://lkwn.cc/f1c1c45a"

# === 2. INICIALIZAÇÃO ===
bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

# === 3. FUNÇÃO PARA GERAR SINAL ALEATÓRIO ===
def gerar_sinal():
    cor = random.choice(["⚪ Branco", "🔴 Vermelho", "🔵 Azul"])
    return f"🎯 Sinal Bac Bo: ✅ Tudo pronto!\nEntrada: {cor}\n💰 Link: {URL_CADASTRO}"

# === 4. ENVIO DE SINAL AUTOMÁTICO A CADA 10 MINUTOS ===
async def loop_sinais():
    while True:
        mensagem = gerar_sinal()
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem)
            print("✅ Sinal enviado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao enviar sinal: {e}")
        await asyncio.sleep(600)  # 10 minutos

# === 5. ROTA DO SERVIDOR PARA VERIFICAÇÃO ===
@app.route("/")
def index():
    return "✅ Bot Bac Bo Sinais está online!"

# === 6. INICIALIZAÇÃO DO LOOP ASSÍNCRONO + FLASK ===
def start():
    loop = asyncio.get_event_loop()
    loop.create_task(loop_sinais())
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    start()
