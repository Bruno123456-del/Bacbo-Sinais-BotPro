import os
import asyncio
import random
import threading
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaAnimation
from telegram.error import TelegramError

# --- Carregando variáveis ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a")

bot = Bot(token=TOKEN)

# --- Flask App ---
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Bot Bac Bo Online!"

# --- Funções de Sinais ---
sinais = ["⚪️⚪️🔴🔴", "🔵🔵⚪️⚪️", "🔴🔴🔵🔵"]

def gerar_sinal():
    return random.choice(sinais)

def enviar_sinal():
    agora = datetime.now().strftime('%H:%M')
    sinal = gerar_sinal()
    
    mensagem = f"""
🎯 NOVO SINAL GERADO 🎯
⏰ Horário: {agora}
🎰 Jogo: BAC BO
🎲 Entrada: {sinal}

⚠️ Apostar até 30 segundos antes!
🎯 Estratégia: Escada Asiática com Cobertura Amarela
🛡️ Cobertura: Empate (Amarelo)

🎁 Bônus de Cadastro + Giros Grátis:
👉 {URL_CADASTRO}
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Jogar Bac Bo Agora", url=URL_CADASTRO)]
    ])

    try:
        bot.send_message(chat_id=CHAT_ID, text=mensagem, reply_markup=keyboard)

        # Enviar imagem conforme tipo
        if "🔴🔴" in sinal or "⚪️⚪️" in sinal or "🔵🔵" in sinal:
            with open("imagens/win-futurista.gif", "rb") as gif:
                bot.send_animation(chat_id=CHAT_ID, animation=gif)
        
        # Opcional: se quiser enviar algo para empate, pode adaptar com lógica diferente
        if "empate" in sinal.lower():  # se você quiser que alguma palavra gere o empate
            with open("imagens/empate.gif", "rb") as empate_img:
                bot.send_animation(chat_id=CHAT_ID, animation=empate_img)

    except TelegramError as e:
        print(f"Erro ao enviar sinal: {e}")

# --- Loop Assíncrono de Sinais ---
async def loop_sinais():
    while True:
        enviar_sinal()
        await asyncio.sleep(600)  # Envia a cada 10 minutos

def iniciar_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_sinais())

# --- Iniciar Thread ---
threading.Thread(target=iniciar_loop).start()
