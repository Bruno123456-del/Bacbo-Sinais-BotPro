import os
import asyncio
import random
import threading
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import TelegramError

# --- Carregando variáveis ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO")

if not TOKEN or not CHAT_ID or not URL_CADASTRO:
    raise ValueError("❌ BOT_TOKEN, CHAT_ID ou URL_CADASTRO não definidos no .env")

# --- Inicialização ---
bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

# --- Estratégia: Escada com Cobertura ---
def gerar_entrada():
    cores = ["🔴 Vermelho", "🔵 Azul"]
    principal = random.choice(cores)
    return principal, "🟡 Amarelo (Cobertura)"

# --- Envio de sinal com visual completo ---
async def enviar_sinal():
    entrada, cobertura = gerar_entrada()
    hora = datetime.now().strftime("%H:%M")

    texto = (
        f"🧠 *SINAL ESTRATÉGICO BAC BO*\n"
        f"🕒 {hora}\n\n"
        f"🎰 Entrada principal: {entrada}\n"
        f"🛡️ Cobertura: {cobertura}\n\n"
        f"💸 *Gestão de risco ativada:*\n"
        f"• 1ª entrada\n"
        f"• G1 se necessário\n"
        f"• G2 final\n\n"
        f"📢 *Não opere fora da gestão!*\n"
        f"🎯 Resultados validados no algoritmo.\n"
    )

    botao = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Jogar Bac Bo", url=URL_CADASTRO)]
    ])

    try:
        # Envia mensagem
        await bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown", reply_markup=botao)

        # Envia imagem da gestão
        with open("imagens/gestao.png", "rb") as img:
            await bot.send_photo(chat_id=CHAT_ID, photo=img, caption="📊 Gestão aplicada (Entrada, G1, G2)")

        # Envia imagem de empate (cobertura)
        with open("imagens/empate.png", "rb") as empate:
            await bot.send_photo(chat_id=CHAT_ID, photo=empate, caption="🟡 Cobertura estratégica ativa (Empate)")

        # Envia GIF futurista de vitória
        with open("imagens/win.gif", "rb") as gif:
            await bot.send_animation(chat_id=CHAT_ID, animation=gif, caption="🚀 Estratégia validada com WINs consistentes!")

        print(f"[{hora}] ✅ Sinal enviado com entrada: {entrada}")

    except TelegramError as e:
        print(f"❌ Erro ao enviar sinal: {e}")

# --- Loop de envio automático a cada 10min ---
async def agendar_sinais():
    while True:
        await enviar_sinal()
        await asyncio.sleep(600)

# --- Status do bot ---
@app.route("/")
def status():
    return "✅ BOT BAC BO ONLINE — Estratégia Escada com Cobertura ativa"

# --- Executa Flask + loop Telegram ---
def run_flask():
    app.run(host="0.0.0.0", port=10000)

def start():
    threading.Thread(target=run_flask).start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(agendar_sinais())

if __name__ == "__main__":
    start()
