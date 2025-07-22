import os
import time
import threading
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Updater

# Carrega variáveis de ambiente
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# Lista de sinais simulados
sinais = [
    "🎲 SINAL BAC BO:\n🔁 Estratégia: Dupla Chance\n🕐 Entrada confirmada!",
    "🎲 SINAL BAC BO:\n🎯 Jogue no ALTO 🔺\n💰 Gestão: 2% da banca",
    "🎲 SINAL BAC BO:\n⚠️ Aposte no PARES\n📊 Probabilidade alta!",
    "🎲 SINAL BAC BO:\n🎯 Estratégia: G1 em ALTO 🔼",
    "🎲 BAC BO SINAL:\n🧠 Estatística indica BAIXO 🔻\n🚨 Gestão conservadora!"
]

# Envia sinais automaticamente a cada 10 minutos
def enviar_sinais_automaticos():
    index = 0
    while True:
        sinal = sinais[index % len(sinais)]
        bot.send_message(chat_id=CHAT_ID, text=sinal)
        index += 1
        time.sleep(600)

# Comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Bem-vindo ao canal de sinais BAC BO!")

# Função principal do bot
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    thread = threading.Thread(target=enviar_sinais_automaticos)
    thread.daemon = True
    thread.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
