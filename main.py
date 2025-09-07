# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 24.2 "MÁQUINA DE CONVERSÃO" (CORRIGIDO E ROBUSTO)
# CRIADO E APRIMORADO POR MANUS
# - Funil de boas-vindas automático e pessoal para cada novo membro.
# - Estratégias de conversão e gatilhos mentais implementados.
# - Correção do erro: string não terminada na sequência de DMs (nome_usuario).
# - Tratamento de exceções, logs e inicialização de estatísticas.
# - Healthcheck Flask opcional para Render.
# ===================================================================================

import os
import logging
import random
import asyncio
import threading
from datetime import time as dt_time, timedelta, datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters, CallbackQueryHandler
)

# --- 0. HEALTHCHECK FLASK (opcional, ajuda no Render) ---
try:
    from flask import Flask
    from flask_cors import CORS
    _FLASK_AVAILABLE = True
except Exception:
    _FLASK_AVAILABLE = False

def start_flask():
    if not _FLASK_AVAILABLE:
        return
    app = Flask(__name__)
    CORS(app)

    @app.get("/")
    def root():
        return {"status": "ok", "name": "Bacbo-Sinais-BotPro", "time": datetime.utcnow().isoformat()}

    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, threaded=True)

# --- 1. CONFIGURAÇÕES E CREDENCIAIS ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0").strip()
FREE_CANAL_ID_STR = os.getenv("CANAL_ID", "0").strip()
VIP_CANAL_ID_STR = os.getenv("VIP_CANAL_ID", "0").strip()
DEPOIMENTOS_ID_STR = os.getenv("DEPOIMENTOS_CANAL_ID", "0").strip()

# Conversões seguras
def _to_int(v: str) -> int:
    s = v.strip()
    if s.startswith("-"):
        s2 = s[1:]
        return -int(s2) if s2.isdigit() else 0
    return int(s) if s.isdigit() else 0

ADMIN_ID = _to_int(ADMIN_ID_STR)
FREE_CANAL_ID = _to_int(FREE_CANAL_ID_STR)
VIP_CANAL_ID = _to_int(VIP_CANAL_ID_STR)
DEPOIMENTOS_CANAL_ID = _to_int(DEPOIMENTOS_ID_STR)

URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_INSTAGRAM = "https://www.instagram.com/apostasmilionariasvip/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
SUPORTE_TELEGRAM = "@Superfinds_bot"

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("bot")

# Validação de variáveis
erros_config = []
if not BOT_TOKEN: erros_config.append("BOT_TOKEN")
if ADMIN_ID == 0: erros_config.append("ADMIN_ID")
if FREE_CANAL_ID == 0: erros_config.append("CANAL_ID")
if VIP_CANAL_ID == 0: erros_config.append("VIP_CANAL_ID")

if erros_config:
    logger.critical("ERRO CRÍTICO: Variáveis ausentes/invalidas: %s", ", ".join(erros_config))
    raise SystemExit(1)

if DEPOIMENTOS_CANAL_ID == 0:
    logger.warning("AVISO: DEPOIMENTOS_CANAL_ID não configurado. Depoimentos desativados.")

# --- 2. MÍDIAS E CONTEÚDO VISUAL ---
GIF_OFERTA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzBqZ3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
PROVAS_SOCIAIS_URLS = [
    f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png"
    for i in range(1, 14)
]

