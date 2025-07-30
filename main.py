import os
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, MessageHandler, filters, InlineQueryHandler

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Função para o comando /start
async def start(update: Update, context: Application.context) -> None:
    """Envia uma mensagem quando o comando /start é emitido."""
    user = update.effective_user
    await update.message.reply_html(
        f"Olá, {user.mention_html()}! Eu sou um bot de exemplo. Use /help para ver os comandos disponíveis.",
    )

# Função para o comando /help
async def help_command(update: Update, context: Application.context) -> None:
    """Envia uma mensagem quando o comando /help é emitido."""
    await update.message.reply_text("Comandos disponíveis:\n/start - Inicia o bot\n/help - Mostra esta mensagem de ajuda\n/echo <texto> - Repete o texto enviado\n/caps <texto> - Converte o texto para maiúsculas\n/inline - Exemplo de consulta inline")

# Função para o comando /echo
async def echo(update: Update, context: Application.context) -> None:
    """Repete a mensagem do usuário."""
    await update.message.reply_text(update.message.text.replace("/echo ", ""))

# Função para o comando /caps
async def caps(update: Update, context: Application.context) -> None:
    """Converte o texto para maiúsculas."""
    text_caps = " ".join(context.args).upper()
    await update.message.reply_text(text_caps)

# Função para lidar com mensagens de texto genéricas
async def handle_message(update: Update, context: Application.context) -> None:
    """Responde a mensagens de texto."""
    await update.message.reply_text(f"Você disse: {update.message.text}")

# Função para lidar com consultas inline
async def inline_query(update: Update, context: Application.context) -> None:
    """Lida com a consulta inline."""
    query = update.inline_query.query

    if not query:
        return

    results = [
        InlineQueryResultArticle(
            id=query.upper(),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=query.lower(),
            title="Lower",
            input_message_content=InputTextMessageContent(query.lower()),
        ),
    ]

    await update.inline_query.answer(results)


def main() -> None:
    """Inicia o bot."""
    # Obter o token do bot das variáveis de ambiente
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        logger.error("O token do bot do Telegram não foi encontrado nas variáveis de ambiente.")
        logger.error("Por favor, defina a variável de ambiente TELEGRAM_BOT_TOKEN.")
        return

    application = Application.builder().token(TOKEN).build()

    # Adicionar handlers de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("caps", caps))

    # Adicionar handler para mensagens de texto genéricas
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Adicionar handler para consultas inline
    application.add_handler(InlineQueryHandler(inline_query))

    # Iniciar o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
