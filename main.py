# -*- coding: utf-8 -*-
# BOT DE SINAIS VIP/FREE - PARTE 1
import asyncio
import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Defina no Render → Environment

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Funções de envio (usam 'context' como nos handlers do PTB)
async def enviar_sinal_free_limitado(context: ContextTypes.DEFAULT_TYPE):
    logger.info("📢 Enviando sinal FREE limitado...")
    await context.bot.send_message(
        chat_id="-1001234567890",  # substitua pelo seu canal/grupo
        text="🎯 SINAL FREE ➝ Entrada estratégica liberada!\n👉 Aproveite AGORA!"
    )

async def enviar_sinal_vip_exclusivo(context: ContextTypes.DEFAULT_TYPE):
    logger.info("💎 Enviando sinal VIP exclusivo...")
    await context.bot.send_message(
        chat_id="-1001234567890",
        text="🔥 SINAL VIP EXCLUSIVO 🔥\n✅ Alta probabilidade\n🚀 Gestão de banca aplicada"
    )

async def enviar_oferta_urgente(bot, user_id: int):
    logger.info(f"⚡ Enviando oferta urgente para {user_id}")
    await bot.send_message(
        chat_id=user_id,
        text="⚡ OFERTA URGENTE ⚡\n💎 Torne-se VIP e receba os melhores sinais!"
    )
# BOT DE SINAIS VIP/FREE - PARTE 2

# Handlers de comando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Novo usuário: {update.effective_user.id}")
    await update.message.reply_text(
        "🤖 Bem-vindo ao BOT DE SINAIS!\n\n"
        "🎯 Digite /vip para conhecer o plano exclusivo.\n"
        "📊 Digite /status para ver o status do bot."
    )

async def promover_vip_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 Seja VIP e receba os melhores sinais!\n"
        "👉 Acesse agora: https://seulink.com/vip"
    )

async def status_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot operacional e enviando sinais normalmente!")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="📌 Você clicou em um botão interativo!")

# Funções agendadas — mantêm assinatura com 'context'
async def autosinal_estrategico(context: ContextTypes.DEFAULT_TYPE):
    await enviar_sinal_free_limitado(context)

async def autosinal_vip(context: ContextTypes.DEFAULT_TYPE):
    await enviar_sinal_vip_exclusivo(context)

async def verificar_vips_expirados(context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔎 Verificando VIPs expirados...")

# Função principal corrigida
async def main():
    logger.info("🚀 Iniciando Bot de Sinais Estratégico...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", promover_vip_comando))
    app.add_handler(CommandHandler("status", status_bot))
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Inicializa e inicia o bot ANTES de ligar o scheduler
    await app.initialize()
    await app.start()
    logger.info("🤖 Bot iniciado com sucesso!")

    # Agendador: PASSAMOS o app como 'context' para as funções agendadas
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        autosinal_estrategico,
        trigger=IntervalTrigger(minutes=25),
        kwargs={'context': app}   # <-- CORREÇÃO IMPORTANTE
    )
    scheduler.add_job(
        autosinal_vip,
        trigger=IntervalTrigger(minutes=15),
        kwargs={'context': app}   # <-- CORREÇÃO IMPORTANTE
    )
    scheduler.add_job(
        verificar_vips_expirados,
        trigger=IntervalTrigger(hours=1),
        kwargs={'context': app}   # <-- CORREÇÃO IMPORTANTE
    )
    scheduler.start()
    logger.info("📅 Agendador de tarefas iniciado")

    # Iniciar polling (mantive seu padrão; se quiser, altero para run_polling())
    await app.updater.start_polling()
    await app.updater.idle()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
    finally:
        logger.info("🔚 Bot finalizado")