# --- 3. MENSAGENS DE MARKETING E FUNIL ---
MARKETING_MESSAGES = {
    "oferta_relampago": (
        "🚨 **OFERTA RELÂMPAGO LIBERADA!** 🚨\n\n"
        "Atenção! Eu recebi autorização para fazer algo que **NUNCA FIZEMOS ANTES**.\n\n"
        "Estou abrindo **AGORA** uma oportunidade única para os **{vagas_restantes} primeiros** que agirem rápido.\n\n"
        "O nosso acesso à **Sala VIP**, que tem uma mensalidade de R$ 549,90, sairá por **R$ 0,00 por 90 DIAS!**\n\n"
        "Isso mesmo, você leu certo. De ~~R$ 549,90~~ por **ZERO REAIS**.\n\n"
        "**COMO FUNCIONA?**\n"
        "Basta fazer o seu **PRIMEIRO DEPÓSITO** na nossa plataforma parceira através do link abaixo. Não importa o valor!\n\n"
        "👇 **QUERO MEU ACESSO AGORA** 👇\n"
        f"[**CLIQUE AQUI PARA FAZER SEU DEPÓSITO E GARANTIR 90 DIAS GRÁTIS**]({URL_CADASTRO_DEPOSITO})\n\n"
        "Ao garantir sua vaga, você leva TUDO isso:\n"
        "🔑 **Grupo VIP Pago Gratuito (por 90 dias)**\n"
        "🤖 Sinais com análise de IA em tempo real\n"
        "🗓️ Sinais organizados por horários\n"
        "💡 Ebook: Mentalidade e gestão de banca\n"
        "🎁 Sorteios exclusivos para membros\n"
        "📈 Material trader avançado\n"
        "💰 **Bônus de até R$600 no depósito**\n"
        "⚡ Sinais ilimitados em TODOS os jogos\n\n"
        "**ATENÇÃO:** Esta oferta é válida apenas pelas **próximas 12 HORAS** ou para os **{vagas_restantes} primeiros**, o que acontecer primeiro. Depois disso, o acesso VIP volta ao preço normal.\n\n"
        "Não perca a chance da sua vida de lucrar com os melhores. Toque no link, faça seu depósito e me envie o print no privado para liberar seu acesso IMEDIATAMENTE!\n\n"
        f"➡️ [**GARANTIR MINHA VAGA AGORA!**]({URL_CADASTRO_DEPOSITO})"
    ),
    "ultima_chance": (
        "⏳ **ÚLTIMA CHAMADA! RESTA APENAS 1 HORA!** ⏳\n\n"
        "A nossa oferta relâmpago de **90 DIAS DE ACESSO VIP GRÁTIS** está se encerrando.\n\n"
        "Restam pouquíssimas vagas e o tempo está acabando. Esta é sua última oportunidade de entrar para a elite e lucrar com nossos sinais VIP sem pagar NADA pela mensalidade.\n\n"
        "De ~~R$ 549,90~~ por **R$ 0,00**.\n\n"
        "Clique no link, faça seu primeiro depósito e garanta sua vaga antes que seja tarde demais!\n\n"
        f"➡️ [**PEGAR MINHA VAGA ANTES QUE ACABE!**]({URL_CADASTRO_DEPOSITO})"
    ),
    "divulgacao": (
        "🤖 **Cansado de perder dinheiro? Conheça nosso Robô de Sinais 100% GRATUITO!** 🤖\n\n"
        "Nossa inteligência artificial analisa o mercado 24/7 e envia sinais de alta assertividade para jogos como Roleta, Aviator, Mines, Slots e muito mais!\n\n"
        "✅ **Sinais Gratuitos Todos os Dias**\n✅ **Análises Precisas e em Tempo Real**\n✅ **Comunidade com Milhares de Membros Lucrando**\n\n"
        "Chega de contar com a sorte. Comece a lucrar com estratégia!\n\n"
        "👇 **ENTRE AGORA NO NOSSO CANAL GRATUITO E COMECE A LUCRAR HOJE MESMO!** 👇\n"
        f"🔗 {URL_TELEGRAM_FREE}\n🔗 {URL_TELEGRAM_FREE}\n"
    ),
    "boas_vindas_start": (
        "💎 **QUER LUCRAR COM SINAIS DE ALTA ASSERTIVIDADE?** 💎\n\n"
        "Você está no lugar certo! Meu nome é Super Finds, e meu trabalho é te ajudar a lucrar.\n\n"
        "No nosso canal gratuito você recebe algumas amostras, mas o verdadeiro potencial está na **Sala VIP Exclusiva**, com dezenas de sinais todos os dias!\n\n"
        "**COMO FUNCIONA O ACESSO VIP?**\n\n"
        "O acesso é **LIBERADO MEDIANTE DEPÓSITO** na plataforma parceira.\n\n"
        "1️⃣ **CADASTRE-SE E DEPOSITE:**\n"
        "Acesse o link, crie sua conta e faça um depósito.\n"
        f"➡️ [**CLIQUE AQUI PARA CADASTRAR E DEPOSITAR**]({URL_CADASTRO_DEPOSITO})\n\n"
        "2️⃣ **ENVIE O COMPROVANTE:**\n"
        "Mande o print do seu depósito **aqui mesmo, nesta conversa,** e receba seu link de acesso VIP na hora!\n"
        "➡️ **É só anexar a imagem e enviar para mim!**\n\n"
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

# --- 4. JOGOS, PROBABILIDADES E MAPAS ---
ASSERTIVIDADE_JOGOS = {
    "Bac Bo 🎲": [70, 20, 10], "Roleta 룰렛": [68, 22, 10], "Slots 🎰": [60, 25, 15],
    "Aviator ✈️": [75, 15, 10], "Spaceman 👨‍🚀": [75, 15, 10], "Mines 💣": [65, 20, 15],
    "Penalty Shoot-Out ⚽️": [72, 18, 10], "Fortune Dragon 🐲": [62, 23, 15],
    "Dragon Tiger 🐉🐅": [70, 20, 10],
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
# --- 5. ESTATÍSTICAS E UTILITÁRIOS ---

def inicializar_estatisticas(bot_data: dict):
    if 'start_time' not in bot_data:
        bot_data['start_time'] = datetime.now()
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bot_data.setdefault(f'{stat}_{ch}', 0)
            bot_data.setdefault(f'daily_{stat}_{ch}', 0)

async def log_admin_action(context: ContextTypes.DEFAULT_TYPE, action: str):
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 **Log de Admin:**\n{action}")
    except Exception as e:
        logger.error(f"Falha ao enviar log para o admin: {e}")

# --- 6. ENVIO DE SINAIS & PROVA SOCIAL ---

async def enviar_aviso_bloco(context: ContextTypes.DEFAULT_TYPE, jogo: str, tipo: str):
    if tipo == "inicio":
        mensagem = (
            f"🚨 **ATENÇÃO, JOGADORES VIP!** 🚨\n\n"
            f"Preparem-se! Em 10 minutos iniciaremos nossa maratona de sinais para o jogo **{jogo}**. "
            f"Fiquem atentos e com a plataforma aberta!"
        )
    elif tipo == "ultimo":
        mensagem = (
            f"⏳ **ÚLTIMO SINAL DO BLOCO!** ⏳\n\n"
            f"Vamos para a última entrada da nossa maratona de **{jogo}**. Foco total para fechar com chave de ouro!"
        )
    else:
        mensagem = (
            f"🏁 **BLOCO DE SINAIS ENCERRADO** 🏁\n\n"
            f"Finalizamos nossa maratona de **{jogo}**. Esperamos que tenham lucrado! "
            f"Fiquem atentos para os próximos blocos de sinais ao longo do dia."
        )
    await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem)
    logger.info(f"Aviso de '{tipo}' para {jogo} enviado ao canal VIP.")

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target_id: int):
    bd = context.bot_data
    inicializar_estatisticas(bd)
    channel_type = 'vip' if target_id == VIP_CANAL_ID else 'free'
    guard_key = f"sinal_em_andamento_{target_id}"

    if bd.get(guard_key, False):
        logger.warning(f"Pulei o sinal de {jogo} para {target_id} pois outro já estava em andamento.")
        return

    bd[guard_key] = True
    try:
        await context.bot.send_animation(
            chat_id=target_id,
            animation=GIF_ANALISANDO,
            caption=f"🔎 Analisando padrões para uma entrada em **{jogo}**..."
        )
        await asyncio.sleep(random.randint(5, 10))

        mensagem_sinal = (
            f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
            f"🎯 **Apostar em:** {aposta}\n"
            f"🔗 **JOGAR NA PLATAFORMA CERTA:** [**CLIQUE AQUI**]({URL_CADASTRO_DEPOSITO})"
        )
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP!_"

        await context.bot.send_message(
            chat_id=target_id, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"Sinal de {jogo} enviado para {target_id}.")

        bd[f'sinais_{channel_type}'] += 1
        bd[f'daily_sinais_{channel_type}'] += 1

        await asyncio.sleep(random.randint(45, 75))
        probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])
        resultado = random.choices(
            ["win_primeira", "win_gale", "loss"], weights=probabilidades, k=1
        )[0]

        bd[f'{resultado}_{channel_type}'] += 1
        bd[f'daily_{resultado}_{channel_type}'] += 1

        greens_dia = bd.get(f'daily_win_primeira_{channel_type}', 0) + bd.get(f'daily_win_gale_{channel_type}', 0)
        reds_dia = bd.get(f'daily_loss_{channel_type}', 0)
        placar_do_dia = f"📊 **Placar do Dia ({channel_type.upper()}):** {greens_dia}W - {reds_dia}L"

        if resultado == "win_primeira":
            caption = f"✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Parabéns a todos! 🤑\n\n{placar_do_dia}"
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
        bd[guard_key] = False

