import os
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Caminhos das imagens locais
WIN_ENTRADA_PATH = os.path.join("imagens", "win_entrada.png")
WIN_GALE1_PATH = os.path.join("imagens", "win_gale1.png")
WIN_GALE2_PATH = os.path.join("imagens", "win_gale2.png")

LINK_AFILIADO = "https://lkwn.cc/f1c1c45a"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    texto = (
        "🎲 *Bot BAC BO* iniciado!\n\n"
        "Use /winentrada para imagem de vitória entrada.\n"
        "Use /wingale1 para imagem de vitória gale 1.\n"
        "Use /wingale2 para imagem de vitória gale 2.\n"
    )
    
    botao = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Jogar Bac Bo", url=LINK_AFILIADO)]]
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=texto,
        parse_mode="Markdown",
        reply_markup=botao,
    )

async def winentrada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    with open(WIN_ENTRADA_PATH, "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="🎉 Vitória Entrada!",
        )

async def wingale1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    with open(WIN_GALE1_PATH, "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="🎉 Vitória Gale 1!",
        )

async def wingale2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    with open(WIN_GALE2_PATH, "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="🎉 Vitória Gale 2!",
        )

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("winentrada", winentrada))
    application.add_handler(CommandHandler("wingale1", wingale1))
    application.add_handler(CommandHandler("wingale2", wingale2))

    application.run_polling()

if __name__ == "__main__":
    main()
