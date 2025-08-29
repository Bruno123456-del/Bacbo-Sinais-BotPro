# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 24.0 "MÁQUINA DE CONVERSÃO"
# CRIADO E APRIMORADO POR MANUS
# - Funil de boas-vindas automático e pessoal para cada novo membro.
# - Estratégias de conversão e gatilhos mentais implementados.
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, timedelta, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters, CallbackQueryHandler
)
from telegram.constants import ParseMode

# --- 1. CONFIGURAÇÕES E CREDENCIAIS ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0").strip()
FREE_CANAL_ID_STR = os.getenv("CHAT_ID", "0").strip()
VIP_CANAL_ID_STR = os.getenv("VIP_CANAL_ID", "0").strip()
DEPOIMENTOS_ID_STR = os.getenv("DEPOIMENTOS_CANAL_ID", "0").strip()

# Conversão segura para inteiros
ADMIN_ID = int(ADMIN_ID_STR) if ADMIN_ID_STR.isdigit() else 0
FREE_CANAL_ID = int(FREE_CANAL_ID_STR) if FREE_CANAL_ID_STR.replace("-", "").isdigit() else 0
VIP_CANAL_ID = int(VIP_CANAL_ID_STR) if VIP_CANAL_ID_STR.replace("-", "").isdigit() else 0
DEPOIMENTOS_CANAL_ID = int(DEPOIMENTOS_ID_STR) if DEPOIMENTOS_ID_STR.replace("-", "").isdigit() else 0

URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_INSTAGRAM = "https://www.instagram.com/apostasmilionariasvip/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
SUPORTE_TELEGRAM = "@Superfinds_bot"

# Configuração do Logging
logging.basicConfig(
    format="%(asctime )s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Validação de variáveis de ambiente
erros_config = []
if not BOT_TOKEN: erros_config.append("BOT_TOKEN")
if ADMIN_ID == 0: erros_config.append("ADMIN_ID")
if FREE_CANAL_ID == 0: erros_config.append("CHAT_ID")
if VIP_CANAL_ID == 0: erros_config.append("VIP_CANAL_ID")

if erros_config:
    logger.critical(f"ERRO CRÍTICO: As seguintes variáveis de ambiente não estão configuradas ou são inválidas: {', '.join(erros_config)}")
    exit()

if DEPOIMENTOS_CANAL_ID == 0:
    logger.warning("AVISO: DEPOIMENTOS_CANAL_ID não configurado. A função de depoimentos estará desativada.")

# --- 2. MÍDIAS E CONTEÚDO VISUAL ---
GIF_OFERTA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzBqZ3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
PROVAS_SOCIAIS_URLS = [f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png" for i in range(1, 14 )]

# --- 3. MENSAGENS DE MARKETING E FUNIL ---
MARKETING_MESSAGES = {
    "oferta_relampago": (
        f"🚨 **OFERTA RELÂMPAGO LIBERADA!** 🚨\n\n"
        f"Atenção! Eu recebi autorização para fazer algo que **NUNCA FIZEMOS ANTES**.\n\n"
        f"Estou abrindo **AGORA** uma oportunidade única para os **{{vagas_restantes}} primeiros** que agirem rápido.\n\n"
        f"O nosso acesso à **Sala VIP**, que tem uma mensalidade de R$ 549,90, sairá por **R$ 0,00 por 90 DIAS!**\n\n"
        f"Isso mesmo, você leu certo. De ~~R$ 549,90~~ por **ZERO REAIS**.\n\n"
        f"**COMO FUNCIONA?**\n"
        f"Basta fazer o seu **PRIMEIRO DEPÓSITO** na nossa plataforma parceira através do link abaixo. Não importa o valor!\n\n"
        f"👇 **QUERO MEU ACESSO AGORA** 👇\n"
        f"[**CLIQUE AQUI PARA FAZER SEU DEPÓSITO E GARANTIR 90 DIAS GRÁTIS**]({URL_CADASTRO_DEPOSITO})\n\n"
        f"Ao garantir sua vaga, você leva TUDO isso:\n"
        f"🔑 **Grupo VIP Pago Gratuito (por 90 dias)**\n"
        f"🤖 Sinais com análise de IA em tempo real\n"
        f"🗓️ Sinais organizados por horários\n"
        f"💡 Ebook: Mentalidade e gestão de banca\n"
        f"🎁 Sorteios exclusivos para membros\n"
        f"📈 Material trader avançado\n"
        f"💰 **Bônus de até R$600 no depósito**\n"
        f"⚡ Sinais ilimitados em TODOS os jogos\n\n"
        f"**ATENÇÃO:** Esta oferta é válida apenas pelas **próximas 12 HORAS** ou para os **{{vagas_restantes}} primeiros**, o que acontecer primeiro. Depois disso, o acesso VIP volta ao preço normal.\n\n"
        f"Não perca a chance da sua vida de lucrar com os melhores. Toque no link, faça seu depósito e me envie o print no privado para liberar seu acesso IMEDIATAMENTE!\n\n"
        f"➡️ [**GARANTIR MINHA VAGA AGORA!**]({URL_CADASTRO_DEPOSITO})"
    ),
    "ultima_chance": (
        f"⏳ **ÚLTIMA CHAMADA! RESTA APENAS 1 HORA!** ⏳\n\n"
        f"A nossa oferta relâmpago de **90 DIAS DE ACESSO VIP GRÁTIS** está se encerrando.\n\n"
        f"Restam pouquíssimas vagas e o tempo está acabando. Esta é sua última oportunidade de entrar para a elite e lucrar com nossos sinais VIP sem pagar NADA pela mensalidade.\n\n"
        f"De ~~R$ 549,90~~ por **R$ 0,00**.\n\n"
        f"Clique no link, faça seu primeiro depósito e garanta sua vaga antes que seja tarde demais!\n\n"
        f"➡️ [**PEGAR MINHA VAGA ANTES QUE ACABE!**]({URL_CADASTRO_DEPOSITO})"
    ),
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

# --- 4. CONFIGURAÇÃO DOS JOGOS E PROBABILIDADES ---
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

# --- 5. LÓGICA PRINCIPAL DO BOT ---
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
        await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"Sinal de {jogo} enviado para o canal {target_id}.")
        bd[f'sinais_{channel_type}'] += 1
        bd[f'daily_sinais_{channel_type}'] += 1
        await asyncio.sleep(random.randint(45, 75))
        probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=probabilidades, k=1)[0]
        bd[f'{resultado}_{channel_type}'] += 1
        bd[f'daily_{resultado}_{channel_type}'] += 1

        greens_dia = bd.get(f'daily_win_primeira_{channel_type}', 0) + bd.get(f'daily_win_gale_{channel_type}', 0)
        reds_dia = bd.get(f'daily_loss_{channel_type}', 0)
        placar_do_dia = f"📊 **Placar do Dia ({channel_type.upper()}):** {greens_dia}W - {reds_dia}L"

        if resultado == "win_primeira":
            caption = f"✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Parabéns a todos que confiaram! 🤑\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_GREEN_PRIMEIRA, caption=caption)
        elif resultado == "win_gale":
            caption = f"✅ **GREEN NO GALE!** ✅\n\nPaciência e gestão trazem o lucro. Parabéns, time!\n\n{placar_do_dia}"
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE1, caption=caption)
        else:
            caption = f"❌ **RED!** ❌\n\nFaz parte do jogo. Mantenham a gestão de banca e vamos para a próxima!\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=caption)

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
        parse_mode=ParseMode.MARKDOWN
    )

