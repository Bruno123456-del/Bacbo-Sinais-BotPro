# -*- coding: utf-8 -*-

import logging
import os
import random
import asyncio
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÃO INICIAL ---

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CANAL_ID = os.getenv("CANAL_ID", "0").strip()
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a" )

if not BOT_TOKEN or CANAL_ID == "0":
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN ou CANAL_ID não foram encontrados no arquivo .env.")

CANAL_ID = int(CANAL_ID)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 2. BANCO DE MÍDIA E MENSAGENS DE MARKETING ---

IMG_WIN_ENTRADA = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
IMG_WIN_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
IMG_WIN_GALE2 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale2.png"
IMG_WIN_EMPATE = "https://raw.githubusercontent.com/Bruno123456‑del/Bacbo‑Sinais‑BotPro/main/imagens/win_empate.png"

GIFS_COMEMORACAO = [
    # URLs originais mantidas...
]

GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5…/giphy.gif"
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5…/giphy.giphy.gif"

MENSAGEM_POS_WIN = f"""
🚀 **QUER RESULTADOS ASSIM?** 🚀

Nossos sinais são calibrados para a **1WIN**. Jogar em outra plataforma pode gerar resultados diferentes.

👉 [**Clique aqui para se cadastrar na 1WIN**]({URL_CADASTRO}) e tenha acesso a:
✅ **Bônus Premium** de boas‑vindas
🏆 **Sorteios Milionários** e até carros de luxo!

Não fique de fora! **Cadastre‑se agora!**
"""

# --- 3. ESTADO DO BOT (Contadores) ---

async def inicializar_contadores(application: Application):
    application.bot_data.setdefault("diario_win", 0)
    application.bot_data.setdefault("diario_loss", 0)
    logger.info(f"Contadores inicializados: {application.bot_data}")

# --- 4. COMANDOS DO USUÁRIO (Para chat privado) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # seu código original de boas-vindas...
    pass

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # seu código original de help...
    pass

# --- 5. LÓGICA PRINCIPAL DOS SINAIS (CORRIGIDA) ---

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    # seu bloco original inalterado...
    pass

async def resumo_diario(context: ContextTypes.DEFAULT_TYPE):
    # seu bloco original de resumo diário inalterado...
    pass

# --- 6. FUNÇÃO ADICIONADA: envio de prova social automática ---

import random as _rand_module
from PIL import Image
from telegram.ext import ContextTypes as _CTX

async def enviar_prova_social(context: _CTX.DEFAULT_TYPE):
    imagens = []
    PASTA = os.path.join(os.path.dirname(__file__), "imagens")
    for f in os.listdir(PASTA):
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(PASTA, f)
            try:
                Image.open(path)
                imagens.append(path)
            except:
                continue
    if not imagens:
        logger.warning("Nenhuma imagem encontrada para prova social.")
        return
    escolha = _rand_module.choice(imagens)
    caption = f"💬 Novo feedback de aluno!\n🔗 Seja parte: {URL_CADASTRO}"
    try:
        with open(escolha, "rb") as imgf:
            await context.bot.send_photo(chat_id=CANAL_ID, photo=imgf, caption=caption)
            logger.info(f"Prova social enviada: {escolha}")
    except Exception as e:
        logger.error(f"Falha ao enviar prova social: {e}")

# --- 7. FUNÇÃO PRINCIPAL QUE INICIA TUDO ---

def main():
    logger.info("Iniciando o bot...")
    application = Application.builder().token(BOT_TOKEN).post_init(inicializar_contadores).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.job_queue.run_repeating(enviar_sinal, interval=random.randint(900, 1500), first=10)
    application.job_queue.run_daily(resumo_diario, time=time(hour=22, minute=0))

    # agendar provas sociais 3x por dia:
    application.job_queue.run_daily(enviar_prova_social, time=time(hour=10, minute=0))
    application.job_queue.run_daily(enviar_prova_social, time=time(hour=15, minute=0))
    application.job_queue.run_daily(enviar_prova_social, time=time(hour=20, minute=0))

    application.run_polling()

if __name__ == "__main__":
    main()
