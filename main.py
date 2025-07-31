import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Habilitar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Definir alguns manipuladores de comando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /start é emitido."""
    user = update.effective_user
    await update.message.reply_html(
        f"Olá {user.mention_html()}!",
    )
[31/07, 11:54] ...: async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /help é emitido."""
    await update.message.reply_text("Use /start para começar.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ecoa a mensagem do usuário."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Inicia o bot."""
    # Crie o Application e passe o token do seu bot. Substitua 'YOUR_BOT_TOKEN' pelo seu token real.
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
[31/07, 11:55] ...: # Em diferentes comandos, use diferentes manipuladores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Em mensagens não-comando, ecoa a mensagem
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Execute o bot até que o usuário pressione Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
[31/07, 11:55] ...: if __name__ == "__main__":
    main()
