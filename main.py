import os
import random
import logging
from telegram import Bot, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image

# === CARREGAR VARIÁVEIS DE AMBIENTE ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = os.getenv("CANAL_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO")

# === CONFIGURAR LOG ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === FRASES E MENSAGENS ===
ENTRADA = "🔔 ENTRADA CONFIRMADA"
GALE1 = "🔁 ENTRADA CONFIRMADA - GALE 1"
GALE2 = "🔁 ENTRADA CONFIRMADA - GALE 2"
GREEN = "✅ GREEN!"
RED = "❌ RED"
AVISO = "🚨 Atenção para a nova entrada!"
MENSAGEM_FIXA = f"Clique aqui para se cadastrar gratuitamente e receber sinais:
{URL_CADASTRO}"
MENSAGEM_POS_WIN = "🔥 Mais um green para conta!"

# === PASTA DAS PROVAS SOCIAIS ===
PASTA_IMAGENS_SOCIAIS = os.path.join(os.path.dirname(__file__), "imagens")

def carregar_provas_sociais():
    imagens = []
    for arquivo in os.listdir(PASTA_IMAGENS_SOCIAIS):
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
            caminho = os.path.join(PASTA_IMAGENS_SOCIAIS, arquivo)
            imagens.append(caminho)
    return imagens

def escolher_prova_social():
    imagens = carregar_provas_sociais()
    if imagens:
        return random.choice(imagens)
    return None

async def enviar_prova_social(context, chat_id):
    imagem_path = escolher_prova_social()
    if imagem_path:
        with open(imagem_path, "rb") as f:
            await context.bot.send_photo(chat_id=chat_id, photo=InputFile(f), caption="📸 Veja nossos resultados reais! Comemore conosco os greens do dia!")

# === FUNÇÕES DOS SINAIS ===
async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    tipo = random.choice([ENTRADA, GALE1, GALE2])
    await context.bot.send_message(chat_id=CANAL_ID, text=f"{AVISO}\n{tipo}")
    await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_FIXA)

    # Simula resultado do sinal (green ou red)
    resultado = random.choice([GREEN, RED])
    await context.bot.send_message(chat_id=CANAL_ID, text=resultado)

    if resultado == GREEN:
        await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN)
        await enviar_prova_social(context, CANAL_ID)

# === COMANDO MANUAL ===
async def start(update, context):
    await update.message.reply_text("🤖 Bot de sinais iniciado com sucesso!")

# === AGENDADOR ===
scheduler = BackgroundScheduler()
scheduler.add_job(enviar_sinal, 'cron', hour='9,15,21', minute=0, second=0, args=[None])
scheduler.start()

# === INICIAR BOT ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.job_queue.run_repeating(enviar_sinal, interval=3600, first=10)  # envia de hora em hora
    print("🤖 Bot está rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()
