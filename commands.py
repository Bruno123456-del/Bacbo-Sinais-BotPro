# commands.py (modificado)
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID, JOGOS
# Importações atualizadas
from messages import get_placar_message, get_bonus_message, get_welcome_message, get_private_start_message, get_strategy_explanation

logger = logging.getLogger(__name__)

# _ATUALIZADO_ /start agora usa a nova mensagem com botões
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto, botoes = get_private_start_message()
    await update.message.reply_text(
        texto,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(botoes)
    )

# _NOVO_ Comando /comecar para o canal
async def comecar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Envia a mensagem de boas-vindas e a fixa no canal
    mensagem_enviada = await update.message.reply_text(
        get_welcome_message(),
        parse_mode='Markdown',
        disable_web_page_preview=True # Impede o Telegram de mostrar prévias dos links
    )
    try:
        await context.bot.pin_chat_message(
            chat_id=update.effective_chat.id,
            message_id=mensagem_enviada.message_id,
            disable_notification=True
        )
        await update.message.delete() # Deleta o comando "/comecar" digitado pelo admin
    except Exception as e:
        logger.error(f"Erro ao fixar mensagem: {e}. O bot tem permissão de admin?")

# _NOVO_ Callback para o botão "Explicar Estratégia"
async def strategy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        text=get_strategy_explanation(),
        parse_mode='Markdown'
    )

# Mantenha as outras funções de comando (placar_command, admin_command, etc.) aqui.
# ...
