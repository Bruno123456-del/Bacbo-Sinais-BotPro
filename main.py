# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS VIP/FREE - VERSÃO 20.0 "CONVERSÃO MÁXIMA"
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, JobQueue
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv

# ==========================================
# CARREGANDO VARIÁVEIS DE AMBIENTE
# ==========================================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))         # Canal Free
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID")) # Canal VIP
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ==========================================
# LOGS
# ==========================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================
# LISTAS E VARIÁVEIS GLOBAIS
# ==========================================
usuarios_vip = set()        # Guarda IDs VIP
usuarios_free = set()       # Guarda IDs Free
mensagens_free = [
    "💥 Sinal Free: Ganhe com segurança! Para desbloquear VIP e bônus exclusivos clique abaixo.",
    "🚀 Últimos resultados Free: Quem entra no VIP garante acesso completo e bônus."
]
mensagens_vip = [
    "🏝️ Bem-vindo ao VIP! Aqui você desbloqueia bônus exclusivos: 600 viagens, ebook profissional, 3 jogos e esportes.",
    "💰 Gestão de banca avançada: juros compostos + mala de dinheiro + viagem para Dubai!"
]
mensagem_urgencia = (
    "⚠️ Vagas restantes! Acabei de receber autorização para liberar apenas os cupos restantes.\n"
    "⏳ Gestão vai ter acesso por 90 dias grátis + bônus de 600 viages + 2 eBooks Profissionais + 3 jogos e esportes!\n"
    "📌 Entre agora e garanta seu lugar VIP!"
)

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================
async def enviar_mensagem_free(update: Update, contexto: ContextTypes.DEFAULT_TYPE):
    """Envia sinais Free e persuasivos para conversão."""
    msg = random.choice(mensagens_free)
    bot = contexto.bot
    await bot.send_message(chat_id=CANAL_ID, text=msg)
    logger.info("Mensagem Free enviada")

async def enviar_mensagem_vip(update: Update, contexto: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Envia sinais VIP apenas para usuários VIP."""
    if user_id not in usuarios_vip:
        logger.info(f"Usuário {user_id} não é VIP, bloqueando mensagem")
        return
    msg = random.choice(mensagens_vip)
    bot = contexto.bot
    await bot.send_message(chat_id=VIP_CANAL_ID, text=msg)
    logger.info(f"Mensagem VIP enviada para {user_id}")

async def mensagem_urgente_vip(bot, user_id: int):
    """Mensagem de urgência com bônus agressivos."""
    await bot.send_message(chat_id=user_id, text=mensagem_urgencia)
    logger.info(f"Mensagem de urgência VIP enviada para {user_id}")

# ==========================================
# FUNÇÃO DE AUTOSINAL
# ==========================================
async def autosinal(context: ContextTypes.DEFAULT_TYPE):
    """Sinal periódico Free para conversão."""
    bot = context.bot
    await enviar_mensagem_free(None, context)
    # Envia urgência para alguns usuários Free aleatórios
    for user_id in list(usuarios_free)[:5]:  # só 5 aleatórios por vez
        await mensagem_urgente_vip(bot, user_id)
# ==========================================
# HANDLERS DE COMANDOS
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    usuarios_free.add(user_id)
    await update.message.reply_text(
        "👋 Bem-vindo! Você está no Free Signals.\n"
        "💡 Para desbloquear VIP e bônus incríveis clique no botão abaixo.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔓 Entrar VIP", url="https://win-agegate-promo-68.lovable.app/")]
        ])
    )

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adiciona usuário ao VIP manualmente (Admin)"""
    user_id = int(context.args[0])
    usuarios_vip.add(user_id)
    usuarios_free.discard(user_id)
    await update.message.reply_text(f"✅ Usuário {user_id} promovido a VIP!")
    logger.info(f"Usuário {user_id} adicionado ao VIP")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra status atual dos usuários"""
    await update.message.reply_text(
        f"Usuarios Free: {len(usuarios_free)}\nUsuarios VIP: {len(usuarios_vip)}"
    )

# ==========================================
# CONFIGURAÇÃO DO AGENDADOR
# ==========================================
scheduler = AsyncIOScheduler()

scheduler.add_job(
    autosinal,
    trigger=IntervalTrigger(minutes=35),
    kwargs={},
    id="autosinal",
    replace_existing=True
)

# ==========================================
# INICIALIZAÇÃO DO BOT
# ==========================================
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("status", status))
    # Iniciar agendador
    scheduler.start()
    # Rodar bot
    await app.start()
    logger.info("🚀 Bot iniciado com sucesso!")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
