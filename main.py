# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 14.0 "BOT CONVERSACIONAL"
# CRIADO E APRIMORADO POR MANUS
# - BOTÕES NA MENSAGEM DE BOAS-VINDAS
# - LOG PRIVADO DE ATIVIDADES DO ADMIN
# - RESPOSTAS AUTOMÁTICAS A PALAVRAS-CHAVE
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, timedelta, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PersistenceInput, PicklePersistence, 
    ChatMemberHandler, MessageHandler, filters
)

# --- 1. CONFIGURAÇÕES E CREDENCIAIS (sem alterações) ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "5011424031"))
FREE_CANAL_ID = int(os.getenv("CHAT_ID", "0").strip()) 
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "0").strip())

URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_INSTAGRAM = "https://www.instagram.com/apostasmilionariasvip/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
SUPORTE_TELEGRAM = "@Superfinds_bot" 

if not BOT_TOKEN or FREE_CANAL_ID == 0 or VIP_CANAL_ID == 0:
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN, CHAT_ID ou VIP_CANAL_ID não estão configurados!"  )

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. MÍDIAS E CONTEÚDO VISUAL (sem alterações) ---
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
PROVAS_SOCIAIS_URLS = [f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png" for i in range(1, 14  )]

# --- 3. MENSAGENS DE MARKETING E FUNIL (sem alterações) ---
MARKETING_MESSAGES = {
    "divulgacao": (
        f"🤖 **Cansado de perder dinheiro? Conheça nosso Robô de Sinais 100% GRATUITO!** 🤖\n\n"
        f"Nossa inteligência artificial analisa o mercado 24/7 e envia sinais de alta assertividade para jogos como Roleta, Aviator, Mines, Slots e muito mais!\n\n"
        f"✅ **Sinais Gratuitos Todos os Dias**\n✅ **Análises Precisas e em Tempo Real**\n✅ **Comunidade com Milhares de Membros Lucrando**\n\n"
        f"Chega de contar com a sorte. Comece a lucrar com estratégia!\n\n"
        f"👇 **ENTRE AGORA NO NOSSO CANAL GRATUITO E COMECE A LUCRAR HOJE MESMO!** 👇\n"
        f"🔗 {URL_TELEGRAM_FREE}\n🔗 {URL_TELEGRAM_FREE}\n"
    ),
    "boas_vindas_start": (
        f"💎 **QUER LUCRAR COM SINAIS DE ALTA ASSERTIVIDADE?** 💎\n\n"
        f"Você está no lugar certo! Meu nome é Super Finds, e meu trabalho é te ajudar a lucrar.\n\n"
        f"No nosso canal gratuito você recebe algumas amostras, mas o verdadeiro potencial está na **Sala VIP Exclusiva**, com dezenas de sinais todos os dias!\n\n"
        f"**COMO FUNCIONA O ACESSO VIP?**\n\n"
        f"O acesso é **LIBERADO MEDIANTE DEPÓSITO** na plataforma parceira.\n\n"
        f"1️⃣ **CADASTRE-SE E DEPOSITE:**\n"
        f"Acesse o link, crie sua conta e faça um depósito.\n"
        f"➡️ [**CLIQUE AQUI PARA CADASTRAR E DEPOSITAR**]({URL_CADASTRO_DEPOSITO})\n\n"
        f"2️⃣ **ENVIE O COMPROVANTE:**\n"
        f"Mande o print do seu depósito **aqui mesmo, nesta conversa,** e receba seu link de acesso VIP na hora!\n"
        f"➡️ **É só anexar a imagem e enviar para mim!**\n\n"
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

# --- 4. CONFIGURAÇÃO DOS JOGOS E PROBABILIDADES (sem alterações) ---
ASSERTIVIDADE_JOGOS = {
    "Bac Bo 🎲": [70, 20, 10], "Roleta 룰렛": [68, 22, 10], "Slots 🎰": [60, 25, 15],
    "Aviator ✈️": [75, 15, 10], "Spaceman 👨‍🚀": [75, 15, 10], "Mines 💣": [65, 20, 15],
    "Penalty Shoot-Out ⚽️": [72, 18, 10], "Fortune Dragon 🐲": [62, 23, 15], "Dragon Tiger 🐉🐅": [70, 20, 10],
    "default": [70, 20, 10]
}
JOGOS = {
    "Bac Bo 🎲": ["Player", "Banker", "Tie (Empate)"],
    "Roleta 룰렛": ["Vermelho ⚫", "Preto 🔴", "Par", "Ímpar", "1ª Dúzia", "2ª Dúzia", "3ª Dúzia"],
    "Slots 🎰": ["Fortune Tiger - 5 Rodadas Turbo", "Fortune Rabbit - 7 Rodadas Normal", "Fortune Mouse - 10 Rodadas Turbo"],
    "Aviator ✈️": ["Buscar vela de 1.80x", "Buscar vela de 2.10x", "Duas entradas de 1.50x"],
    "Spaceman 👨‍🚀": ["Sair em 1.90x", "Sair em 2.20x", "Duas saídas em 1.60x"],
    "Mines 💣": ["3 minas - Tentar 4 rodadas", "5 minas - Tentar 2 rodadas"],
    "Penalty Shoot-Out ⚽️": ["Apostar no Gol", "Apostar na Defesa"],
    "Fortune Dragon 🐲": ["8 Rodadas Turbo", "10 Rodadas Normal"],
    "Dragon Tiger 🐉🐅": ["Dragon", "Tiger", "Tie (Empate)"]
}
JOGOS_MAP = {key.split(" ")[0].lower(): key for key in JOGOS.keys()}

# --- 5. LÓGICA PRINCIPAL DO BOT (sem alterações) ---
async def enviar_aviso_bloco(context: ContextTypes.DEFAULT_TYPE, jogo: str, tipo: str):
    if tipo == "inicio":
        mensagem = f"🚨 **ATENÇÃO, JOGADORES VIP!** 🚨\n\nPreparem-se! Em 10 minutos iniciaremos nossa maratona de sinais para o jogo **{jogo}**. Fiquem atentos e com a plataforma aberta!"
    elif tipo == "ultimo":
        mensagem = f"⏳ **ÚLTIMO SINAL DO BLOCO!** ⏳\n\nVamos para a última entrada da nossa maratona de **{jogo}**. Foco total para fechar com chave de ouro!"
    else: # encerramento
        mensagem = f"🏁 **BLOCO DE SINAIS ENCERRADO** 🏁\n\nFinalizamos nossa maratona de **{jogo}**. Esperamos que tenham lucrado! Fiquem atentos para os próximos blocos de sinais ao longo do dia."
    await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem)
    logger.info(f"Aviso de '{tipo}' para {jogo} enviado ao canal VIP.")

def inicializar_estatisticas(bot_data):
    if 'start_time' not in bot_data:
        bot_data['start_time'] = datetime.now()
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            if f'{stat}_{ch}' not in bot_data: bot_data[f'{stat}_{ch}'] = 0
            if f'daily_{stat}_{ch}' not in bot_data: bot_data[f'daily_{stat}_{ch}'] = 0

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target_id: int):
    bd = context.bot_data
    channel_type = 'vip' if target_id == VIP_CANAL_ID else 'free'
    if bd.get(f"sinal_em_andamento_{target_id}", False):
        logger.warning(f"Pulei o sinal de {jogo} para o canal {target_id} pois outro já estava em andamento.")
        return
    bd[f"sinal_em_andamento_{target_id}"] = True
    try:
        await context.bot.send_animation(chat_id=target_id, animation=GIF_ANALISANDO, caption=f"🔎 Analisando padrões para uma entrada em **{jogo}**...")
        await asyncio.sleep(random.randint(5, 10))
        mensagem_sinal = (f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
                          f"🎯 **Apostar em:** {aposta}\n"
                          f"🔗 **JOGAR NA PLATAFORMA CERTA:** [**CLIQUE AQUI**]({URL_CADASTRO_DEPOSITO})")
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP!_"
        await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal de {jogo} enviado para o canal {target_id}.")
        bd[f'sinais_{channel_type}'] += 1
        bd[f'daily_sinais_{channel_type}'] += 1
        await asyncio.sleep(random.randint(45, 75))
        probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=probabilidades, k=1)[0]
        bd[f'{resultado}_{channel_type}'] += 1
        bd[f'daily_{resultado}_{channel_type}'] += 1
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
    url_prova = random.choice(PROVAS_SOCIAIS_URLS)
    legenda = random.choice(MARKETING_MESSAGES["legendas_prova_social"])
    await context.bot.send_photo(
        chat_id=FREE_CANAL_ID,
        photo=url_prova,
        caption=f"{legenda}\n\n[**QUERO LUCRAR ASSIM TAMBÉM!**]({URL_CADASTRO_DEPOSITO})",
        parse_mode='Markdown'
    )

