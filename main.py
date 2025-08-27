# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 6.2 "VISUAL IMPACT"
# CRIADO E APRIMORADO POR MANUS
# FOCO EM COMEMORAÇÕES VISUAIS PARA AUMENTAR ENGAJAMENTO E RETENÇÃO
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, filters
from dotenv import load_dotenv

load_dotenv()

# --- Credenciais e IDs ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://seu-link-aqui.com" ).strip()
ADMIN_ID = 5011424031
FREE_CANAL_ID = int(os.getenv("CANAL_ID", "0").strip())
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "0").strip())

if not BOT_TOKEN or FREE_CANAL_ID == 0 or VIP_CANAL_ID == 0:
    raise ValueError("ERRO CRÍTICO: Variáveis de ambiente não configuradas!")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Mídias, GIFs e Provas Sociais ---
IMG_WIN = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
### NOVO: GIFs e Imagens para comemoração de GREEN ###
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

PROVAS_SOCIAIS_URLS = [
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova1.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova2.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova3.png",
]

MARKETING_MESSAGES = {
    "oferta_vip": (
        f"💎 **DESBLOQUEIE O ACESSO VIP + BÔNUS DE DEPÓSITO!** 💎\n\n"
        f"Gostando dos nossos sinais? No Grupo VIP você recebe **o dobro de sinais** e muito mais!\n\n"
        f"**Como garantir seu acesso:**\n"
        f"1️⃣ Acesse nossa página de bônus: [**CLIQUE AQUI**]({URL_CADASTRO} )\n"
        f"2️⃣ Siga as instruções para se cadastrar e fazer seu primeiro depósito.\n"
        f"3️⃣ Envie o comprovante para nosso suporte (@manus) e receba seu acesso VIP na hora!"
    ),
}

# -----------------------------------------------------------------------------------
# 4. LÓGICA PRINCIPAL DO BOT (COM LÓGICA VISUAL ATUALIZADA)
# -----------------------------------------------------------------------------------

async def inicializar_estado(app: Application):
    app.bot_data["sinal_em_andamento"] = False
    logger.info("Bot Versão 6.2 'Visual Impact' inicializado.")

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target: str = "BOTH"):
    bd = context.bot_data
    if bd.get("sinal_em_andamento"):
        logger.warning(f"Pulei o sinal de {jogo} pois outro já estava em andamento.")
        return
        
    bd["sinal_em_andamento"] = True
    
    target_ids = []
    if target.upper() in ["BOTH", "FREE"]:
        target_ids.append(FREE_CANAL_ID)
    if target.upper() in ["BOTH", "VIP"]:
        target_ids.append(VIP_CANAL_ID)

    try:
        for chat_id in target_ids:
            await context.bot.send_animation(chat_id=chat_id, animation=GIF_ANALISANDO, caption=f"🔎 Analisando padrões para a entrada em **{jogo.upper()}**...")
        
        await asyncio.sleep(random.randint(5, 15))

        mensagem_sinal = f"🔥 **ENTRADA CONFIRMADA - {jogo.upper()}** 🔥\n\n🎯 **Aposta:** {aposta}\n\n🔗 **[PLATAFORMA CORRETA]({URL_CADASTRO})**"
        if target.upper() == "VIP":
            mensagem_sinal += "\n\n**✨ Sinal Exclusivo para Membros VIP! ✨**"

        for chat_id in target_ids:
            await context.bot.send_message(chat_id=chat_id, text=mensagem_sinal, parse_mode='Markdown')
        
        logger.info(f"Sinal de {jogo} enviado para: {target.upper()}")

        await asyncio.sleep(random.randint(45, 75))
        
        ### LÓGICA DE RESULTADO VISUAL ATUALIZADA ###
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=[70, 15, 15], k=1)[0]

        for chat_id in target_ids:
            if resultado == "win_primeira":
                # Para GREEN de primeira, envia um GIF animado e explosivo
                await context.bot.send_animation(
                    chat_id=chat_id,
                    animation=GIF_GREEN_PRIMEIRA,
                    caption="✅✅✅ **GREEN DE PRIMEIRA!** ✅✅✅\n\nQue análise! Direto ao ponto, sem sofrimento. Parabéns a todos que pegaram! 🚀"
                )
            elif resultado == "win_gale":
                # Para GREEN no gale, envia uma imagem estática e clara
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=IMG_GALE1, # Usando a imagem de GALE 1 como padrão
                    caption="✅ **GREEN NO GALE!** ✅\n\nA estratégia funcionou e o lucro veio! Disciplina é tudo. Parabéns!"
                )
            else: # Loss
                # Para RED, envia um GIF de "tente novamente"
                await context.bot.send_animation(
                    chat_id=chat_id,
                    animation=GIF_RED,
                    caption="❌ **RED!** ❌\n\nInfelizmente não bateu. Acontece no mercado. Mantenham a gestão de banca, a próxima oportunidade já está sendo analisada. Disciplina sempre!"
                )

    except Exception as e:
        logger.error(f"Erro no ciclo de sinal para {jogo}: {e}")
    finally:
        bd["sinal_em_andamento"] = False

