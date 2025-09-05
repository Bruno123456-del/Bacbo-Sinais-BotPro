# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 19.0 "ROBUSTO"
# ===================================================================================

import logging
import os
import random
import threading
from datetime import datetime, timedelta, time as dtime
from flask import Flask

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, PicklePersistence
)

# -----------------------------------------------------------------------------------
# CONFIGURAÇÃO DE LOG
# -----------------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------------
# CLASSE DE CONFIGURAÇÃO
# -----------------------------------------------------------------------------------
class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")  # Canal Free
    VIP_CANAL_ID = os.getenv("VIP_CANAL_ID")
    ADMIN_ID = os.getenv("ADMIN_ID")
    VIP_ACCESS_LINK = os.getenv("VIP_ACCESS_LINK", "https://t.me/seulinkvip")

    @staticmethod
    def validate():
        required = ["BOT_TOKEN", "CHAT_ID", "VIP_CANAL_ID", "ADMIN_ID"]
        for var in required:
            if not getattr(Config, var):
                raise ValueError(f"⚠️ Variável obrigatória faltando: {var}")

CONFIG = Config()
CONFIG.validate()

# -----------------------------------------------------------------------------------
# GESTOR DE JOGOS
# -----------------------------------------------------------------------------------
class GameManager:
    def __init__(self):
        self.games = {
            "bacbo": {"emoji": "🎲", "nome": "Bac Bo"},
            "roleta": {"emoji": "🎡", "nome": "Roleta"},
            "blackjack": {"emoji": "🃏", "nome": "Blackjack"},
        }

    def get_game(self, game_name: str):
        return self.games.get(game_name.lower())

GAME_MANAGER = GameManager()

# -----------------------------------------------------------------------------------
# GESTOR DE ESTATÍSTICAS
# -----------------------------------------------------------------------------------
class StatsManager:
    def __init__(self, bot_data):
        self.bot_data = bot_data
        if "stats" not in self.bot_data:
            self.bot_data["stats"] = {"wins": 0, "losses": 0, "date": datetime.now().date()}

    def add_win(self):
        self.bot_data["stats"]["wins"] += 1

    def add_loss(self):
        self.bot_data["stats"]["losses"] += 1

    def reset_daily(self):
        today = datetime.now().date()
        if self.bot_data["stats"]["date"] != today:
            self.bot_data["stats"] = {"wins": 0, "losses": 0, "date": today}
# -----------------------------------------------------------------------------------
# HANDLERS DE COMANDOS
# -----------------------------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bem-vindo ao BOT DE SINAIS!\n"
        "Comandos:\n"
        "/sinal [jogo] free|vip\n"
        "/placar\n"
        "/stats\n"
        "/autosinal"
    )

async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(CONFIG.ADMIN_ID):
        await update.message.reply_text("🚫 Apenas admin pode enviar sinais manuais.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /sinal [jogo] free|vip")
        return

    game_name, channel_type = context.args[0], context.args[1]
    game = GAME_MANAGER.get_game(game_name)
    if not game:
        await update.message.reply_text("Jogo inválido.")
        return

    await send_signal(context, game_name, channel_type)
    await update.message.reply_text(f"Sinal enviado para {channel_type.upper()}.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = StatsManager(context.bot_data)
    s = context.bot_data["stats"]
    await update.message.reply_text(f"📊 Wins: {s['wins']} | Losses: {s['losses']}")

async def placar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = context.bot_data["stats"]
    total = s["wins"] + s["losses"]
    pct = (s["wins"] / total * 100) if total > 0 else 0
    await update.message.reply_text(
        f"🏆 Placar do dia:\n"
        f"Wins: {s['wins']}\nLosses: {s['losses']}\nAssertividade: {pct:.2f}%"
    )

async def autosinal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(CONFIG.ADMIN_ID):
        return
    current = context.bot_data.get("autosinal_enabled", True)
    context.bot_data["autosinal_enabled"] = not current
    status = "✅ LIGADO" if context.bot_data["autosinal_enabled"] else "❌ DESLIGADO"
    await update.message.reply_text(f"🔄 Autosinal agora está {status}.")

# -----------------------------------------------------------------------------------
# ENVIO DE SINAL
# -----------------------------------------------------------------------------------
async def send_signal(context: ContextTypes.DEFAULT_TYPE, game_name: str, channel_type="free"):
    game = GAME_MANAGER.get_game(game_name)
    if not game:
        return

    # Decide canal
    chat_id = CONFIG.CHAT_ID if channel_type == "free" else CONFIG.VIP_CANAL_ID

    # Simulação resultado
    result = random.choice(["green", "red"])
    if result == "green":
        StatsManager(context.bot_data).add_win()
        text = f"{game['emoji']} Sinal {game['nome']} → ✅ GREEN"
    else:
        StatsManager(context.bot_data).add_loss()
        text = f"{game['emoji']} Sinal {game['nome']} → ❌ RED"

    await context.bot.send_message(chat_id=chat_id, text=text)
# -----------------------------------------------------------------------------------
# JOBS AUTOMÁTICOS
# -----------------------------------------------------------------------------------
OPERATING_START = 8
OPERATING_END = 23
SIGNAL_INTERVAL_MINUTES = 35

async def send_auto_signal_job(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    if not (OPERATING_START <= now.hour < OPERATING_END):
        return
    if not context.bot_data.get("autosinal_enabled", True):
        return

    game_name = random.choice(list(GAME_MANAGER.games.keys()))
    await send_signal(context, game_name, "free")

async def reset_daily_stats_job(context: ContextTypes.DEFAULT_TYPE):
    StatsManager(context.bot_data).reset_daily()

# -----------------------------------------------------------------------------------
# FLASK PARA RENDER
# -----------------------------------------------------------------------------------
def start_flask():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Bot ativo no Render ✅"

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# -----------------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------------
def main():
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(CONFIG.BOT_TOKEN).persistence(persistence).build()

    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("sinal", signal_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("placar", placar_command))
    app.add_handler(CommandHandler("autosinal", autosinal_command))

    # Jobs
    app.job_queue.run_repeating(
        send_auto_signal_job,
        interval=timedelta(minutes=SIGNAL_INTERVAL_MINUTES),
        first=15,
        name="autosinal"
    )
    app.job_queue.run_daily(
        reset_daily_stats_job,
        time=dtime(hour=0, minute=0, second=5),
        name="reset"
    )

    # Flask paralelo
    threading.Thread(target=start_flask, daemon=True).start()

    logger.info("🚀 Bot iniciado com sucesso!")
    app.run_polling()

if __name__ == "__main__":
    main()
