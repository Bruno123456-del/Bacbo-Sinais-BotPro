import os
import random
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from flask import Flask
from threading import Thread

# =============== CONFIG ===============
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Ex: '-1001234567890'
URL_CADASTRO = "https://lkwn.cc/f1c1c45a"
PASTA_IMAGENS = "imagens"

bot = Bot(token=TOKEN)
app = Flask(__name__)
# ======================================

# Estratégia "Escada Asiática com Cobertura"
sinais = [
    ("Player", "Banco", "Amarelo"),
    ("Banco", "Player", "Amarelo"),
    ("Player", "Player", "Amarelo"),
    ("Banco", "Banco", "Amarelo"),
]

estatisticas = {
    "wins": 0,
    "gale1": 0,
    "gale2": 0,
    "perdas": 0,
    "total": 0,
}


def gerar_mensagem_sinal(entrada, gale1, cobertura):
    return f"""🚨 NOVO SINAL GERADO 🚨

🎯 Entrada: {entrada}
🔥 Gale 1: {gale1}
🛡️ Cobertura (empate): {cobertura}

🎯 Valor da entrada: R$20,00
🛡️ Valor da cobertura: R$5,00
💰 Banca recomendada: R$1000+

🔁 Use até 2 Gales (Progressão Inteligente)
📊 Gestão: 1 a 2% por entrada + Cobertura

🎮 Clique aqui para jogar: 👉 {URL_CADASTRO}"""

def gerar_botao():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Jogar Bac Bo Agora", url=URL_CADASTRO)]
    ])

def escolher_imagem_win():
    opcoes = [
        "win_entrada.png",
        "win_gale1.png",
        "win_gale2.png"
    ]
    escolhida = random.choice(opcoes)
    if "gale1" in escolhida:
        estatisticas["gale1"] += 1
    elif "gale2" in escolhida:
        estatisticas["gale2"] += 1
    else:
        estatisticas["wins"] += 1
    estatisticas["total"] += 1
    return os.path.join(PASTA_IMAGENS, escolhida)

async def enviar_sinal():
    entrada, gale1, cobertura = random.choice(sinais)
    mensagem = gerar_mensagem_sinal(entrada, gale1, cobertura)
    imagem = escolher_imagem_win()

    await bot.send_photo(
        chat_id=CHAT_ID,
        photo=open(imagem, "rb"),
        caption=mensagem,
        reply_markup=gerar_botao()
    )

async def enviar_gestao():
    texto = f"""
📊 *Gestão Inteligente de Banca* 📊

💵 Banca ideal: *R$1000 ou mais*
🎯 Entrada: *R$20 (2% da banca)*
🛡️ Cobertura: *R$5 a R$10 (empate = amarelo)*

🔁 Use Gale 1 e Gale 2 com sabedoria
⚠️ Nunca aposte mais que 5% da sua banca!

🎮 Cadastre-se e aproveite os bônus agora:
👉 {URL_CADASTRO}
"""
    await bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown")

async def enviar_mensagem_motivacional():
    frases = [
        "🔥 Cada vitória te aproxima da liberdade financeira!",
        "💰 Quem aposta com inteligência, lucra no longo prazo.",
        "🎯 A consistência vence a sorte.",
        "📈 Disciplina e gestão são as chaves do sucesso!"
    ]
    frase = random.choice(frases)
    await bot.send_message(chat_id=CHAT_ID, text=frase)

async def enviar_estatisticas():
    msg = f"""📊 *Estatísticas do Dia* 📊

✅ Win direto: {estatisticas["wins"]}
🌀 Gale 1: {estatisticas["gale1"]}
🔥 Gale 2: {estatisticas["gale2"]}
❌ Perdas: {estatisticas["perdas"]}
🎯 Total de sinais: {estatisticas["total"]}

🔗 {URL_CADASTRO}
"""
    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

async def rotina_diaria():
    while True:
        agora = datetime.now()
        proxima_execucao = agora.replace(hour=20, minute=0, second=0, microsecond=0)
        if agora > proxima_execucao:
            proxima_execucao += timedelta(days=1)
        espera = (proxima_execucao - agora).total_seconds()
        await asyncio.sleep(espera)

        await enviar_sinal()
        await enviar_gestao()
        await enviar_mensagem_motivacional()
        await enviar_estatisticas()

@app.route('/')
def home():
    return '✅ Bot Bac Bo Online - Estratégia Escada Asiática'

def iniciar_flask():
    app.run(host='0.0.0.0', port=3000)

def iniciar_asyncio():
    asyncio.run(rotina_diaria())

# ========= INICIAR =========
if __name__ == "__main__":
    Thread(target=iniciar_flask).start()
    Thread(target=iniciar_asyncio).start()
