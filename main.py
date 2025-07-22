import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_BONUS = os.getenv("URL_BONUS", "https://seusite.com/bonus" ) # URL padrão

# Lista de sinais
sinais = [
    "🎲 SINAL BAC BO: Estratégia Dupla Chance 🔁. Entrada confirmada!",
    "🎲 SINAL BAC BO: Jogue no ALTO 🔺. Gestão: 2% da banca.",
    "🎲 SINAL BAC BO: Aposte no PARES ⚠️. Probabilidade alta!",
    "🎲 SINAL BAC BO: Estratégia G1 em ALTO 🔼.",
    "🎲 SINAL BAC BO: Estatística indica BAIXO 🔻. Gestão conservadora!"
]

# Envia sinais automaticamente
async def enviar_sinais(bot: Bot):
    index = 0
    while True:
        sinal = sinais[index % len(sinais)]
        try:
            await bot.send_message(chat_id=CHAT_ID, text=sinal)
            print(f"Sinal enviado para o chat {CHAT_ID}")
        except Exception as e:
            print(f"Erro ao enviar sinal: {e}")
        
        index += 1
        await asyncio.sleep(600) # Pausa de 10 minutos

# Comando /bonus com botão
async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "Clique no botão abaixo para pegar seu bônus exclusivo! 🎁"
    botao = InlineKeyboardButton(text="Pegar Bônus Agora!", url=URL_BONUS)
    teclado = InlineKeyboardMarkup([[botao]])
    await update.message.reply_text(text=texto, reply_markup=teclado)

# Função principal
async def main():
    print("Iniciando o bot...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("bonus", bonus))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em execução.")

    asyncio.create_task(enviar_sinais(application.bot))
    print(f"Envio de sinais para o chat {CHAT_ID} agendado.")

    # Mantém o script rodando
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
