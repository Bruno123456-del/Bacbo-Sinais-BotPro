import os
import random
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Logs visíveis no Render
logging.basicConfig(level=logging.INFO)

# Carrega .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Caminhos
IMAGEM_PATHS = {
    "entrada": os.path.join("imagens", "win_entrada.png"),
    "gale1": os.path.join("imagens", "win_gale1.png"),
    "gale2": os.path.join("imagens", "win_gale2.png"),
}
GIF_PATHS = [
    os.path.join("imagens", "gifs", "green1.gif"),
    os.path.join("imagens", "gifs", "green2.gif"),
    os.path.join("imagens", "gifs", "green3.gif"),
]
LINK_AFILIADO = "https://lkwn.cc/f1c1c45a"

# Frases motivacionais rotativas
FRASES = [
    "💡 Já está usando a mesma plataforma que a gente?",
    "🎁 Cadastre-se e ganhe bônus de boas-vindas!",
    "📊 A consistência é o segredo dos milionários.",
    "🤖 Nosso algoritmo trabalha 24h para você.",
    "🚀 O sucesso começa com um passo. Clique abaixo!",
]

# === COMANDOS ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    frase = random.choice(FRASES)

    texto = (
        "🎲 *Bot BAC BO* iniciado!\n\n"
        "Use os comandos abaixo para interagir com o bot:\n"
        "/winentrada - Imagem de vitória na entrada\n"
        "/wingale1 - Imagem de vitória na Gale 1\n"
        "/wingale2 - Imagem de vitória na Gale 2\n"
    )
    botao = InlineKeyboardMarkup([[InlineKeyboardButton("🎰 Jogar Bac Bo", url=LINK_AFILIADO)]])

    await context.bot.send_message(chat_id=chat_id, text=texto, parse_mode="Markdown", reply_markup=botao)
    await context.bot.send_message(chat_id=chat_id, text=frase)

async def enviar_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE, tipo: str):
    try:
        chat_id = update.effective_chat.id
        with open(IMAGEM_PATHS[tipo], "rb") as img:
            await context.bot.send_photo(chat_id=chat_id, photo=img, caption=f"🎉 Vitória {tipo.capitalize()}!")

        # Envia um GIF comemorativo aleatório
        gif_path = random.choice(GIF_PATHS)
        with open(gif_path, "rb") as gif:
            await context.bot.send_animation(chat_id=chat_id, animation=gif)

        # Botões de interação
        botoes = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Green", callback_data="green"),
                InlineKeyboardButton("🔴 Red", callback_data="red"),
            ]
        ])
        await context.bot.send_message(chat_id=chat_id, text="Resultado da sua entrada:", reply_markup=botoes)

        # Frase de engajamento
        frase = random.choice(FRASES)
        await context.bot.send_message(chat_id=chat_id, text=frase)

        logging.info(f"[SUCESSO] Enviou imagem e GIF do tipo: {tipo} para {chat_id}")
    except Exception as e:
        logging.error(f"[ERRO] ao enviar {tipo}: {str(e)}")

async def winentrada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_imagem(update, context, "entrada")

async def wingale1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_imagem(update, context, "gale1")

async def wingale2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_imagem(update, context, "gale2")

# === BOTÕES DE GREEN/RED ===

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    resultado = "✅ GREEN! Parabéns! 🟢" if query.data == "green" else "🔴 RED! Gestão é tudo. ⚠️"
    await query.edit_message_text(text=resultado)

    logging.info(f"[BOTÃO] {query.data.upper()} clicado por {query.from_user.username or query.from_user.id}")

# === INICIALIZAÇÃO DO BOT ===

def start_bot():
    if not TOKEN:
        logging.error("❌ BOT_TOKEN não definido.")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("winentrada", winentrada))
    app.add_handler(CommandHandler("wingale1", wingale1))
    app.add_handler(CommandHandler("wingale2", wingale2))
    app.add_handler(CallbackQueryHandler(button_handler))

    logging.info("🚀 Bot iniciado com sucesso.")
    app.run_polling()

if __name__ == "__main__":
    start_bot()
