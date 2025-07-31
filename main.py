import os
import asyncio
import random
import threading
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.error import TelegramError

# --- Carregando variáveis ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO")

# Verificação de segurança
if not TOKEN or not CHAT_ID or not URL_CADASTRO:
    raise ValueError("❌ BOT_TOKEN, CHAT_ID ou URL_CADASTRO não definidos no .env")

# --- Inicialização ---
bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

# --- Estratégia: Escada Asiática com Cobertura (Amarelo) ---
def gerar_entrada():
    cores = ["🔴 Vermelho", "🔵 Azul"]
    principal = random.choice(cores)
    return principal, "🟡 Amarelo (Cobertura)"

# --- Envio de sinal com gestão e botão ---
async def enviar_sinal():
    entrada, cobertura = gerar_entrada()
    hora = datetime.now().strftime("%H:%M")

    texto = (
        f"🧠 *SINAL ESTRATÉGICO BAC BO*\n"
        f"🕒 {hora}\n\n"
        f"🎰 Entrada principal: {entrada}\n"
        f"🟡 Cobertura: {cobertura}\n\n"
        f"💸 *Gestão de risco ativada:*\n"
        f"• 1ª entrada\n"
        f"• G1 se necessário\n"
        f"• G2 final\n\n"
        f"🎁 Bônus de boas-vindas disponível!\n"
    )

    # Botão personalizado
    botao = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Jogar Bac Bo", url=URL_CADASTRO)]
    ])

    try:
        # Envia mensagem com botão
        await bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown", reply_markup=botao)

        # Envia imagem de gestão de risco
        with open("imagens/gestao.png", "rb") as img:
            await bot.send_photo(chat_id=CHAT_ID, photo=img, caption="📊 Gestão de risco aplicada com sucesso!")

        # Envia GIF animado de vitória como estímulo
        with open("imagens/win.gif", "rb") as gif:
            await bot.send_animation(chat_id=CHAT_ID, animation=gif, caption="🔥 Confiança é tudo. Siga a estratégia!")

        print(f"[{hora}] ✅ Sinal enviado com entrada: {entrada}")

    except TelegramError as e:
        print(f"❌ Erro ao enviar sinal: {e}")

# --- Loop de envio automático a cada 10min ---
async def agendar_sinais():
    while True:
        await enviar_sinal()
        await asyncio.sleep(600)

# --- Página Flask (status) ---
@app.route("/")
def status():
    return "✅ BOT BAC BO ONLINE — Estratégia Escada com Cobertura ativa"

# --- Inicia servidor Flask paralelo ao loop de sinais ---
def run_flask():
    app.run(host="0.0.0.0", port=10000)

def start():
    threading.Thread(target=run_flask).start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(agendar_sinais())

if __name__ == "__main__":
    start()
