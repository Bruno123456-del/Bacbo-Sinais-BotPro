# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 8.0 "MÁQUINA DE SINAIS"
# CRIADO E APRIMORADO POR MANUS
# FOCO EM SINAIS DE ALTÍSSIMA FREQUÊNCIA NO VIP PARA MÁXIMA CONVERSÃO
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, timedelta, datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# --- 1. CONFIGURAÇÕES E CREDENCIAIS ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "5011424031"))
FREE_CANAL_ID = int(os.getenv("CANAL_ID", "0").strip())
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "0").strip())

# --- Links do Funil (Confirmados e Integrados) ---
URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_INSTAGRAM = "https://www.instagram.com/apostasmilionariasvip/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
SUPORTE_TELEGRAM = "@seu_usuario_de_suporte" # IMPORTANTE: Coloque o @ do seu suporte

if not BOT_TOKEN or FREE_CANAL_ID == 0 or VIP_CANAL_ID == 0:
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN, CANAL_ID ou VIP_CANAL_ID não estão configurados!" )

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. MÍDIAS E CONTEÚDO VISUAL ---
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
PROVAS_SOCIAIS_URLS = [f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png" for i in range(1, 14 )]

# --- 3. MENSAGENS DE MARKETING E FUNIL ---
MARKETING_MESSAGES = {
    "boas_vindas_start": (
        f"💎 **QUER LUCRAR COM SINAIS DE ALTA ASSERTIVIDADE?** 💎\n\n"
        f"Você está no lugar certo! Nosso bot envia sinais gratuitos, mas o verdadeiro potencial está na nossa **Sala VIP Exclusiva**, com dezenas de sinais todos os dias!\n\n"
        f"**COMO FUNCIONA O ACESSO VIP?**\n\n"
        f"O acesso é **LIBERADO MEDIANTE DEPÓSITO** na plataforma parceira. Você não paga pelo acesso, apenas deposita para você mesmo jogar!\n\n"
        f"1️⃣ **CADASTRE-SE E DEPOSITE:**\n"
        f"Acesse o link, crie sua conta e faça um depósito.\n"
        f"➡️ [**CLIQUE AQUI PARA CADASTRAR E DEPOSITAR**]({URL_CADASTRO_DEPOSITO})\n\n"
        f"2️⃣ **ENVIE O COMPROVANTE:**\n"
        f"Mande o print para nosso suporte e receba seu link de acesso VIP na hora!\n"
        f"➡️ **Suporte:** {SUPORTE_TELEGRAM}\n\n"
        f"Acesse nosso Instagram: {URL_INSTAGRAM}\n"
        f"Ou entre no nosso canal grátis: {URL_TELEGRAM_FREE}"
    ),
    "acesso_liberado_vip": (
        "Olá! Comprovante recebido e verificado. Seja muito bem-vindo(a) à nossa Sala VIP! 🚀\n\n"
        "Aqui está o seu link de acesso exclusivo. Não compartilhe com ninguém!\n\n"
        "🔗 **Link VIP:** https://t.me/+q2CCKi1CKmljMTFh\n\n"
        "Prepare-se para uma chuva de sinais. Boas apostas!"
     ),
    "legendas_prova_social": [
        "🔥 **O GRUPO VIP ESTÁ PEGANDO FOGO!** 🔥\n\nMais um de nossos membros VIP lucrando. E você, vai ficar de fora?",
        "🚀 **RESULTADO DE MEMBRO VIP!** 🚀\n\nAnálises precisas, resultados reais. Parabéns pelo green!",
        "🤔 **AINDA NA DÚVIDA?** 🤔\n\nEnquanto você pensa, outros estão lucrando. O acesso VIP te coloca na frente.",
        "✅ **RESULTADOS FALAM MAIS QUE PALAVRAS!** ✅\n\nMais um green para a conta da família VIP. A consistência que você procura está aqui."
    ]
}

# --- 4. CONFIGURAÇÃO DOS JOGOS E APOSTAS ---
JOGOS = {
    "Bac Bo 🎲": ["Player", "Banker", "Tie (Empate)"],
    "Roleta 룰렛": ["Vermelho ⚫", "Preto 🔴", "Par", "Ímpar", "1ª Dúzia", "2ª Dúzia", "3ª Dúzia"],
    "Slots 🎰": ["Fortune Tiger - 5 Rodadas Turbo", "Fortune Rabbit - 7 Rodadas Normal", "Fortune Mouse - 10 Rodadas Turbo"],
    "Aviator ✈️": ["Buscar vela de 1.80x", "Buscar vela de 2.10x", "Duas entradas de 1.50x"],
    "Spaceman 👨‍🚀": ["Sair em 1.90x", "Sair em 2.20x", "Duas saídas em 1.60x"]
}

# --- 5. LÓGICA PRINCIPAL DO BOT ---

async def enviar_aviso_bloco(context: ContextTypes.DEFAULT_TYPE, jogo: str):
    """Envia uma mensagem de aquecimento 10 minutos antes de um bloco de sinais."""
    mensagem = f"🚨 **ATENÇÃO, JOGADORES VIP!** 🚨\n\nPreparem-se! Em 10 minutos iniciaremos nossa maratona de sinais para o jogo **{jogo}**. Fiquem atentos e com a plataforma aberta!"
    await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem)
    logger.info(f"Aviso de bloco para {jogo} enviado ao canal VIP.")

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target_id: int):
    """Envia um ciclo completo de sinal: análise, entrada e resultado."""
    bd = context.bot_data
    # Bloqueio para evitar sobreposição de sinais
    if bd.get(f"sinal_em_andamento_{target_id}", False):
        logger.warning(f"Pulei o sinal de {jogo} para o canal {target_id} pois outro já estava em andamento.")
        return
        
    bd[f"sinal_em_andamento_{target_id}"] = True
    
    try:
        # Etapa 1: Análise
        await context.bot.send_animation(chat_id=target_id, animation=GIF_ANALISANDO, caption=f"🔎 Analisando padrões para uma entrada em **{jogo}**...")
        await asyncio.sleep(random.randint(5, 10))

        # Etapa 2: Sinal
        mensagem_sinal = (f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
                          f"🎯 **Apostar em:** {aposta}\n"
                          f"🔗 **JOGAR NA PLATAFORMA CERTA:** [**CLIQUE AQUI**]({URL_CADASTRO_DEPOSITO})")
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP!_"
        await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal de {jogo} enviado para o canal {target_id}.")

        # Etapa 3: Resultado (simulado)
        await asyncio.sleep(random.randint(45, 75))
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=[70, 20, 10], k=1)[0]
        
        if resultado == "win_primeira":
            await context.bot.send_animation(chat_id=target_id, animation=GIF_GREEN_PRIMEIRA, caption="✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Parabéns a todos que confiaram! 🤑")
        elif resultado == "win_gale":
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE1, caption="✅ **GREEN NO GALE!** ✅\n\nPaciência e gestão trazem o lucro. Parabéns, time!")
        else:
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption="❌ **RED!** ❌\n\nFaz parte do jogo. Mantenham a gestão de banca e vamos para a próxima!")

    except Exception as e:
        logger.error(f"Erro no ciclo de sinal para {jogo} no canal {target_id}: {e}")
    finally:
        bd[f"sinal_em_andamento_{target_id}"] = False

