import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token do bot (inserido diretamente)
BOT_TOKEN = "7975008855:AAFQfTcSn3r5HiR0eXPaimJo0K3pX7osNfw"

# IDs
FREE_CHAT_ID = -1002808626127
VIP_CHAT_ID = -1003053055680
ADMIN_ID = 5011424031

# ---------------------
# Funções do Bot
# ---------------------

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id == VIP_CHAT_ID:
        text = "Bem-vindo, VIP! ⭐"
    elif chat_id == FREE_CHAT_ID:
        text = "Bem-vindo ao grupo FREE! ✅"
    else:
        text = "Olá! Você não está nos grupos FREE ou VIP."

    keyboard = [
        [InlineKeyboardButton("Visite nosso site", url="https://superfinds.com.br")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "/start - Inicia o bot\n"
        "/help - Mostra esta mensagem\n"
        "Mais comandos serão adicionados em breve."
    )
    await update.message.reply_text(text)

# Comando de admin
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Você não tem permissão para usar este comando.")
        return
    await update.message.reply_text("Olá, Admin! Comandos de controle disponíveis.")

# Callback de botão
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Você clicou: {query.data}")

# ---------------------
# Função principal
# ---------------------

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Adiciona handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Inicia o bot
    print("Bot iniciado...")
    application.run_polling()

if __name__ == "__main__":
    main()
