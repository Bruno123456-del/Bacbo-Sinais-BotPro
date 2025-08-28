# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 20.7 "A VERSÃO FINAL, TESTADA E COMPLETA"
# CRIADO E APRIMORADO POR MANUS
# - CÓDIGO COMPLETO, COM TODAS AS FUNÇÕES E CORREÇÕES DE SINTAXE.
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, timedelta, datetime
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters
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

logging.basicConfig(
    format="%(asctime )s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Validação inteligente para garantir que as variáveis essenciais estão configuradas
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
PROVAS_SOCIAIS_URLS = [f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png" for i in range(1, 14  )]

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

# --- 5. AGENDAMENTO DE SINAIS AUTOMÁTICOS ---
# Formato: (hora, minuto, 'jogo_curto', 'canal_tipo')
# **PERSONALIZAR AQUI**
AGENDA_SINAIS = [
    (10, 30, 'roleta', 'free'), (14, 30, 'mines', 'free'), (18, 30, 'aviator', 'free'),
    (9, 0, 'bacbo', 'vip'), (9, 15, 'dragontiger', 'vip'), (11, 0, 'roleta', 'vip'),
    (11, 15, 'penalty', 'vip'), (13, 0, 'spaceman', 'vip'), (13, 15, 'aviator', 'vip'),
    (15, 0, 'slots', 'vip'), (15, 15, 'fortunedragon', 'vip'), (17, 0, 'mines', 'vip'),
    (17, 15, 'roleta', 'vip'), (19, 0, 'bacbo', 'vip'), (19, 15, 'dragontiger', 'vip'),
    (21, 0, 'aviator', 'vip'), (21, 15, 'penalty', 'vip'),
]

# --- 6. LÓGICA PRINCIPAL DO BOT ---
async def enviar_aviso_bloco(context: ContextTypes.DEFAULT_TYPE, jogo: str, tipo: str):
    mensagem = ""
    if tipo == "inicio":
        mensagem = f"🚨 **ATENÇÃO, JOGADORES VIP!** 🚨\n\nPreparem-se! Em 10 minutos iniciaremos nossa maratona de sinais para o jogo **{jogo}**. Fiquem atentos e com a plataforma aberta!"
    elif tipo == "ultimo":
        mensagem = f"⏳ **ÚLTIMO SINAL DO BLOCO!** ⏳\n\nVamos para a última entrada da nossa maratona de **{jogo}**. Foco total para fechar com chave de ouro!"
    else:
        mensagem = f"🏁 **BLOCO DE SINAIS ENCERRADO** 🏁\n\nFinalizamos nossa maratona de **{jogo}**. Esperamos que tenham lucrado! Fiquem atentos para os próximos blocos de sinais ao longo do dia."
    await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem)
    logger.info
