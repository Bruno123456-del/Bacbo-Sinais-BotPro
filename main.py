# -*- coding: utf-8 -*-

import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest
from telegram.constants import ChatAction

# --- 1. CONFIGURAÇÃO INICIAL ---
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# --- 2. BANCO DE DADOS DE EXEMPLO ---
cores = ["🔴 Vermelho", "⚫ Preto"]
casas = ["🐲 Dragão", "🐯 Tigre"]

# --- 3. FUNÇÃO PRINCIPAL DE ENVIO DE SINAL ---
async def simular_e_enviar_sinal(bot: Bot):
    try:
        await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.TYPING)
        cor = random.choice(cores)
        casa = random.choice(casas)
        mensagem = f"🎯 NOVO SINAL GERADO!

🎨 Cor: {cor}
🏠 Casa: {casa}

⏳ Validade: 3 minutos
⚙️ Estratégia: Entrada + 2 Gales"
        await bot.send_message(chat_id=CHAT_ID, text=mensagem)
        print("✅ Sinal enviado com sucesso.")

        # Envia resultado simulado após o sinal
        await asyncio.sleep(5)
        resultado = random.choice(["win_entrada", "win_gale1", "win_gale2"])

        if resultado == "win_entrada":
            await bot.send_message(chat_id=CHAT_ID, text="✅ GREEN na ENTRADA! 💸")
        elif resultado == "win_gale1":
            await bot.send_message(chat_id=CHAT_ID, text="✅ GREEN no GALE 1! 🤑")
        else:
            await bot.send_message(chat_id=CHAT_ID, text="✅ GREEN no GALE 2! 🔥")

        # Enviar imagem correspondente ao resultado
        mapa_resultado_imagem = {
            "win_entrada": "imagens/win_entrada.png",
            "win_gale1": "imagens/win_gale1.png",
            "win_gale2": "imagens/win_gale2.png"
        }

        imagem = mapa_resultado_imagem.get(resultado)
        if imagem:
            legenda = random.choice([
                "📸 Comprovado! Resultado da nossa última entrada!",
                "💰 Prova social: WIN confirmado agora mesmo.",
                "🔥 Lucro real capturado e printado!"
            ])
            await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem, 'rb'), caption=legenda)
            print("✅ Print enviado com sucesso.")

    except Exception as e:
        print(f"Erro ao enviar sinal ou print: {e}")

# --- 4. COMANDOS DO BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot de sinais BAC BO iniciado!")

async def estrategia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Estratégia utilizada: Entrada + 2 Gales. Foco em gestão e consistência!")

async def suporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💬 Suporte: Fale com @seuusuario ou envie um e-mail para suporte@dominio.com")

# --- 5. AGENDAMENTO DE SINAIS ---
async def agendar_sinais(app: Application, bot: Bot):
    while True:
        await simular_e_enviar_sinal(bot)
        await asyncio.sleep(600)  # A cada 10 minutos

# --- 6. MAIN ---
def main():
    app = Application.builder().token(TOKEN).build()
    bot = Bot(token=TOKEN)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("estrategia", estrategia))
    app.add_handler(CommandHandler("suporte", suporte))

    loop = asyncio.get_event_loop()
    loop.create_task(agendar_sinais(app, bot))

    print("🚀 Bot rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()