# --- 6. COMANDOS, MODERAÇÃO, EVENTOS E LOGS ---

# ★★★ NOVA FUNCIONALIDADE: LOG DE ADMIN ★★★
async def log_admin_action(context: ContextTypes.DEFAULT_TYPE, action: str):
    """Envia uma notificação de log para o chat privado do admin."""
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 **Log de Admin:**\n{action}")
    except Exception as e:
        logger.error(f"Falha ao enviar log para o admin: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=MARKETING_MESSAGES["boas_vindas_start"], parse_mode='Markdown', disable_web_page_preview=False)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    await log_admin_action(context, "Comando `/stats` executado.")
    bd = context.bot_data
    inicializar_estatisticas(bd)
    uptime = datetime.now() - bd['start_time']
    days, rem = divmod(uptime.total_seconds(), 86400); hours, rem = divmod(rem, 3600); minutes, _ = divmod(rem, 60)
    stats_text = (
        f"📊 **PAINEL DE ESTATÍSTICAS GERAIS** 📊\n\n"
        f"🕒 **Tempo Ativo:** {int(days)}d, {int(hours)}h, {int(minutes)}m\n\n"
        f"--- **Canal Gratuito (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_free', 0)} | ✅: {bd.get('win_primeira_free', 0)} | ☑️: {bd.get('win_gale_free', 0)} | ❌: {bd.get('loss_free', 0)}\n\n"
        f"--- **Canal VIP (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_vip', 0)} | ✅: {bd.get('win_primeira_vip', 0)} | ☑️: {bd.get('win_gale_vip', 0)} | ❌: {bd.get('loss_vip', 0)}\n"
    )
    await update.message.reply_text(stats_text)

async def manual_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    try:
        _, jogo_curto, canal = context.args
        jogo_completo = JOGOS_MAP.get(jogo_curto.lower())
        if not jogo_completo:
            await update.message.reply_text(f"❌ Jogo '{jogo_curto}' não encontrado. Use um dos: {', '.join(JOGOS_MAP.keys())}")
            return
        target_id = VIP_CANAL_ID if canal.lower() == 'vip' else FREE_CANAL_ID
        aposta = random.choice(JOGOS[jogo_completo])
        context.job_queue.run_once(lambda ctx: asyncio.create_task(enviar_sinal_especifico(ctx, jogo_completo, aposta, target_id)), 0)
        log_message = f"Comando `/sinal {jogo_curto} {canal}` executado. Sinal de '{jogo_completo}' enviado para o canal {canal.upper()}."
        await log_admin_action(context, log_message)
        await update.message.reply_text("✅ Sinal manual enviado com sucesso.")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ **Uso incorreto!**\nUse: `/sinal <jogo> <canal>`\nExemplo: `/sinal mines vip`")

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    try:
        user_to_ban = context.args[0]
        if not user_to_ban.startswith('@'):
            await update.message.reply_text("⚠️ Formato inválido. Use o @username do usuário. Ex: `/ban @username`")
            return
        
        log_message = f"Comando `/ban {user_to_ban}` executado.\n"
        banned_in_any = False
        for chat_id in [FREE_CANAL_ID, VIP_CANAL_ID]:
            try:
                await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_to_ban)
                log_message += f"  - ✅ Banido com sucesso do canal {chat_id}.\n"
                banned_in_any = True
            except Exception as e:
                log_message += f"  - ❌ Falha ao banir do canal {chat_id}: {e}\n"
        
        await log_admin_action(context, log_message)
        if banned_in_any:
            await update.message.reply_text(f"✅ Tentativa de banimento de {user_to_ban} concluída. Veja o log para detalhes.")
        else:
            await update.message.reply_text(f"❌ Não foi possível banir {user_to_ban} de nenhum canal. Verifique o log.")

    except IndexError:
        await update.message.reply_text("⚠️ **Uso incorreto!**\nUse: `/ban @username`")