async def enviar_prova_social(context: ContextTypes.DEFAULT_TYPE):
    """Envia uma prova social no canal gratuito."""
    url_prova = random.choice(PROVAS_SOCIAIS_URLS)
    legenda = random.choice(MARKETING_MESSAGES["legendas_prova_social"])
    await context.bot.send_photo(
        chat_id=FREE_CANAL_ID,
        photo=url_prova,
        caption=f"{legenda}\n\n[**QUERO LUCRAR ASSIM TAMBÉM!**]({URL_CADASTRO_DEPOSITO})",
        parse_mode='Markdown'
    )

# --- 6. COMANDOS DE USUÁRIO ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=MARKETING_MESSAGES["boas_vindas_start"], parse_mode='Markdown', disable_web_page_preview=False)

# --- 7. AGENDAMENTO DE TAREFAS DE ALTA FREQUÊNCIA ---
def agendar_tarefas(app: Application):
    jq = app.job_queue
    
    # --- AGENDAMENTO GRUPO FREE (2 SINAIS POR JOGO/DIA) ---
    logger.info("Agendando sinais para o Canal Gratuito...")
    free_schedule = {
        "Bac Bo 🎲": [time(10, 0), time(19, 0)],
        "Roleta 룰렛": [time(11, 0), time(20, 0)],
        "Slots 🎰": [time(12, 0), time(21, 0)],
        "Aviator ✈️": [time(14, 0), time(22, 0)],
        "Spaceman 👨‍🚀": [time(15, 0), time(23, 0)]
    }
    for jogo, horarios in free_schedule.items():
        for horario in horarios:
            aposta = random.choice(JOGOS[jogo])
            jq.run_daily(lambda ctx, j=jogo, a=aposta: asyncio.create_task(enviar_sinal_especifico(ctx, j, a, FREE_CANAL_ID)), time=horario)

    # --- AGENDAMENTO GRUPO VIP (MARATONA DE SINAIS) ---
    logger.info("Agendando maratona de sinais para o Canal VIP...")
    vip_blocks = {
        "Bac Bo 🎲": time(9, 0),
        "Roleta 룰렛": time(13, 0),
        "Slots 🎰": time(16, 0),
        "Aviator ✈️": time(19, 30),
        "Spaceman 👨‍🚀": time(22, 30)
    }
    for jogo, start_time in vip_blocks.items():
        # Agendar o aviso 10 minutos antes do bloco
        aviso_time = (datetime.combine(datetime.today(), start_time) - timedelta(minutes=10)).time()
        jq.run_daily(lambda ctx, j=jogo: asyncio.create_task(enviar_aviso_bloco(ctx, j)), time=aviso_time)
        
        # Agendar os 15 sinais com intervalo de 15 minutos
        for i in range(15):
            signal_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=15 * i)).time()
            aposta = random.choice(JOGOS[jogo])
            jq.run_daily(lambda ctx, j=jogo, a=aposta: asyncio.create_task(enviar_sinal_especifico(ctx, j, a, VIP_CANAL_ID)), time=signal_time)

    # --- AGENDAMENTO MARKETING (PROVAS SOCIAIS NO GRUPO FREE) ---
    logger.info("Agendando postagens de marketing e prova social...")
    for hour in [9, 12, 15, 18, 21]:
        jq.run_daily(enviar_prova_social, time=time(hour=hour, minute=45))

    logger.info("Todos os agendamentos (FREE, VIP e Marketing) foram concluídos com sucesso.")

# --- 8. FUNÇÃO PRINCIPAL (MAIN) ---
def main() -> None:
    logger.info("Iniciando o bot - Versão 8.0 'Máquina de Sinais'...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    agendar_tarefas(app)
    logger.info("Bot iniciado e pronto para operar em alta frequência.")
    app.run_polling()

if __name__ == "__main__":
    main()
