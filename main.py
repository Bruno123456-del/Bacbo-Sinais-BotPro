import logging
import os
import random
from datetime import datetime
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))

# Habilitar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Contadores de win e loss
diario_win = 0
diario_loss = 0

# Caminhos das imagens
IMG_WIN = "imagens/win-futurista.gif"
IMG_LOSS = "imagens/loss-futurista.gif"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(f"Olá {user.mention_html()}! Seja bem-vindo ao canal de sinais Bac Bo!")

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start para começar. Em breve mais comandos estarão disponíveis.")

# Função para enviar sinal com imagem de resultado
definir_resultado():
    return random.choice(["win", "loss"])

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    global diario_win, diario_loss
    resultado = definir_resultado()

    mensagem = f"🎲 Novo Sinal Bac Bo 🎲\n\n🎯 Estratégia: Escada Asiática\n🎰 Entrada: Jogar agora\n💡 Resultado: {resultado.upper()}"

    if resultado == "win":
        diario_win += 1
        imagem = IMG_WIN
    else:
        diario_loss += 1
        imagem = IMG_LOSS

    try:
        await context.bot.send_photo(chat_id=CANAL_ID, photo=open(imagem, "rb"), caption=mensagem)
    except Exception as e:
        logging.error(f"Erro ao enviar sinal: {e}")

# Resumo diário
async def resumo_diario(context: ContextTypes.DEFAULT_TYPE):
    global diario_win, diario_loss

    resumo = (
        f"📊 RESUMO DO DIA 📊\n\n"
        f"✅ Greens: {diario_win}\n❌ Reds: {diario_loss}\n\n"
        f"🚀 Continue com a gente e multiplique sua banca!"
    )
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo)
    diario_win = 0
    diario_loss = 0

# Main
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Sinais a cada 10 minutos
    application.job_queue.run_repeating(enviar_sinal, interval=600, first=5)

    # Resumo diário às 23:59
    application.job_queue.run_daily(resumo_diario, time=datetime.strptime("23:59", "%H:%M").time())

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
