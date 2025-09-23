import os
import logging
import random
import asyncio
from datetime import datetime

# Importa configurações e mensagens
from config import (
    BOT_TOKEN, FREE_CANAL_ID, VIP_CANAL_ID, ADMIN_ID,
    URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM, URL_VIP_ACESSO,
    JOGOS_COMPLETOS, GIFS_VITORIA,
    INTERVALO_SINAL_AUTOMATICO, INTERVALO_MARKETING_AUTOMATICO
)
from messages import (
    get_start_message, get_start_keyboard,
    get_vip_offer_message, get_vip_offer_keyboard,
    get_photo_received_message
)
from signal_logic import enviar_sinal_jogo

# (O resto dos imports e configurações iniciais permanecem os mesmos)
try:
    from sistema_conversao_vip import SistemaConversaoVIP
except ImportError:
    print("ERRO CRÍTICO: O arquivo 'sistema_conversao_vip.py' não foi encontrado.")
    exit()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import Conflict, BadRequest
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters, CallbackQueryHandler
)

# --- CONFIGURAÇÕES DE SEGURANÇA ---
if not BOT_TOKEN:
    print("ERRO CRÍTICO: A variável de ambiente BOT_TOKEN não foi encontrada ou está vazia.")
    exit()

# --- CONFIGURAÇÃO DE LOGGING ---
# --- CONFIGURAÇÃO DE LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    style="%"  # Corrigido: define o estilo correto de formatação
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("bot_main")

# --- FUNÇÕES AUXILIARES E DE ERRO ---
def inicializar_estatisticas(bot_data: dict):
    logger.info("Inicializando/Verificando estatísticas...")
    bot_data.setdefault("start_time", datetime.now())
    bot_data.setdefault("usuarios_unicos", set())
    bot_data.setdefault("conversoes_vip", 0)
    bot_data.setdefault("sinais_vip", 0)
    bot_data.setdefault("win_primeira_vip", 0)
    bot_data.setdefault("win_gale_vip", 0)
    bot_data.setdefault("loss_vip", 0)
    logger.info("Estatísticas OK.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exceção ao manipular uma atualização: {context.error}", exc_info=context.error)
    if isinstance(context.error, Conflict):
        logger.warning("ERRO DE CONFLITO DETECTADO. Outra instância do bot pode estar rodando.")
    elif isinstance(context.error, BadRequest) and "Failed to get content from URL" in str(context.error):
        logger.error(f"ERRO DE URL INVÁLIDA: Não foi possível baixar o conteúdo. Verifique as URLs de GIFs e Imagens.")
    elif isinstance(context.error, KeyError):
        logger.critical(f"KeyError: {context.error}. Isso pode indicar um problema de inicialização. Reiniciando estatísticas.")
        inicializar_estatisticas(context.bot_data)

# --- COMANDOS E INTERAÇÕES DO BOT ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome_usuario = user.first_name or "Campeão"
    if user.id not in context.bot_data["usuarios_unicos"]:
        context.bot_data["usuarios_unicos"].add(user.id)
        logger.info(f"Novo usuário capturado pelo funil: {nome_usuario} ({user.id})")

    mensagem = get_start_message(nome_usuario)
    keyboard = InlineKeyboardMarkup(get_start_keyboard())
    
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_caption(caption=mensagem, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    else:
        await context.bot.send_animation(chat_id=user.id, animation=random.choice(GIFS_VITORIA), caption=mensagem, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

# --- CALLBACKS E EVENTOS ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    
    if query.data == "oferta_vip":
        await query.answer()
        mensagem = get_vip_offer_message(user.first_name)
        keyboard = InlineKeyboardMarkup(get_vip_offer_keyboard())
        try:
            await query.edit_message_caption(caption=mensagem, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        except BadRequest:
            await query.edit_message_text(text=mensagem, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    sistema_conversao = context.bot_data.get("sistema_conversao")
    if sistema_conversao:
        await sistema_conversao.processar_comprovante_deposito(user.id, user.first_name)
    else:
        await update.message.reply_text(get_photo_received_message())

# --- AGENDAMENTOS ---
async def enviar_sinal_automatico(context: ContextTypes.DEFAULT_TYPE):
    jogo = random.choice(list(JOGOS_COMPLETOS.keys()))
    confianca_vip = random.uniform(0.90, 0.98)
    await enviar_sinal_jogo(context, jogo, VIP_CANAL_ID, confianca_vip)
    # O sleep entre os envios VIP e FREE é para simular um atraso e criar a sensação de exclusividade
    await asyncio.sleep(random.randint(15, 45)) 
    await enviar_sinal_jogo(context, jogo, FREE_CANAL_ID, confianca_vip)

async def enviar_marketing_automatico(context: ContextTypes.DEFAULT_TYPE):
    sistema_conversao = context.bot_data.get("sistema_conversao")
    if not sistema_conversao: return
    await sistema_conversao.enviar_campanha_marketing(FREE_CANAL_ID)

# --- FUNÇÃO PRINCIPAL ---
def main():
    logger.info("Iniciando o bot...")
    persistence = PicklePersistence(filepath="bot_data.pkl")
    
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()
    inicializar_estatisticas(app.bot_data)

    sistema_conversao = SistemaConversaoVIP(app, URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM, URL_VIP_ACESSO)
    app.bot_data["sistema_conversao"] = sistema_conversao

    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("start", start_command))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))

    jq = app.job_queue
    jq.run_repeating(enviar_sinal_automatico, interval=INTERVALO_SINAL_AUTOMATICO, first=10)
    jq.run_repeating(enviar_marketing_automatico, interval=INTERVALO_MARKETING_AUTOMATICO, first=30)

    logger.info("🚀 Bot do Júnior Moreira V27.0 iniciado com sucesso!")
    logger.info(f"🎮 {len(JOGOS_COMPLETOS)} jogos sendo analisados!")
    logger.info("💎 Sistema de conversão VIP ativado!")
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()


