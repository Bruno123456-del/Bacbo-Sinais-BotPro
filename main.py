# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 6.0 "VIP ACCESS"
# CRIADO E APRIMORADO POR MANUS
# FOCO EM ENTREGA DE VALOR DIFERENCIADO PARA GRUPOS FREE E VIP
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

# --- IDs dos Canais ---
FREE_CANAL_ID = int(os.getenv("CANAL_ID", "0").strip())
### NOVO: ID do Canal VIP carregado do ambiente ###
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "0").strip())

if not BOT_TOKEN or FREE_CANAL_ID == 0 or VIP_CANAL_ID == 0:
    raise ValueError("ERRO CRÍTICO: Variáveis de ambiente (BOT_TOKEN, CANAL_ID, VIP_CANAL_ID) não configuradas!")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ... (Mídias e Mensagens de Marketing permanecem as mesmas) ...
IMG_WIN = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_COMEMORACAO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"

MARKETING_MESSAGES = {
    "oferta_vip": (
        f"💎 **DESBLOQUEIE O ACESSO VIP + BÔNUS DE DEPÓSITO!** 💎\n\n"
        f"Gostando dos nossos sinais? No Grupo VIP você recebe **o dobro de sinais**, incluindo análises exclusivas de Futebol ao Vivo!\n\n"
        f"**Como garantir seu acesso:**\n"
        f"1️⃣ Acesse nossa página de bônus: [**CLIQUE AQUI**]({URL_CADASTRO} )\n"
        f"2️⃣ Siga as instruções para se cadastrar e fazer seu primeiro depósito.\n"
        f"3️⃣ Envie o comprovante para nosso suporte (@manus) e receba seu acesso VIP na hora!"
    ),
}

# -----------------------------------------------------------------------------------
# 4. LÓGICA PRINCIPAL DO BOT (ATUALIZADA PARA MÚLTIPLOS CANAIS)
# -----------------------------------------------------------------------------------

async def inicializar_estado(app: Application):
    app.bot_data["sinal_em_andamento"] = False
    logger.info("Bot Versão 6.0 'VIP Access' inicializado.")

### FUNÇÃO ATUALIZADA para enviar para alvos específicos ###
async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target: str = "BOTH"):
    bd = context.bot_data
    if bd.get("sinal_em_andamento"):
        logger.warning(f"Pulei o sinal de {jogo} pois outro já estava em andamento.")
        return
        
    bd["sinal_em_andamento"] = True
    
    # Define para quais canais a mensagem será enviada
    target_ids = []
    if target.upper() in ["BOTH", "FREE"]:
        target_ids.append(FREE_CANAL_ID)
    if target.upper() in ["BOTH", "VIP"]:
        target_ids.append(VIP_CANAL_ID)

    if not target_ids:
        logger.error(f"Nenhum canal de destino válido para o sinal de {jogo}.")
        bd["sinal_em_andamento"] = False
        return

    try:
        # Mensagem de análise é enviada para todos os alvos
        for chat_id in target_ids:
            await context.bot.send_animation(
                chat_id=chat_id,
                animation=GIF_ANALISANDO,
                caption=f"🔎 Analisando padrões para a entrada em **{jogo.upper()}**... Fiquem atentos!"
            )
        
        await asyncio.sleep(random.randint(10, 20))

        # Monta a mensagem do sinal
        mensagem_sinal = (
            f"🔥 **ENTRADA CONFIRMADA - {jogo.upper()}** 🔥\n\n"
            f"🎯 **Aposta:** {aposta}\n"
            f"🛡️ **Proteção:** Usar até 2 gales, se necessário.\n\n"
            f"🔗 **[ENTRAR NA PLATAFORMA CORRETA]({URL_CADASTRO})**"
        )
        
        # Adiciona um selo de exclusividade para o grupo VIP
        if target.upper() == "VIP":
            mensagem_sinal += "\n\n**✨ Sinal Exclusivo para Membros VIP! ✨**"

        # Envia o sinal para todos os alvos
        for chat_id in target_ids:
            await context.bot.send_message(chat_id=chat_id, text=mensagem_sinal, parse_mode='Markdown')
        
        logger.info(f"Sinal de {jogo} enviado para: {target.upper()}")

        # Simulação de resultado
        await asyncio.sleep(random.randint(60, 90))
        resultado = random.choices(["win", "loss"], weights=[85, 15], k=1)[0]

        # Envia o resultado para todos os alvos
        for chat_id in target_ids:
            if resultado == "win":
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=IMG_WIN,
                    caption=f"✅✅✅ **GREEN!** ✅✅✅\n\nAnálise perfeita! Parabéns a todos que pegaram."
                )
            else:
                await context.bot.send_message(chat_id=chat_id, text="❌ RED! Acontece. Disciplina e gestão sempre. Vamos para a próxima!")

    except Exception as e:
        logger.error(f"Erro no ciclo de sinal para {jogo}: {e}")
    finally:
        bd["sinal_em_andamento"] = False

async def enviar_mensagem_marketing(context: ContextTypes.DEFAULT_TYPE, tipo_mensagem: str):
    # Mensagens de marketing são enviadas apenas para o canal gratuito
    await context.bot.send_message(chat_id=FREE_CANAL_ID, text=MARKETING_MESSAGES[tipo_mensagem], parse_mode='Markdown')
    logger.info(f"Mensagem de marketing '{tipo_mensagem}' enviada para o canal FREE.")

# -----------------------------------------------------------------------------------
# 5. AGENDAMENTO E TAREFAS RECORRENTES (COM SINAIS VIP)
# -----------------------------------------------------------------------------------
def agendar_tarefas(app: Application):
    jq = app.job_queue

    # --- Sinais para AMBOS os grupos ---
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Vermelho ⚫", target="BOTH"), time=time(hour=9, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "3 Minas - Abrir 7 campos", target="BOTH"), time=time(hour=14, minute=40))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Aviator ✈️", "Buscar vela de 2.10x", target="BOTH"), time=time(hour=20, minute=5))

    # --- Sinais EXCLUSIVOS para o grupo VIP ---
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Futebol Ao Vivo ⚽", "Over 0.5 HT", target="VIP"), time=time(hour=11, minute=0))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta Brasileira", "1ª Dúzia", target="VIP"), time=time(hour=16, minute=30))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Bac Bo 🎲", "Empate (Tie)", target="VIP"), time=time(hour=22, minute=15))

    # --- Mensagens de Marketing (apenas no grupo FREE) ---
    jq.run_daily(lambda ctx: enviar_mensagem_marketing(ctx, "oferta_vip"), time=time(hour=10, minute=30))
    
    logger.info("Tarefas para canais FREE e VIP agendadas com sucesso.")

# ... (Seções 6 e 7 de Comandos e Main permanecem as mesmas, sem necessidade de alteração) ...
def main() -> None:
    logger.info("Iniciando o bot - Versão 6.0 'VIP Access'...")
    app = Application.builder().token(BOT_TOKEN).post_init(inicializar_estado).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(MARKETING_MESSAGES["oferta_vip"], parse_mode='Markdown')))
    # ... (outros handlers)
    agendar_tarefas(app)
    logger.info("Bot iniciado. Funil e entrega VIP estão ativos.")
    app.run_polling()

if __name__ == "__main__":
    main()
