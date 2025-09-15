import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from messages import get_free_channel_message, get_vip_channel_signal

# Configuração de logging
logging.basicConfig(
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',
    level=logging.INFO
)

# Carregar variáveis de ambiente (essas serão configuradas no Render.com)
TELEGRAM_BOT_TOKEN = os.getenv(\'TELEGRAM_BOT_TOKEN\', \'YOUR_BOT_TOKEN\')
AFFILIATE_LINK = os.getenv(\'AFFILIATE_LINK\', \'https://win-agegate-promo-68.lovable.app/\')
FREE_CHANNEL_ID = os.getenv(\'FREE_CHANNEL_ID\')
VIP_CHANNEL_ID = os.getenv(\'VIP_CHANNEL_ID\')

# --- Funções do Bot ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia uma mensagem de boas-vindas quando o comando /start é emitido."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Olá! Sou o bot que vai te ajudar a alcançar seus objetivos financeiros. Vamos começar?"
    )

async def post_to_free_channel(context: ContextTypes.DEFAULT_TYPE):
    """Posta conteúdo periodicamente no canal gratuito."""
    chat_id = FREE_CHANNEL_ID
    
    messages_to_send, reply_markup = get_free_channel_message(AFFILIATE_LINK)

    for msg_content in messages_to_send:
        if isinstance(msg_content, dict) and "image" in msg_content:
            # Envia a imagem e o texto
            with open(msg_content["image"], 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=InputFile(image_file), caption=msg_content["text"])
        else:
            # Envia apenas texto
            await context.bot.send_message(chat_id=chat_id, text=msg_content, parse_mode=\'Markdown\')

    # Botão para o link de afiliado (sempre no final)
    await context.bot.send_message(
        chat_id=chat_id,
        text="👇 **Clique no botão abaixo para fazer seu cadastro, depositar e garantir sua vaga no VIP!**",
        reply_markup=reply_markup,
        parse_mode=\'Markdown\'
    )

async def post_to_vip_channel(context: ContextTypes.DEFAULT_TYPE):
    """Posta sinais periodicamente no canal VIP."""
    chat_id = VIP_CHANNEL_ID
    signal_text, cta_text = get_vip_channel_signal()
    await context.bot.send_message(chat_id=chat_id, text=signal_text, parse_mode=\'Markdown\')
    await context.bot.send_message(chat_id=chat_id, text=cta_text)

async def handle_deposit_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com o recebimento de imagens (provas de depósito)."""
    user = update.effective_user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Olá, {user.first_name}! Recebi sua imagem. Nossa equipe irá verificar seu depósito em breve. Se tudo estiver correto, você receberá o link de acesso ao Canal VIP e seus e-books. Obrigado!"
    )
    # Aqui, você poderia notificar um administrador para verificar a imagem manualmente.

def main() -> None:
    """Inicia o bot e configura os handlers e jobs."""
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers de comando
    application.add_handler(CommandHandler("start", start))

    # Handler para imagens (comprovantes de depósito)
    application.add_handler(MessageHandler(filters.PHOTO, handle_deposit_proof))

    # Jobs agendados para postar nos canais
    job_queue = application.job_queue
    # Posta no canal Free a cada 2 horas (7200 segundos)
    job_queue.run_repeating(post_to_free_channel, interval=7200, first=10)
    # Posta no canal VIP a cada 30 minutos (1800 segundos)
    job_queue.run_repeating(post_to_vip_channel, interval=1800, first=20)

    # Inicia o bot
    application.run_polling()

if __name__ == \'__main__\':
    main()