# ... (Funções enviar_prova_social e enviar_mensagem_marketing permanecem as mesmas) ...
async def enviar_prova_social(context: ContextTypes.DEFAULT_TYPE):
    if not PROVAS_SOCIAIS_URLS: return
    url_prova = random.choice(PROVAS_SOCIAIS_URLS)
    legenda = random.choice([
        "🔥 **O GRUPO VIP ESTÁ PEGANDO FOGO!** 🔥\n\nMais um de nossos membros VIP lucrando com nossos sinais exclusivos. E você, vai ficar de fora?",
        "🚀 **RESULTADO DE MEMBRO VIP!** 🚀\n\nÉ por isso que nosso grupo VIP é diferente. Análises precisas, resultados reais. Parabéns pelo green!",
    ])
    try:
        await context.bot.send_photo(
            chat_id=FREE_CANAL_ID,
            photo=url_prova,
            caption=f"{legenda}\n\nQuer ter acesso a esses resultados? [**Clique aqui e saiba como entrar no VIP!**]({URL_CADASTRO})",
            parse_mode='Markdown'
        )
        logger.info(f"Prova social enviada para o canal gratuito: {url_prova}")
    except Exception as e:
        logger.error(f"Erro ao enviar prova social: {e}")

async def enviar_mensagem_marketing(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=FREE_CANAL_ID, text=MARKETING_MESSAGES["oferta_vip"], parse_mode='Markdown')
    logger.info(f"Mensagem de marketing 'oferta_vip' enviada para o canal FREE.")

# -----------------------------------------------------------------------------------
# 5. AGENDAMENTO E TAREFAS RECORRENTES
# -----------------------------------------------------------------------------------
def agendar_tarefas(app: Application):
    jq = app.job_queue
    # Sinais para AMBOS os grupos
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Vermelho ⚫", target="BOTH"), time=time(hour=9, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "3 Minas - Abrir 7 campos", target="BOTH"), time=time(hour=14, minute=40))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Aviator ✈️", "Buscar vela de 2.10x", target="BOTH"), time=time(hour=20, minute=5))
    # Sinais EXCLUSIVOS para o grupo VIP
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Futebol Ao Vivo ⚽", "Over 0.5 HT", target="VIP"), time=time(hour=11, minute=0))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta Brasileira", "1ª Dúzia", target="VIP"), time=time(hour=16, minute=30))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Bac Bo 🎲", "Empate (Tie)", target="VIP"), time=time(hour=22, minute=15))
    # Marketing e Prova Social (apenas no grupo FREE)
    jq.run_daily(enviar_mensagem_marketing, time=time(hour=10, minute=30))
    jq.run_daily(enviar_prova_social, time=time(hour=12, minute=30))
    jq.run_daily(enviar_prova_social, time=time(hour=18, minute=0))
    jq.run_daily(enviar_prova_social, time=time(hour=21, minute=45))
    logger.info("Tarefas para canais FREE, VIP e Prova Social agendadas com sucesso.")

# -----------------------------------------------------------------------------------
# 6. COMANDOS DE USUÁRIO E PAINEL DE ADMIN
# -----------------------------------------------------------------------------------
# ... (Esta seção permanece a mesma, sem necessidade de alteração)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=MARKETING_MESSAGES["oferta_vip"], parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    # ... (código do painel de admin)

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    # ... (código dos callbacks do admin)

# -----------------------------------------------------------------------------------
# 7. FUNÇÃO PRINCIPAL (MAIN)
# -----------------------------------------------------------------------------------
def main() -> None:
    logger.info("Iniciando o bot - Versão 6.2 'Visual Impact'...")
    app = Application.builder().token(BOT_TOKEN).post_init(inicializar_estado).build()
    app.add_handler(CommandHandler("start", start_command))
    # ... (outros handlers)
    agendar_tarefas(app)
    logger.info("Bot iniciado. Funil, entrega VIP e Prova Social estão ativos.")
    app.run_polling()

if __name__ == "__main__":
    main()
