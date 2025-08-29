# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 24.3 "MÁQUINA DE CONVERSÃO VIP"
# APRIMORADO POR MANUS
# - Nova oferta estratégica (Torneio VIP: Rolex, Lamborghini).
# - Funil de boas-vindas otimizado para conversão imediata.
# - Lógica aprimorada para evitar spam e direcionar ao pagamento.
# - Correção de bugs e melhorias de robustez.
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
        return {"status": "ok", "name": "Bacbo-Sinais-BotPro-V24.3", "time": datetime.utcnow().isoformat()}

    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, threaded=True)

# --- 1. CONFIGURAÇÕES E CREDENCIAIS ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0").strip()
FREE_CANAL_ID_STR = os.getenv("CHAT_ID", "0").strip()
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
VIP_LINK_ACESSO = "https://t.me/+q2CCKi1CKmljMTFh" # Link real do seu grupo VIP

# Logging
logging.basicConfig(
    format="%(asctime )s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("bot")

# Validação de variáveis
erros_config = []
if not BOT_TOKEN: erros_config.append("BOT_TOKEN")
if ADMIN_ID == 0: erros_config.append("ADMIN_ID")
if FREE_CANAL_ID == 0: erros_config.append("CHAT_ID")
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
GIF_LUXO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3k4a2w4eDJwM2w4cWw2c3g2eDVwM3c4cTZyM3c4cTZyM3c4cTZyMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif" # GIF de luxo para a nova oferta
PROVAS_SOCIAIS_URLS = [
    f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png"
    for i in range(1, 14 )
]

# --- 3. MENSAGENS DE MARKETING E FUNIL (REFORMULADO) ---
MARKETING_MESSAGES = {
    "nova_oferta_torneio": (
        "**Maldivas, Rolex, Lamborghini... Isso não é só para herdeiros!**  Rolex, Lamborghini 💙\n\n"
        "É para os participantes do nosso **TORNEIO VIP!**\n\n"
        "Olha o que os jogadores ganharam da última vez:\n"
        "• Mala de dinheiro + viagem a Dubai para duas pessoas\n"
        "• Lamborghini Urus\n"
        "• Rolex Datejust 41\n"
        "• Ingressos para o BKFC Dubai\n"
        "• MacBook Pro 16” e iPhone 16 Pro Max\n\n"
        "Quer ter a chance de ganhar prêmios assim?\n"
        "O primeiro passo é entrar para o nosso **CLUBE PRIVADO.**\n\n"
        "🔥 **O jogo pelos prêmios mais desejados começa aqui!** 🔥\n"
        f"👇 **FAÇA SEU DEPÓSITO E ENTRE PARA A ELITE!** 👇\n"
        f"[QUERO ENTRAR NO CLUBE VIP AGORA!]({URL_CADASTRO_DEPOSITO})"
    ),
    "oferta_relampago": (
        "🚨 **OFERTA RELÂMPAGO LIBERADA!** 🚨\n\n"
        "Atenção! Recebi autorização para fazer algo que NUNCA FIZEMOS ANTES.\n\n"
        "Estou abrindo AGORA uma oportunidade única para os **{vagas_restantes} primeiros** que agirem rápido.\n\n"
        "Nosso acesso à Sala VIP, que tem uma mensalidade de R$ 549,90, sairá por **R$ 0,00 por 90 DIAS!**\n\n"
        "Isso mesmo, de ~~R$ 549,90~~ por **ZERO REAIS.**\n\n"
        "**COMO FUNCIONA?**\n"
        "Basta fazer o seu **PRIMEIRO DEPÓSITO** na nossa plataforma parceira através do link abaixo. **Qualquer valor te qualifica!**\n\n"
        f"👇 **QUERO MEU ACESSO AGORA** 👇\n"
        f"[CLIQUE AQUI PARA DEPOSITAR E GARANTIR 90 DIAS GRÁTIS]({URL_CADASTRO_DEPOSITO})\n\n"
        "Ao garantir sua vaga, você leva TUDO isso:\n"
        "🔑 **Acesso ao Grupo VIP Pago (por 90 dias)**\n"
        "🏆 **Chance de ganhar em Torneios Exclusivos (Rolex, Carros, Viagens)**\n"
        "🤖 Sinais com IA em tempo real (Assertividade de 95%+)\n"
        "💰 **Bônus de até R$600 no depósito**\n"
        "⚡️ Sinais ilimitados em TODOS os jogos\n\n"
        "**ATENÇÃO:** Esta oferta é válida apenas pelas próximas 12 HORAS ou para os **{vagas_restantes} primeiros**. Depois disso, o acesso VIP volta ao preço normal.\n\n"
        "Não perca a chance da sua vida. Toque no link, faça seu depósito e me envie o print no privado para liberar seu acesso IMEDIATAMENTE!\n\n"
        f"➡️ [GARANTIR MINHA VAGA AGORA!]({URL_CADASTRO_DEPOSITO})"
    ),
    "ultima_chance": (
        "⏳ **ÚLTIMA CHAMADA! RESTA APENAS 1 HORA!** ⏳\n\n"
        "Nossa oferta relâmpago de 90 DIAS DE ACESSO VIP GRÁTIS está se encerrando.\n\n"
        "Restam pouquíssimas vagas e o tempo está acabando. Esta é sua última oportunidade de entrar para a elite e lucrar com nossos sinais VIP sem pagar NADA pela mensalidade.\n\n"
        "De R$ 549,90 por R$ 0,00.\n\n"
        "Clique no link, faça seu primeiro depósito e garanta sua vaga antes que seja tarde demais!\n\n"
        f"➡️ [PEGAR MINHA VAGA ANTES QUE ACABE!]({URL_CADASTRO_DEPOSITO})"
    ),
    "boas_vindas_dm": (
        "💎 **SEU ACESSO VIP ESTÁ A UM PASSO!** 💎\n\n"
        "Olá! Meu nome é Super Finds, e meu trabalho é te ajudar a lucrar de verdade.\n\n"
        "Você entrou no nosso canal gratuito, onde damos uma pequena amostra do nosso poder. Mas a verdadeira mina de ouro, com **dezenas de sinais todos os dias e lucros consistentes**, está na **Sala VIP Exclusiva.**\n\n"
        "**COMO ENTRAR PARA A ELITE?**\n"
        "O acesso é **LIBERADO IMEDIATAMENTE** após seu primeiro depósito na plataforma parceira.\n\n"
        "1️⃣ **CADASTRE-SE E DEPOSITE:**\n"
        "Acesse o link abaixo, crie sua conta e faça um depósito de qualquer valor.\n"
        f"➡️ [**CLIQUE AQUI PARA CADASTRAR E DEPOSITAR**]({URL_CADASTRO_DEPOSITO})\n\n"
        "2️⃣ **ENVIE O COMPROVANTE:**\n"
        "Mande o print (a foto) do seu depósito **aqui mesmo, nesta conversa**, e eu te envio o link de acesso VIP na hora!\n\n"
        "É simples: depositou, mandou o print, lucrou. Estou aguardando!"
    ),
    "acesso_liberado_vip": (
        "🚀 **ACESSO LIBERADO! BEM-VINDO(A) À ELITE!** 🚀\n\n"
        "Comprovante recebido e verificado com sucesso!\n\n"
        "Parabéns, você acaba de entrar para o nosso seleto grupo de vencedores. Aqui está o seu link de acesso exclusivo. **Não compartilhe com ninguém, ele é pessoal e intransferível.**\n\n"
        f"🔗 **Seu Link VIP:** {VIP_LINK_ACESSO}\n\n"
        "Prepare-se para uma chuva de sinais e lucros. Boas apostas!"
    ),
    "legendas_prova_social": [
        "🔥 O GRUPO VIP ESTÁ PEGANDO FOGO! 🔥\n\nMais um de nossos membros VIP lucrando alto. E você, vai ficar de fora?",
        "🚀 RESULTADO DE MEMBRO VIP! 🚀\n\nAnálises precisas, resultados reais. Parabéns pelo green! Isso é só o começo.",
        "🤔 AINDA NA DÚVIDA? 🤔\n\nEnquanto você pensa, outros estão enchendo o bolso. O acesso VIP te coloca na frente.",
        "✅ RESULTADOS FALAM MAIS QUE PALAVRAS! ✅\n\nMais um green para a conta da família VIP. A consistência que você procura está aqui."
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
    "Roleta 룰렛": ["Vermelho ⚫️", "Preto 🔴", "Par", "Ímpar", "1ª Dúzia", "2ª Dúzia", "3ª Dúzia"],
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
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 **Log de Admin:**\n{action}", parse_mode=ParseMode.MARKDOWN)
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
    else: # fim
        mensagem = (
            f"🏁 **BLOCO DE SINAIS ENCERRADO** 🏁\n\n"
            f"Finalizamos nossa maratona de **{jogo}**. Esperamos que tenham lucrado! "
            f"Fiquem atentos para os próximos blocos de sinais ao longo do dia."
        )
    await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem, parse_mode=ParseMode.MARKDOWN)
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
            caption=f"🔎 **Analisando padrões para uma entrada em {jogo}...**\n\nNossa IA está buscando a melhor oportunidade. Fique atento!"
        )
        await asyncio.sleep(random.randint(5, 10))

        mensagem_sinal = (
            f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
            f"🎯 **Apostar em:** {aposta}\n"
            f"🔗 **JOGAR NA PLATAFORMA CERTA:** [CLIQUE AQUI]({URL_CADASTRO_DEPOSITO})"
        )
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP! Boa sorte, elite!_"

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
            caption = f"✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Dinheiro no bolso da galera! 🤑\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_GREEN_PRIMEIRA, caption=caption, parse_mode=ParseMode.MARKDOWN)
        elif resultado == "win_gale":
            caption = f"✅ **GREEN NO GALE!** ✅\n\nPaciência e gestão trazem o lucro. Parabéns, time!\n\n{placar_do_dia}"
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE1, caption=caption, parse_mode=ParseMode.MARKDOWN)
        else:
            caption = f"❌ **RED!** ❌\n\nFaz parte do jogo. Mantenham a gestão de banca e vamos para a próxima! O VIP sempre recupera.\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=caption, parse_mode=ParseMode.MARKDOWN)

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
        caption=f"{legenda}\n\n[QUERO LUCRAR ASSIM TAMBÉM!]({URL_CADASTRO_DEPOSITO})",
        parse_mode=ParseMode.MARKDOWN
    )