async def divulgar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    try:
        target_chat_id = context.args[0]
        mensagem = MARKETING_MESSAGES["divulgacao"]
        await context.bot.send_message(chat_id=target_chat_id, text=mensagem, disable_web_page_preview=False)
        log_message = f"Comando `/divulgar` executado. Mensagem enviada para o chat ID: {target_chat_id}."
        await log_admin_action(context, log_message)
        await update.message.reply_text(f"✅ Mensagem de divulgação enviada com sucesso!")
    except IndexError:
        await update.message.reply_text("⚠️ **Uso incorreto!**\nUse: `/divulgar <ID do chat de destino>`")
    except Exception as e:
        await update.message.reply_text(f"❌ **Erro ao enviar mensagem:**\n`{e}`")

# ★★★ ATUALIZAÇÃO: BOAS-VINDAS COM BOTÕES ★★★
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = update.chat_member
    if result.new_chat_member.status == 'member' and result.old_chat_member.status != 'member':
        novo_membro = result.new_chat_member.user
        chat_id = result.chat.id
        
        if chat_id == FREE_CANAL_ID:
            mensagem = f"👋 Seja bem-vindo(a), {novo_membro.first_name}!\n\nVocê está no lugar certo para começar a lucrar. Fique de olho nos sinais gratuitos e explore nossos links úteis abaixo!"
            keyboard = [
                [InlineKeyboardButton("💎 QUERO ACESSO VIP 💎", url=f"https://t.me/{SUPORTE_TELEGRAM.lstrip('@' )}")],
                [InlineKeyboardButton("📸 NOSSO INSTAGRAM", url=URL_INSTAGRAM)],
            ]
        elif chat_id == VIP_CANAL_ID:
            mensagem = f"🚀 Bem-vindo(a) à elite, {novo_membro.first_name}!\n\nVocê está na Sala VIP. Fique com a plataforma aberta e prepare-se para a nossa maratona de sinais!"
            keyboard = [
                [InlineKeyboardButton("💰 ACESSAR PLATAFORMA 💰", url=URL_CADASTRO_DEPOSITO)],
            ]
        else: return

        reply_markup = InlineKeyboardMarkup(keyboard)
        msg_enviada = await context.bot.send_message(chat_id=chat_id, text=mensagem, reply_markup=reply_markup)
        
        # Apaga a mensagem após 5 minutos para não poluir o canal
        context.job_queue.run_once(lambda ctx: ctx.bot.delete_message(chat_id=chat_id, message_id=msg_enviada.message_id), 300)
        logger.info(f"Mensagem de boas-vindas com botões enviada para {novo_membro.first_name}.")

