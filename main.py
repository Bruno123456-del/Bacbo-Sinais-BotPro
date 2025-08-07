# -*- coding: utf-8 -*-

import os
import random
import asyncio
from datetime import datetime, time as dt_time
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import TelegramError
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

# Frases e imagens automáticas
frases_win = [
    "✅ WIN confirmado! Seguimos lucrando com inteligência. 💸",
    "🔥 Mais um GREEN na conta! Confia no processo.",
    "💰 Lucro garantido! Estratégia asiática é insana.",
]

frases_empate = [
    "🟨 Empate! Seguimos firmes na próxima entrada.",
    "🟨 Deu cobertura! Vamos pra cima na próxima.",
    "🟨 Resultado: empate! A gestão salva vidas.",
]

frases_agradecimento = [
    "Mano, fechei R$260 só hoje! Tmj 🔥🔥🔥",
    "Gratidão pelos sinais, irmão! Nunca ganhei tanto assim 🙌",
    "Esse canal é surreal... Obrigado de verdade! 💰",
]

def horario_ativo():
    agora = datetime.now().time()
    return (dt_time(13, 0) <= agora <= dt_time(17, 0)) or (dt_time(19, 0) <= agora <= dt_time(22, 0))

def gerar_sinal():
    opcoes = ["⚪ Branco", "🔴 Vermelho", "🔵 Azul"]
    entrada = random.choice(opcoes)
    gale1 = random.choice(opcoes)
    gale2 = random.choice(opcoes)
    sinal = f"""
🎯 NOVO SINAL BAC BO IGNITE

🎰 Entrada Principal: {entrada}
🔁 Gale 1: {gale1}
🔁 Gale 2: {gale2}
🟨 Cobertura: Amarelo (Empate)

🎯 Estratégia: Escada Asiática com Gestão
⏰ Validade: 1 minuto após o envio

{gerar_botoes()}
"""
    return sinal

def gerar_botoes():
    botoes = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Jogar Bac Bo", url="https://lkwn.cc/f1c1c45a")],
        [InlineKeyboardButton("📈 Gestão de Banca", url="https://t.me/+exemplo")],
    ])
    return botoes

async def enviar_mensagem(texto, imagem=None):
    try:
        if imagem:
            with open(imagem, 'rb') as img:
                await bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=texto, reply_markup=gerar_botoes())
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=texto, reply_markup=gerar_botoes())
    except TelegramError as e:
        print(f"Erro ao enviar mensagem: {e}")

async def rotina_sinais():
    while True:
        if horario_ativo():
            sinal = gerar_sinal()
            await enviar_mensagem(sinal)
            await asyncio.sleep(60)

            imagem_win = "imagens/win.png"
            frase_win = random.choice(frases_win)
            await enviar_mensagem(frase_win, imagem_win)
            await asyncio.sleep(60)

            imagem_empate = "imagens/empate.png"
            frase_empate = random.choice(frases_empate)
            await enviar_mensagem(frase_empate, imagem_empate)
            await asyncio.sleep(60)

            imagem_agradecimento = "imagens/agradecimento.png"
            frase_agradecimento = random.choice(frases_agradecimento)
            await enviar_mensagem(frase_agradecimento, imagem_agradecimento)
            await asyncio.sleep(600)
        else:
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(rotina_sinais())