async def enviar_prova_social(context: ContextTypes.DEFAULT_TYPE):
    url_prova = random.choice(PROVAS_SOCIAIS_URLS)
    legenda = random.choice(MARKETING_MESSAGES["legendas_prova_social"])
    await context.bot.send_photo(
        chat_id=FREE_CANAL_ID,
        photo=url_prova,
        caption=f"{legenda}\n\n[**QUERO LUCRAR ASSIM TAMBÉM!**]({URL_CADASTRO_DEPOSITO})",
        parse_mode=ParseMode.MARKDOWN
    )

# --- 7. SEQUÊNCIA DE DMs PÓS-ENTRADA (FUNIL) ---

async def boas_vindas_sequencia(context: ContextTypes.DEFAULT_TYPE):
    """
    Envia uma sequência de DMs para pressionar a conversão.
    Correção aplicada: uso de chave 'nome_usuario' corretamente.
    """
    user_id = context.job.chat_id
    nome_usuario = context.job.data.get('nome_usuario', 'amigo')

    # Mensagem 1 (após ~1 hora do ingresso no grupo)
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"Ei {nome_usuario}, vi que você entrou no nosso grupo gratuito. 👀\n\n"
                f"Só pra você saber, as vagas para o acesso VIP de 90 dias GRÁTIS estão acabando. "
                f"Restam apenas **{random.randint(5, 9)}** vagas.\n\n"
                f"Não perca a chance de lucrar de verdade. "
                f"[**Clique aqui para garantir a sua vaga antes que acabe!**]({URL_CADASTRO_DEPOSITO})"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM Follow-up (1/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM Follow-up (1/2) para {user_id}: {e}")

    await asyncio.sleep(3600 * 4)  # Espera 4 horas

    # Mensagem 2
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"E aí, {nome_usuario}! Passando pra avisar que a oferta está quase no fim. 🔥\n\n"
                f"Muita gente já garantiu a vaga e está lucrando no VIP. Você vai mesmo ficar de fora?\n\n"
                f"Lembre-se: depósito de qualquer valor = 90 dias de VIP GRÁTIS. Simples assim.\n\n"
                f"[**ÚLTIMA CHANCE DE GARANTIR SUA VAGA**]({URL_CADASTRO_DEPOSITO})"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM Follow-up (2/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM Follow-up (2/2) para {user_id}: {e}")

# --- 8. COMANDOS DE ADMIN ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        MARKETING_MESSAGES["boas_vindas_start"],
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )
    await log_admin_action(context, f"Usuário {user.full_name} (id={user.id}) iniciou o bot.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    bd = context.bot_data
    inicializar_estatisticas(bd)
    uptime = datetime.now() - bd.get('start_time', datetime.now())

    stats_msg = "📊 **Estatísticas do Bot** 📊\n\n"
    stats_msg += f"Uptime: {str(uptime).split('.')[0]}\n\n"

    for ch in ["free", "vip"]:
        sinais = bd.get(f'sinais_{ch}', 0)
        w_p = bd.get(f'win_primeira_{ch}', 0)
        w_g = bd.get(f'win_gale_{ch}', 0)
        loss = bd.get(f'loss_{ch}', 0)
        assertividade = ((w_p + w_g) / sinais * 100) if sinais > 0 else 0

        stats_msg += f"**--- Canal {ch.upper()} ---**\n"
        stats_msg += f"Sinais: {sinais}\n"
        stats_msg += f"Wins (1ª): {w_p}\n"
        stats_msg += f"Wins (Gale): {w_g}\n"
        stats_msg += f"Losses: {loss}\n"
        stats_msg += f"Assertividade: {assertividade:.2f}%\n\n"

    await update.message.reply_text(stats_msg)

async def manual_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Uso: /sinal <free|vip> <jogo> <aposta...>")
        return

    target_channel, jogo_key, *aposta_parts = args
    aposta = " ".join(aposta_parts)
    jogo_nome = JOGOS_MAP.get(jogo_key.lower())

    if not jogo_nome:
        await update.message.reply_text(f"Jogo '{jogo_key}' não encontrado. Opções: {', '.join(JOGOS_MAP.keys())}")
        return

    target_id = VIP_CANAL_ID if target_channel.lower() == 'vip' else FREE_CANAL_ID

    context.job_queue.run_once(lambda ctx: enviar_sinal_especifico(ctx, jogo_nome, aposta, target_id), 1)
    await update.message.reply_text(f"✅ Sinal para '{jogo_nome}' agendado para o canal {target_channel.upper()}.")

# --- 9. AGENDAMENTO DE MENSAGENS DE MARKETING ---

async def send_marketing_message(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    msg_type = job_data.get("type", "divulgacao")
    vagas = random.randint(3, 7)

    if msg_type == "oferta_relampago":
        msg = MARKETING_MESSAGES["oferta_relampago"].format(vagas_restantes=vagas)
        gif = GIF_OFERTA
    elif msg_type == "ultima_chance":
        msg = MARKETING_MESSAGES["ultima_chance"]
        gif = None
    else:
        msg = MARKETING_MESSAGES["divulgacao"]
        gif = None

    try:
        if gif:
            await context.bot.send_animation(chat_id=FREE_CANAL_ID, animation=gif, caption=msg, parse_mode=ParseMode.MARKDOWN)
        else:
            await context.bot.send_message(chat_id=FREE_CANAL_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"Mensagem de marketing '{msg_type}' enviada.")
    except Exception as e:
        logger.error(f"Falha ao enviar marketing '{msg_type}': {e}")

async def reset_daily_stats(context: ContextTypes.DEFAULT_TYPE):
    bd = context.bot_data
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bd[f'daily_{stat}_{ch}'] = 0
    logger.info("Estatísticas diárias resetadas.")

    # Reagendar para o próximo dia
    agora = datetime.now()
    proximo_reset = (agora + timedelta(days=1)).replace(hour=0, minute=0, second=5, microsecond=0)
    context.job_queue.run_once(reset_daily_stats, when=(proximo_reset - agora).total_seconds())

# --- 10. MANIPULADORES DE EVENTOS ---

async def handle_new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if not member.is_bot:
            context.job_queue.run_once(
                boas_vindas_sequencia,
                3600,  # 1 hora
                chat_id=member.id,
                data={'nome_usuario': member.first_name}
            )
            logger.info(f"Sequência de DMs agendada para {member.full_name} ({member.id}).")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not update.message.photo:
        return

    try:
        file_id = update.message.photo[-1].file_id
        caption = (
            f"📩 **Comprovante recebido**\n"
            f"Usuário: {user.full_name} (id={user.id})\n"
            f"Username: @{user.username or 'N/A'}"
        )

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )

        await update.message.reply_text(
            "✅ Recebi seu comprovante! Vou validar rapidinho e já libero seu acesso VIP. "
            "Se precisar, me chame no suporte: " + SUPORTE_TELEGRAM
        )

        # (Opcional) após "validar", já libera:
        await context.bot.send_message(
            chat_id=user.id,
            text=MARKETING_MESSAGES["acesso_liberado_vip"],
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        logger.error(f"Erro ao processar foto: {e}")
        await update.message.reply_text("⚠️ Não consegui processar sua imagem agora. Tente reenviar, por favor.")

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Comando não reconhecido. Use /start.")

# --- 11. MAIN & AGENDADORES ---

def configurar_agendamentos(app: Application):
    jq = app.job_queue

    # Marketing recorrente
    jq.run_repeating(
        send_marketing_message,
        interval=3600 * 6,  # a cada 6 horas
        first=60,           # 1 min após iniciar
        data={"type": "divulgacao"}
    )
    jq.run_repeating(
        send_marketing_message,
        interval=3600 * 12,  # a cada 12 horas
        first=120,
        data={"type": "oferta_relampago"}
    )
    jq.run_repeating(
        send_marketing_message,
        interval=3600 * 24,  # a cada 24 horas
        first=180,
        data={"type": "ultima_chance"}
    )

    # Prova social no free a cada 4h
    jq.run_repeating(enviar_prova_social, interval=3600 * 4, first=300)

    # Reset diário às 00:00 (timezone do host)
    agora = datetime.now()
    proximo_reset = (agora + timedelta(days=1)).replace(hour=0, minute=0, second=5, microsecond=0)
    jq.run_once(reset_daily_stats, when=(proximo_reset - agora).total_seconds())

async def on_startup(app: Application):
    logger.info("Bot iniciado com sucesso.")

def build_application() -> Application:
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    # Comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("sinal", manual_signal_command))

    # Eventos
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat_members))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Agendamentos
    configurar_agendamentos(app)

    # Startup
    app.post_init = on_startup
    return app

def main():
    # Sobe um pequeno servidor Flask em thread (útil no Render)
    if _FLASK_AVAILABLE:
        threading.Thread(target=start_flask, daemon=True).start()

    app = build_application()
    logger.info("Iniciando pooling...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()