# ★★★ NOVA FUNCIONALIDADE: RESPOSTA A PALAVRAS-CHAVE ★★★
async def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Ignora mensagens do admin para não se auto-responder
    if update.effective_user.id == ADMIN_ID: return
    
    text = update.message.text.lower()
    keywords = ["vip", "acesso", "funciona", "comprar", "como entra"]
    
    if any(keyword in text for keyword in keywords):
        user_mention = update.effective_user.mention_html()
        reply_text = (
            f"Olá, {user_mention}! Vi que você tem interesse no acesso VIP. Para saber como funciona e liberar seu acesso, "
            f"por favor, inicie uma conversa com nosso bot de suporte.\n\n"
            f"➡️ **Clique aqui para falar com o suporte:** @{SUPORTE_TELEGRAM.lstrip('@')}"
        )
        # Envia a resposta mencionando o usuário
        await update.message.reply_text(reply_text, parse_mode='HTML')
        logger.info(f"Resposta automática enviada para {update.effective_user.first_name} sobre acesso VIP.")

# --- 7. AGENDAMENTO DE TAREFAS (sem alterações) ---
async def postar_placar_diario(context: ContextTypes.DEFAULT_TYPE):
    bd = context.bot_data
    for ch_type, ch_id in [('free', FREE_CANAL_ID), ('vip', VIP_CANAL_ID)]:
        total_sinais = bd.get(f'daily_sinais_{ch_type}', 0)
        if total_sinais == 0: continue
        greens = bd.get(f'daily_win_primeira_{ch_type}', 0) + bd.get(f'daily_win_gale_{ch_type}', 0)
        reds = bd.get(f'daily_loss_{ch_type}', 0)
        assertividade = (greens / total_sinais * 100) if total_sinais > 0 else 0
        placar_msg = (
            f"🏁 **PLACAR DO DIA - CANAL {'VIP' if ch_type == 'vip' else 'GRATUITO'}** 🏁\n\n"
            f"Fechamos o dia com os seguintes resultados:\n\n"
            f"✅ **Greens:** {greens}\n"
            f"❌ **Reds:** {reds}\n"
            f"--------------------\n"
            f"🎯 **Assertividade:** {assertividade:.2f}%\n\n"
            f"Amanhã tem mais! Mantenham a gestão e vamos com tudo! 💪"
        )
        await context.bot.send_message(chat_id=ch_id, text=placar_msg)
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bd[f'daily_{stat}_{ch_type}'] = 0
    logger.info("Placar diário postado e contadores zerados.")