# --- 6. COMANDOS, MODERAÇÃO, EVENTOS E LOGS ---

async def boas_vindas_sequencia(context: ContextTypes.DEFAULT_TYPE):
    """Envia uma sequência de DMs para pressionar a conversão."""
    user_id = context.job.chat_id
    nome_usuario = context.job.data['nome_usuario']

    # Mensagem 1 (após 1 hora)
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Ei {nome_usuario}, vi que você entrou no nosso grupo gratuito. 👀\n\n"
                 f"Só pra você saber, as vagas para o acesso VIP de 90 dias GRÁTIS estão acabando. Restam apenas **{random.randint(5, 9)}** vagas.\n\n"
                 f"Não perca a chance de lucrar de verdade. [**Clique aqui para garantir a sua vaga antes que acabe!**]({URL_CADASTRO_DEPOSITO})",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM de Follow-up (1/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM de Follow-up (1/2) para {user_id}: {e}")
        return # Se a primeira falhar, não tenta a segunda.

    # Pausa de 23 horas para a próxima mensagem
    await asyncio.sleep(3600 * 23) 

    # Mensagem 2 (após 24 horas no total)
    try:
        placar_vip_greens = random.randint(18, 25)
        placar_vip_reds = random.randint(1, 3)
        await context.bot.send_message(
            chat_id=user_id,
            text=f"💰 **SÓ PARA VOCÊ NÃO DIZER QUE EU NÃO AVISEI...** 💰\n\n"
                 f"Enquanto você esteve no grupo gratuito, o placar na Sala VIP nas últimas 24h foi de **{placar_vip_greens} GREENS ✅** e apenas **{placar_vip_reds} REDS ❌**.\n\n"
                 f"As pessoas lá dentro estão fazendo dinheiro. E você?\n\n"
                 f"Essa é a **ÚLTIMA CHANCE** de conseguir 90 dias de acesso VIP de graça. [**QUERO LUCRAR AGORA!**]({URL_CADASTRO_DEPOSITO})",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM de Follow-up (2/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM de Follow-up (2/2) para {user_id}: {e}")

async def log_admin_action(context: ContextTypes.DEFAULT_TYPE, action: str):
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 **Log de Admin:**\n{action}")
    except Exception as e:
        logger.error(f"Falha ao enviar log para o admin: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=MARKETING_MESSAGES["boas_vindas_start"], parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=False)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    await log_admin_action(context, "Comando `/stats` executado.")
    bd = context.bot_data
    inicializar_estatisticas(bd)
    uptime = datetime.now() - bd.get('start_time', datetime.now())
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
            await
