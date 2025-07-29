from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text("Bot iniciado!")

def main():
    application = Application.builder().token("SEU_TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
