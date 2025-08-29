# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - BAC BO 🔥
# VERSÃO 20.0 (ROBUSTO, MODULAR E PROFISSIONAL)
# ===================================================================================

import os
import random
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Configuração de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Carregar variáveis do .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Inicializar Bot
bot = Bot(token=BOT_TOKEN)

# Lista de frases de motivação / prova social
PROVAS_SOCIAIS = [
    "🔥 'Lucro garantido, gratidão demais!' – João S.",
    "💎 'Primeira vez que vejo consistência assim!' – Maria R.",
    "🚀 'Dobrei minha banca em 2 dias!' – Carlos M.",
    "🤑 'Esse grupo é surreal, obrigado!' – Fernanda T.",
    "🔥 'Ganhei R$ 540 só hoje, sem acreditar!' – Pedro H."
]
# Função para gerar um sinal aleatório (simulação)
def gerar_sinal():
    opcoes = ["🔴 Vermelho", "🔵 Azul", "🟡 Empate (Cobertura)"]
    escolha = random.choice(opcoes)
    return f"🎯 SINAL ENCONTRADO: {escolha}\n⚡ Gestão: 1 entrada fixa\n🚨 Estrategia Escada Asiática"

# Função para enviar provas sociais (mensagens motivacionais)
async def enviar_prova_social(app: Application):
    mensagem = random.choice(PROVAS_SOCIAIS)
    try:
        await app.bot.send_message(chat_id=CANAL_ID, text=mensagem)
    except Exception as e:
        logging.error(f"Erro ao enviar prova social: {e}")

# Função para enviar sinais automáticos
async def enviar_sinal(app: Application):
    sinal = gerar_sinal()
    botao = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Jogar Bac Bo", url="https://lkwn.cc/f1c1c45a")]
    ])
    try:
        await app.bot.send_message(chat_id=CANAL_ID, text=sinal, reply_markup=botao)
        logging.info("Sinal enviado com sucesso")
    except Exception as e:
        logging.error(f"Erro ao enviar sinal: {e}")
# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Canal VIP", url="https://t.me/+SeuCanalVIP")],
        [InlineKeyboardButton("🎲 Jogar Bac Bo", url="https://lkwn.cc/f1c1c45a")]
    ])
    await update.message.reply_text(
        "🤖 Bem-vindo ao BOT de SINAIS BAC BO!\n\n"
        "Aqui você recebe sinais gratuitos diariamente.\n"
        "Quer ganhar ainda mais? Conheça o nosso VIP!",
        reply_markup=teclado
    )

# /ajuda
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Comandos disponíveis:\n"
        "/start - Mensagem inicial\n"
        "/ajuda - Lista de comandos\n"
        "/vip - Informações do VIP\n"
        "/suporte - Contato com o suporte"
    )

# /vip
async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Nosso VIP é exclusivo e limitado!\n\n"
        "✅ Sinais 24h\n"
        "✅ Estratégia Escada Asiática\n"
        "✅ Suporte individual\n\n"
        "👉 Acesse agora: https://t.me/+SeuCanalVIP"
    )

# /suporte
async def suporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📩 Suporte: @SeuUsuarioSuporte")

# /admin (apenas admin)
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("🔐 Painel Admin:\n- Enviar sinal manual\n- Ver estatísticas")
    else:
        await update.message.reply_text("❌ Você não tem permissão para acessar esse comando.")
# Função principal de execução
async def executar_rotinas(app: Application):
    while True:
        await enviar_sinal(app)
        await asyncio.sleep(600)  # envia sinal a cada 10 minutos
        await enviar_prova_social(app)

# Inicializar Bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("suporte", suporte))
    app.add_handler(CommandHandler("admin", admin))

    # Iniciar loops paralelos
    app.job_queue.run_once(lambda ctx: executar_rotinas(app), 1)

    # Rodar bot
    app.run_polling()

if __name__ == "__main__":
    main()
