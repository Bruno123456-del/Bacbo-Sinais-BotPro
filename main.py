# -*- coding: utf-8 -*-
import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =====================================================================
# CONFIGURAÇÕES INICIAIS
# =====================================================================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = os.getenv("CANAL_ID")
VIP_CANAL_ID = os.getenv("VIP_CANAL_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# =====================================================================
# HANDLERS DE COMANDOS
# =====================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot de Sinais iniciado!\n\n"
        "📌 Você receberá sinais automáticos aqui nos canais configurados."
    )

# =====================================================================
# JOBS AUTOMÁTICOS
# =====================================================================
async def autosinal_estrategico(context: ContextTypes.DEFAULT_TYPE):
    """Sinal grátis a cada 25 minutos"""
    await context.bot.send_message(
        chat_id=CANAL_ID,
        text="🎯 SINAL FREE ➝ Entrada estratégica liberada!\n👉 Aproveite AGORA!"
    )

async def autosinal_vip(context: ContextTypes.DEFAULT_TYPE):
    """Sinal VIP a cada 15 minutos"""
    await context.bot.send_message(
        chat_id=VIP_CANAL_ID,
        text="🔥 SINAL VIP EXCLUSIVO 🔥\n✅ Alta probabilidade\n🚀 Gestão de banca aplicada"
    )

async def verificar_vips_expirados(context: ContextTypes.DEFAULT_TYPE):
    """Verifica assinaturas expiradas (exemplo placeholder)"""
    logger.info("🔎 Verificando VIPs expirados...")

# =====================================================================
# FLASK (KEEP ALIVE)
# =====================================================================
app_flask = Flask(__name__)
CORS(app_flask)

@app_flask.route("/")
def home():
    return "✅ Bot de Sinais Bac Bo rodando!"

# =====================================================================
# MAIN
# =====================================================================
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Comandos básicos
    application.add_handler(CommandHandler("start", start))

    # JOBS AUTOMÁTICOS
    job_queue = application.job_queue
    job_queue.run_repeating(autosinal_estrategico, interval=1500, first=10)  # 25 min
    job_queue.run_repeating(autosinal_vip, interval=900, first=20)           # 15 min
    job_queue.run_repeating(verificar_vips_expirados, interval=3600, first=30)  # 1h

    # Iniciar bot em paralelo com Flask
    from threading import Thread
    Thread(target=lambda: app_flask.run(host="0.0.0.0", port=10000)).start()

    logger.info("🤖 Bot iniciado com sucesso!")
    application.run_polling()

# =====================================================================
# EXECUÇÃO
# =====================================================================
if __name__ == "__main__":
    main()