def agendar_tarefas(app: Application):
    jq = app.job_queue
    logger.info("Agendando sinais para o Canal Gratuito...")
    free_schedule = {
        "Bac Bo 🎲": [time(10)], "Roleta 룰렛": [time(11)], "Slots 🎰": [time(12)], "Aviator ✈️": [time(14)], 
        "Spaceman 👨‍🚀": [time(15)], "Mines 💣": [time(18)], "Penalty Shoot-Out ⚽️": [time(20)], 
        "Fortune Dragon 🐲": [time(21)], "Dragon Tiger 🐉🐅": [time(22)]
    }
    for jogo, horarios in free_schedule.items():
        for horario in horarios:
            horario_dinamico = horario.replace(minute=random.randint(0, 9))
            aposta = random.choice(JOGOS[jogo])
            jq.run_daily(lambda ctx, j=jogo, a=aposta: asyncio.create_task(enviar_sinal_especifico(ctx, j, a, FREE_CANAL_ID)), time=horario_dinamico)
    
    horario_surpresa = time(hour=random.randint(16, 17), minute=random.randint(0, 59))
    jq.run_daily(lambda ctx: asyncio.create_task(enviar_sinal_especifico(ctx, "Bac Bo 🎲", random.choice(JOGOS["Bac Bo 🎲"]), FREE_CANAL_ID)), time=horario_surpresa)
    
    logger.info("Agendando maratona de sinais para o Canal VIP...")
    vip_blocks = {
        "Bac Bo 🎲": time(9, 0), "Roleta 룰렛": time(10, 30), "Mines 💣": time(12, 0), "Slots 🎰": time(13, 30),
        "Penalty Shoot-Out ⚽️": time(15, 0), "Aviator ✈️": time(16, 30), "Fortune Dragon 🐲": time(18, 0),
        "Spaceman 👨‍🚀": time(20, 0), "Dragon Tiger 🐉🐅": time(22, 0)
    }
    num_sinais_bloco = 5
    for jogo, start_time in vip_blocks.items():
        aviso_inicio_time = (datetime.combine(datetime.today(), start_time) - timedelta(minutes=10)).time()
        jq.run_daily(lambda ctx, j=jogo: asyncio.create_task(enviar_aviso_bloco(ctx, j, "inicio")), time=aviso_inicio_time)
        for i in range(num_sinais_bloco):
            signal_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=10 * i)).time()
            aposta = random.choice(JOGOS[jogo])
            if i == num_sinais_bloco - 1:
                aviso_ultimo_time = (datetime.combine(datetime.today(), signal_time) - timedelta(minutes=1)).time()
                jq.run_daily(lambda ctx, j=jogo: asyncio.create_task(enviar_aviso_bloco(ctx, j, "ultimo")), time=aviso_ultimo_time)
            jq.run_daily(lambda ctx, j=jogo, a=aposta: asyncio.create_task(enviar_sinal_especifico(ctx, j, a, VIP_CANAL_ID)), time=signal_time)
        encerramento_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=10 * num_sinais_bloco + 2)).time()
        jq.run_daily(lambda ctx, j=jogo: asyncio.create_task(enviar_aviso_bloco(ctx, j, "encerramento")), time=encerramento_time)

    logger.info("Agendando postagens de marketing...")
    for hour in [9, 12, 15, 18, 21]:
        jq.run_daily(enviar_prova_social, time=time(hour=hour, minute=random.randint(40, 55)))
    
    jq.run_daily(postar_placar_diario, time=time(hour=23, minute=55))
    logger.info("Placar diário agendado para as 23:55.")
    
    logger.info("Todos os agendamentos foram concluídos com sucesso.")

# --- 8. FUNÇÃO PRINCIPAL (MAIN) ---
def main() -> None:
    logger.info("Iniciando o bot Super Finds - Versão 14.0 'Bot Conversacional'...")
    