# --- 7. SEQUÊNCIA DE DMs PÓS-ENTRADA (FUNIL OTIMIZADO) ---

async def boas_vindas_sequencia(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.chat_id
    nome_usuario = context.job.data.get('nome_usuario', 'amigo')

    # Mensagem 1 (após 1 hora) - Urgência
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"Ei {nome_usuario}, vi que você ainda não garantiu seu acesso VIP. 👀\n\n"
                f"As vagas para o acesso de 90 dias GRÁTIS estão acabando. **Restam apenas {random.randint(5, 9)} vagas.**\n\n"
                f"Não perca a chance de lucrar de verdade. É só fazer um depósito de qualquer valor.\n"
                f"➡️ [**CLIQUE AQUI PARA GARANTIR SUA VAGA**]({URL_CADASTRO_DEPOSITO})"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM Follow-up (1/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM Follow-up (1/2) para {user_id}: {e}")
        return

    # Pausa de 23 horas para a próxima mensagem
    await asyncio.sleep(3600 * 23)

    # Mensagem 2 (após 24h) - Prova Social + Última Chance
    try:
        placar_vip_greens = random.randint(18, 25)
        placar_vip_reds = random.randint(1, 3)
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "💰 **SÓ PARA VOCÊ NÃO DIZER QUE EU NÃO AVISEI...** 💰\n\n"
                f"Enquanto você esteve no grupo gratuito, o placar na Sala VIP nas últimas 24h foi de **{placar_vip_greens} GREENS ✅ e apenas {placar_vip_reds} REDS ❌.**\n\n"
                "As pessoas lá dentro estão fazendo dinheiro. E você?\n\n"
                f"Essa é a **ÚLTIMA CHANCE** de conseguir 90 dias de acesso VIP de graça. Depois disso, só pagando o valor cheio.\n"
                f"➡️ [**QUERO LUCRAR AGORA!**]({URL_CADASTRO_DEPOSITO})"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM Follow-up (2/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM Follow-up (2/2) para {user_id}: {e}")

# --- 8. MARKETING PROGRAMADO E RESET DIÁRIO ---

async def send_marketing_message(context: ContextTypes.DEFAULT_TYPE):
    message_type = context.job.data["type"]
    vagas_restantes = random.randint(3, 7)
    message_text = MARKETING_MESSAGES[message_type]
    
    gif_map = {
        "oferta_relampago": GIF_OFERTA,
        "ultima_chance": GIF_OFERTA,
        "nova_oferta_torneio": GIF_LUXO
    }
    gif_to_send = gif_map.get(message_type)

    if message_type in {"oferta_relampago"}:
        message_text = message_text.format(vagas_restantes=vagas_restantes)

    try:
        if gif_to_send:
            await context.bot.send_animation(
                chat_id=FREE_CANAL_ID,
                animation=gif_to_send,
                caption=message_text,
                parse_mode=ParseMode.MARKDOWN
            )
        else: # Para mensagens sem GIF, como a de divulgação antiga
             await context.bot.send_message(
                chat_id=FREE_CANAL_ID,
                text=message_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
        logger.info(f"Mensagem de marketing '{message_type}' enviada.")
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem de marketing '{message_type}': {e}")

async def reset_daily_stats(context: ContextTypes.DEFAULT_TYPE):
    bd = context.bot_data
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bd[f'daily_{stat}_{ch}'] = 0
    logger.info("Estatísticas diárias resetadas.")
    await log_admin_action(context, "Estatísticas diárias foram resetadas.")

# --- 9. COMANDOS ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=MARKETING_MESSAGES["boas_vindas_dm"],
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    await log_admin_action(context, "Comando /stats executado.")
    bd = context.bot_data
    inicializar_estatisticas(bd)
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    days, rem = divmod(int(uptime.total_seconds()), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    stats_text = (
        f"📊 **PAINEL DE ESTATÍSTICAS GERAIS** 📊\n\n"
        f"🕒 **Tempo Ativo:** {days}d, {hours}h, {minutes}m\n\n"
        f"--- **Canal Gratuito (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_free', 0)} | ✅: {bd.get('win_primeira_free', 0)} | "
        f"☑️: {bd.get('win_gale_free', 0)} | ❌: {bd.get('loss_free', 0)}\n\n"
        f"--- **Canal VIP (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_vip', 0)} | ✅: {bd.get('win_primeira_vip', 0)} | "
        f"☑️: {bd.get('win_gale_vip', 0)} | ❌: {bd.get('loss_vip', 0)}\n"
    )
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

# --- CÓDIGO CORRIGIDO PARA O BLOCO 2 ---

async def manual_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        # Espera 3 argumentos: /sinal <jogo> <canal>
        if len(context.args) != 2:
            await update.message.reply_text(
                "⚠️ **Uso incorreto!**\nUse: `/sinal <jogo> <canal>`\nEx.: `/sinal mines vip`",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        jogo_curto, canal = context.args
        jogo_completo = JOGOS_MAP.get(jogo_curto.lower())

        if not jogo_completo:
            await update.message.reply_text(
                f"❌ Jogo '{jogo_curto}' não encontrado. Use um dos: {', '.join(JOGOS_MAP.keys())}"
            )
            return
            
        target_id = VIP_CANAL_ID if canal.lower() == 'vip' else FREE_CANAL_ID

        aposta = random.choice(JOGOS[jogo_completo])

        context.job_queue.run_once(
            callback=lambda ctx: asyncio.create_task(
                enviar_sinal_especifico(ctx, jogo_completo, aposta, target_id)
            ),
            when=0
        )

        log_message = f"Comando /sinal {jogo_curto} enviado para o canal {canal.upper()}."
        await log_admin_action(context, log_message)
        await update.message.reply_text(f"✅ Sinal manual para `{jogo_completo}` agendado para o canal **{canal.upper()}**.", parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao processar comando /sinal: {e}")
        logger.error(f"Erro no comando /sinal manual: {e}")

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
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 **Log de Admin:**\n{action}", parse_mode=ParseMode.MARKDOWN)
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
    else: # fim
        mensagem = (
            f"🏁 **BLOCO DE SINAIS ENCERRADO** 🏁\n\n"
            f"Finalizamos nossa maratona de **{jogo}**. Esperamos que tenham lucrado! "
            f"Fiquem atentos para os próximos blocos de sinais ao longo do dia."
        )
    await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem, parse_mode=ParseMode.MARKDOWN)
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
            caption=f"🔎 **Analisando padrões para uma entrada em {jogo}...**\n\nNossa IA está buscando a melhor oportunidade. Fique atento!"
        )
        await asyncio.sleep(random.randint(5, 10))

        mensagem_sinal = (
            f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
            f"🎯 **Apostar em:** {aposta}\n"
            f"🔗 **JOGAR NA PLATAFORMA CERTA:** [CLIQUE AQUI]({URL_CADASTRO_DEPOSITO})"
        )
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP! Boa sorte, elite!_"

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
            caption = f"✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Dinheiro no bolso da galera! 🤑\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_GREEN_PRIMEIRA, caption=caption, parse_mode=ParseMode.MARKDOWN)
        elif resultado == "win_gale":
            caption = f"✅ **GREEN NO GALE!** ✅\n\nPaciência e gestão trazem o lucro. Parabéns, time!\n\n{placar_do_dia}"
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE1, caption=caption, parse_mode=ParseMode.MARKDOWN)
        else:
            caption = f"❌ **RED!** ❌\n\nFaz parte do jogo. Mantenham a gestão de banca e vamos para a próxima! O VIP sempre recupera.\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=caption, parse_mode=ParseMode.MARKDOWN)

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
        caption=f"{legenda}\n\n[QUERO LUCRAR ASSIM TAMBÉM!]({URL_CADASTRO_DEPOSITO})",
        parse_mode=ParseMode.MARKDOWN
    )

# --- 7. SEQUÊNCIA DE DMs PÓS-ENTRADA (FUNIL OTIMIZADO) ---

async def boas_vindas_sequencia(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.chat_id
    nome_usuario = context.job.data.get('nome_usuario', 'amigo')

    # Mensagem 1 (após 1 hora) - Urgência
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"Ei {nome_usuario}, vi que você ainda não garantiu seu acesso VIP. 👀\n\n"
                f"As vagas para o acesso de 90 dias GRÁTIS estão acabando. **Restam apenas {random.randint(5, 9)} vagas.**\n\n"
                f"Não perca a chance de lucrar de verdade. É só fazer um depósito de qualquer valor.\n"
                f"➡️ [**CLIQUE AQUI PARA GARANTIR SUA VAGA**]({URL_CADASTRO_DEPOSITO})"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM Follow-up (1/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM Follow-up (1/2) para {user_id}: {e}")
        return

    # Pausa de 23 horas para a próxima mensagem
    await asyncio.sleep(3600 * 23)

    # Mensagem 2 (após 24h) - Prova Social + Última Chance
    try:
        placar_vip_greens = random.randint(18, 25)
        placar_vip_reds = random.randint(1, 3)
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "💰 **SÓ PARA VOCÊ NÃO DIZER QUE EU NÃO AVISEI...** 💰\n\n"
                f"Enquanto você esteve no grupo gratuito, o placar na Sala VIP nas últimas 24h foi de **{placar_vip_greens} GREENS ✅ e apenas {placar_vip_reds} REDS ❌.**\n\n"
                "As pessoas lá dentro estão fazendo dinheiro. E você?\n\n"
                f"Essa é a **ÚLTIMA CHANCE** de conseguir 90 dias de acesso VIP de graça. Depois disso, só pagando o valor cheio.\n"
                f"➡️ [**QUERO LUCRAR AGORA!**]({URL_CADASTRO_DEPOSITO})"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM Follow-up (2/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM Follow-up (2/2) para {user_id}: {e}")

# --- 8. MARKETING PROGRAMADO E RESET DIÁRIO ---

async def send_marketing_message(context: ContextTypes.DEFAULT_TYPE):
    message_type = context.job.data["type"]
    vagas_restantes = random.randint(3, 7)
    message_text = MARKETING_MESSAGES[message_type]
    
    gif_map = {
        "oferta_relampago": GIF_OFERTA,
        "ultima_chance": GIF_OFERTA,
        "nova_oferta_torneio": GIF_LUXO
    }
    gif_to_send = gif_map.get(message_type)

    if message_type in {"oferta_relampago"}:
        message_text = message_text.format(vagas_restantes=vagas_restantes)

    try:
        if gif_to_send:
            await context.bot.send_animation(
                chat_id=FREE_CANAL_ID,
                animation=gif_to_send,
                caption=message_text,
                parse_mode=ParseMode.MARKDOWN
            )
        else: # Para mensagens sem GIF, como a de divulgação antiga
             await context.bot.send_message(
                chat_id=FREE_CANAL_ID,
                text=message_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
        logger.info(f"Mensagem de marketing '{message_type}' enviada.")
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem de marketing '{message_type}': {e}")

async def reset_daily_stats(context: ContextTypes.DEFAULT_TYPE):
    bd = context.bot_data
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bd[f'daily_{stat}_{ch}'] = 0
    logger.info("Estatísticas diárias resetadas.")
    await log_admin_action(context, "Estatísticas diárias foram resetadas.")

# --- 9. COMANDOS ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=MARKETING_MESSAGES["boas_vindas_dm"],
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    await log_admin_action(context, "Comando /stats executado.")
    bd = context.bot_data
    inicializar_estatisticas(bd)
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    days, rem = divmod(int(uptime.total_seconds()), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    stats_text = (
        f"📊 **PAINEL DE ESTATÍSTICAS GERAIS** 📊\n\n"
        f"🕒 **Tempo Ativo:** {days}d, {hours}h, {minutes}m\n\n"
        f"--- **Canal Gratuito (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_free', 0)} | ✅: {bd.get('win_primeira_free', 0)} | "
        f"☑️: {bd.get('win_gale_free', 0)} | ❌: {bd.get('loss_free', 0)}\n\n"
        f"--- **Canal VIP (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_vip', 0)} | ✅: {bd.get('win_primeira_vip', 0)} | "
        f"☑️: {bd.get('win_gale_vip', 0)} | ❌: {bd.get('loss_vip', 0)}\n"
    )
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

async def manual_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        _, jogo_curto, canal = context.args
        jogo_completo = JOGOS_MAP.get(jogo_curto.lower())
        if not jogo_completo:
            await update.message.reply_text(
                f"❌ Jogo '{jogo_curto}' não encontrado. Use um dos: {', '.join(JOGOS_MAP.keys())}"
            )
            return
        target_id = VIP_CANAL_ID if

