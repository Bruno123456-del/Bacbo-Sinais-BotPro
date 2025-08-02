# main.py
import logging
import os
import random
import datetime
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Configurações iniciais
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7975008855:AAHZ8F0XUfRtRX643Z3B3DoOA3h5YLVnRDs"
CANAL_ID = int(os.getenv("CANAL_ID") or -1002808626127)

# Diretório das imagens
IMG_WIN = "imagens/win-futurista.gif"
IMG_LOSS = "imagens/loss-futurista.gif"

# Contadores globais
ganhos = 0
perdas = 0

# Configura logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de exemplos de sinais (fictícios)
sinais = [
    {"jogo": "BAC BO", "palpite": "Escada Asiática", "resultado": "win"},
    {"jogo": "BAC BO", "palpite": "Cobertura Amarela", "resultado": "loss"},
    {"jogo": "BAC BO", "palpite": "Dupla Chance", "resultado": "win"},
]

# Enviar sinal com imagem
async def enviar_sinal(application):
    global ganhos, perdas
    sinal = random.choice(sinais)
    texto = (
        f"🎯 PALPITE DO DIA 🎯\n"
        f"🎮 Jogo: {sinal['jogo']}\n"
        f"💡 Estratégia: {sinal['palpite']}\n"
        f"📊 Resultado: {'✅ GREEN' if sinal['resultado'] == 'win' else '❌ RED'}\n\n"
        f"🔗 Jogar agora: https://lkwn.cc/f1c1c45a"
    )

    imagem = IMG_WIN if sinal['resultado'] == 'win' else IMG_LOSS
    if sinal['resultado'] == 'win':
        ganhos += 1
    else:
        perdas += 1

    try:
        await application.bot.send_photo(chat_id=CANAL_ID, photo=open(imagem, 'rb'), caption=texto)
    except Exception as e:
        logger.error(f"Erro ao enviar sinal: {e}")

# Resumo do dia
async def resumo_diario(application):
    texto = (
        f"📊 RESUMO DO DIA 📊\n"
        f"✅ GREENS: {ganhos}\n"
        f"❌ REDS: {perdas}\n"
        f"🏆 Assertividade: {round((ganhos / (ganhos + perdas)) * 100, 1) if ganhos + perdas > 0 else 0}%\n\n"
        f"🎯 Continue acompanhando nossos palpites exclusivos aqui no canal!"
    )
    await application.bot.send_message(chat_id=CANAL_ID, text=texto)

# Comando de teste manual
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot ativo! Enviaremos os sinais automáticos para o canal!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start para iniciar. Os sinais serão enviados automaticamente.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Enviar sinais a cada 10 minutos e resumo a cada dia (simples para Render)
    async def tarefa_sinais():
        while True:
            await enviar_sinal(application)
            await asyncio.sleep(600)  # 10 minutos

    async def tarefa_resumo():
        while True:
            now = datetime.datetime.now()
            if now.hour == 23 and now.minute == 59:
                await resumo_diario(application)
                await asyncio.sleep(60)
            await asyncio.sleep(30)

    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(tarefa_sinais())
    loop.create_task(tarefa_resumo())

    application.run_polling()

if __name__ == "__main__":
    main()
