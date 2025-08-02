import logging
import os
import random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
BOT_TOKEN = "7975008855:AAGEc1_htKryQnZ0qPemvoWs0Mz3PG22Q3U"
CANAL_ID = -1002808626127  # Substitua se necessário

# Ativa logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Caminhos das imagens
IMG_WIN = "imagens/win-futurista.gif"
IMG_LOSS = "imagens/loss-futurista.gif"

# Contadores
diario_win = 0
diario_loss = 0

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Olá {user.mention_html()}! Seja bem-vindo ao canal de sinais Bac Bo!"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start para começar. Em breve mais comandos estarão disponíveis.")

# Resultado aleatório
def definir_resultado():
    return random.choice(["win", "loss"])

# Enviar sinal
async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    global diario_win, diario_loss
    resultado = definir_resultado()

    mensagem = (
        f"🎲 Novo Sinal Bac Bo 🎲\n\n"
        f"🎯 Estratégia: Escada Asiática\n"
        f"🎰 Entrada: Jogar agora\n"
        f"💡 Resultado: {resultado.upper()}"
    )

    imagem = IMG_WIN if resultado == "win" else IMG_LOSS
    if resultado == "win":
        diario_win += 1
    else:
        diario_loss += 1

    try:
        with open(imagem, "rb") as img:
            await context.bot.send_photo(chat_id=CANAL_ID, photo=img, caption=mensagem)
    except Exception as e:
        logging.error(f"Erro ao enviar imagem: {e}")

# Enviar resumo do dia
async def resumo_diario(context: ContextTypes.DEFAULT_TYPE):
    global diario_win, diario_loss
    resumo = (
        f"📊 RESUMO DO DIA 📊\n\n"
        f"✅ Greens: {diario_win}\n"
        f"❌ Reds: {diario_loss}\n\n"
        f"🚀 Continue com a gente e multiplique sua banca!"
    )
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo)
    diario_win = 0
    diario_loss = 0

# Main
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.job_queue.run_repeating(enviar_sinal, interval=600, first=5)
    application.job_queue.run_daily(resumo_diario, time=datetime.strptime("23:59", "%H:%M").time())

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
