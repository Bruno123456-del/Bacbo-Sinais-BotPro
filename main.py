# -*- coding: utf-8 -*-
# ===================================================================================
# MAIN.PY - BOT DE SINAIS APOSTAS MILIONÁRIAS V25.1 (ESTRATÉGIA BOT-FIRST)
# ARQUIVO PRINCIPAL PARA EXECUÇÃO DO BOT
# CRIADO E APRIMORADO POR MANUS
# ===================================================================================

import os
import logging
import random
import asyncio
from datetime import datetime

# Tenta importar o sistema de conversão. Se não encontrar, avisa e encerra.
try:
    from sistema_conversao_vip import SistemaConversaoVIP
except ImportError:
    print("ERRO CRÍTICO: O arquivo 'sistema_conversao_vip.py' não foi encontrado.")
    print("Certifique-se de que ambos os arquivos ('main.py' e 'sistema_conversao_vip.py') estão na mesma pasta.")
    exit()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters, CallbackQueryHandler
)

# --- CONFIGURAÇÕES DE SEGURANÇA ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "7975008855:AAFQfTcSn3r5HiR0eXPaimJo0K3pX7osNfw")
FREE_CANAL_ID = int(os.getenv("FREE_CANAL_ID", "-1002808626127"))
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "-1003053055680"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789")) # Coloque seu ID de admin aqui

# --- CONFIGURAÇÕES GERAIS ---
URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
URL_VIP_ACESSO = "https://t.me/+q2CCKi1CKmljMTFh"
SUPORTE_TELEGRAM = "@Superfinds_bot"

# --- CONFIGURAÇÃO DE LOGGING (CORRIGIDA ) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    style='%'
)
logging.getLogger("httpx" ).setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logger = logging.getLogger("bot_main")

# --- DADOS DO BOT (JOGOS, GIFS, ETC.) ---
JOGOS_COMPLETOS = {
    "Fortune Tiger 🐅": {"apostas": ["10 Rodadas Turbo", "15 Rodadas Normal"], "assertividade": [92, 7, 1]},
    "Aviator ✈️": {"apostas": ["Sair em 1.50x", "Sair em 2.00x"], "assertividade": [95, 4, 1]},
    "Mines 💣": {"apostas": ["3 Minas - 4 Cliques", "5 Minas - 2 Cliques"], "assertividade": [89, 9, 2]},
    "Bac Bo 🎲": {"apostas": ["Player", "Banker"], "assertividade": [94, 5, 1]},
    "Dragon Tiger 🐉🐅": {"apostas": ["Dragon", "Tiger"], "assertividade": [93, 6, 1]},
    "Roleta Brasileira 🇧🇷": {"apostas": ["Vermelho", "Preto", "1ª Dúzia"], "assertividade": [90, 8, 2]},
    "Spaceman 👨‍🚀": {"apostas": ["Sair em 1.80x", "Sair em 2.50x"], "assertividade": [94, 5, 1]},
    "Penalty Shoot-Out ⚽": {"apostas": ["Gol", "Defesa"], "assertividade": [91, 7, 2]},
    "Fortune Rabbit 🐰": {"apostas": ["8 Rodadas Turbo", "12 Rodadas Normal"], "assertividade": [90, 8, 2]},
    "Gates of Olympus ⚡": {"apostas": ["Ante Bet Ativo", "20 Rodadas Normal"], "assertividade": [88, 10, 2]},
    "Sweet Bonanza 🍭": {"apostas": ["Ante Bet 25%", "15 Rodadas Normal"], "assertividade": [89, 9, 2]},
    "Plinko 🎯": {"apostas": ["16 Pinos - Médio", "12 Pinos - Alto"], "assertividade": [87, 11, 2]},
    "Crazy Time 🎪": {"apostas": ["Número 1", "Número 2", "Coin Flip"], "assertividade": [85, 13, 2]},
    "Lightning Roulette ⚡": {"apostas": ["Números Sortudos", "Vermelho"], "assertividade": [89, 9, 2]},
    "Andar Bahar 🃏": {"apostas": ["Andar", "Bahar"], "assertividade": [92, 6, 2]}
}
GIFS_ANALISE = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"]
GIFS_VITORIA = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"]
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
IMG_GALE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"

# --- FUNÇÕES AUXILIARES ---
def inicializar_estatisticas(bot_data: dict ):
    if 'start_time' not in bot_data:
        bot_data['start_time'] = datetime.now()
    if 'usuarios_unicos' not in bot_data:
        bot_data['usuarios_unicos'] = set()
    bot_data.setdefault('conversoes_vip', 0)
    for ch in ['vip']: # Não precisamos mais de stats para o 'free'
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bot_data.setdefault(f'{stat}_{ch}', 0)

# --- COMANDOS DO BOT ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome_usuario = user.first_name or "Campeão"
    context.bot_data['usuarios_unicos'].add(user.id)
    logger.info(f"Novo usuário capturado pelo funil Bot-First: {nome_usuario} ({user.id})")

    mensagem = f"""
Olá, {nome_usuario}! 👋 Seja muito bem-vindo(a).

Se você está aqui, é porque está cansado(a) de perder dinheiro com estratégias que não funcionam e quer ter acesso a um método validado.

**Você tomou a decisão certa.**

Nossa Inteligência Artificial analisa 15 jogos 24h por dia, e hoje estamos com uma **condição histórica para novos membros.**

🔥 **OFERTA DE BOAS-VINDAS LIBERADA PARA VOCÊ:** 🔥

Use o código **`GESTAO`** e faça seu primeiro depósito para ganhar:

💰 **Bônus de até R$ 600,00** na plataforma.
💎 **90 DIAS DE ACESSO VIP GRÁTIS** ao nosso grupo de sinais.
🏆 **Acesso aos SORTEIOS MILIONÁRIOS** (Lamborghini, Rolex, etc).
📚 **E-book "Juros Compostos nas Apostas"**.

Esta é a sua chance de parar de apostar e começar a investir.

👇 **ESCOLHA SEU PRÓXIMO PASSO:**
"""
    keyboard = [
        [InlineKeyboardButton("🚀 SIM, QUERO ATIVAR A OFERTA AGORA!", callback_data="oferta_vip_imediata")],
        [InlineKeyboardButton("🤔 Quero ver as provas primeiro (Canal Gratuito)", url=URL_TELEGRAM_FREE)]
    ]
    await context.bot.send_animation(
        chat_id=user.id,
        animation=random.choice(GIFS_VITORIA),
        caption=mensagem,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    bd = context.bot_data
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    usuarios_unicos = len(bd.get('usuarios_unicos', set()))
    conversoes = bd.get('conversoes_vip', 0)
    sinais_vip = bd.get('sinais_vip', 0)
    greens_vip = bd.get('win_primeira_vip', 0) + bd.get('win_gale_vip', 0)
    reds_vip = bd.get('loss_vip', 0)
    taxa_conversao = (conversoes / max(usuarios_unicos, 1)) * 100
    assertividade_vip = (greens_vip / max(sinais_vip, 1)) * 100

    mensagem = f"""
📊 **ESTATÍSTICAS DO BOT**
Uptime: {uptime.days}d {uptime.seconds//3600}h
Usuários Capturados: {usuarios_unicos}
Conversões VIP: {conversoes} ({taxa_conversao:.1f}%)

💎 **Canal VIP:**
Sinais: {sinais_vip} | Greens: {greens_vip} | Reds: {reds_vip}
Assertividade: {assertividade_vip:.1f}%
"""
    await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)

# --- LÓGICA DE SINAIS (NOVA ESTRATÉGIA) ---
async def enviar_sinal_jogo(context: ContextTypes.DEFAULT_TYPE, jogo: str, target_id: int, confianca: float):
    bd = context.bot_data
    dados_jogo = JOGOS_COMPLETOS.get(jogo, {})
    aposta_escolhida = random.choice(dados_jogo.get("apostas", ["Aposta Padrão"]))

    if target_id == VIP_CANAL_ID:
        logger.info(f"Enviando sinal VIP completo para o jogo {jogo}.")
        await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_ANALISE), caption=f"🤖 Analisando padrões no {jogo}...")
        await asyncio.sleep(random.randint(8, 12))
        mensagem_sinal = f"💎 **SINAL VIP CONFIRMADO | {jogo}** 💎\n\n🎯 **ENTRADA:** {aposta_escolhida}\n🔥 **Confiança:** {'⭐' * 5} (ALTÍSSIMA)\n\n🔗 **JOGAR AGORA:**\n[**>> CLIQUE AQUI PARA ACESSAR A PLATAFORMA <<**]({URL_CADASTRO_DEPOSITO})"
        await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN)
        
        bd['sinais_vip'] += 1
        await asyncio.sleep(random.randint(60, 90))
        
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=dados_jogo["assertividade"], k=1)[0]
        bd[f'{resultado}_vip'] += 1
        
        if resultado == "win_primeira":
            await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_VITORIA), caption=f"✅✅✅ GREEN NA PRIMEIRA! {jogo} 🤑")
        elif resultado == "win_gale":
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE, caption=f"✅ GREEN NO GALE! {jogo} 💪")
        else:
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=f"❌ RED! Faz parte! {jogo} 🔄")

    elif target_id == FREE_CANAL_ID:
        logger.info(f"Enviando Sinal Fantasma (marketing) para o jogo {jogo}.")
        await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_ANALISE), caption=f"🤖 Analisando o {jogo}...")
        await asyncio.sleep(random.randint(5, 8))
        msg_oportunidade = f"🚨 **OPORTUNIDADE DE LUCRO IDENTIFICADA!** 🚨\n\nNossa IA encontrou um padrão com **{confianca*100:.0f}% de confiança** no **{jogo}**.\n\n🔥 **SINAL ENVIADO AGORA PARA OS MEMBROS VIP!** 🔥\n\nEles estão entrando na operação neste exato momento. Você não precisa mais ficar de fora!"
        keyboard = [[InlineKeyboardButton("💎 QUERO RECEBER ESSE SINAL! (ENTRAR NO VIP)", callback_data="oferta_vip")]]
        await context.bot.send_message(chat_id=target_id, text=msg_oportunidade, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        
        await asyncio.sleep(random.randint(70, 100))
        
        greens_vip = bd.get('win_primeira_vip', 0) + bd.get('win_gale_vip', 0)
        reds_vip = bd.get('loss_vip', 0)
        assertividade_vip = (greens_vip / max(greens_vip + reds_vip, 1)) * 100
        
        msg_resultado = f"✅✅ **GREEN NO VIP!** ✅✅\n\nO sinal que enviamos há pouco no **{jogo}** bateu! A entrada era: **{aposta_escolhida}**.\n\nNossos membros VIP acabaram de lucrar mais uma vez! 🤑\n\n📊 **Placar de hoje (Apenas VIP):**\n**{greens_vip} ✅ x {reds_vip} ❌** ({assertividade_vip:.1f}% de Assertividade)\n\nCansado de só olhar? Faça parte do time que lucra de verdade."
        keyboard_resultado = [[InlineKeyboardButton("🚀 CHEGA DE PERDER! QUERO ENTRAR NO VIP AGORA!", callback_data="oferta_vip")]]
        await context.bot.send_photo(
            chat_id=target_id,
            photo=f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{random.randint(1, 19 )}.png",
            caption=msg_resultado,
            reply_markup=InlineKeyboardMarkup(keyboard_resultado),
            parse_mode=ParseMode.MARKDOWN
        )

# --- CALLBACKS E EVENTOS ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data in ["oferta_vip", "oferta_vip_imediata"]:
        vagas_restantes = random.randint(5, 15)
        mensagem = f"""
🚨 **EXCELENTE DECISÃO, {user.first_name}!** 🚨
Você está a um passo de destravar tudo.
🔥 **Use o Código Promocional: `GESTAO`** 🔥
Ao fazer seu primeiro depósito, você desbloqueia:
💰 **BÔNUS DE ATÉ R$ 600,00**
💎 **90 DIAS DE ACESSO VIP GRÁTIS**
📚 **E-BOOK "JUROS COMPOSTOS"**
🏆 **SORTEIOS MILIONÁRIOS**
⚠️ **ATENÇÃO: RESTAM APENAS {vagas_restantes} VAGAS!**
**Passo 1:** Clique abaixo e faça seu cadastro/depósito.
**Passo 2:** Volte aqui e me envie o comprovante.
"""
        keyboard = [
            [InlineKeyboardButton("🚀 ATIVAR OFERTA E USAR CÓDIGO 'GESTAO'", url=URL_CADASTRO_DEPOSITO)],
            [InlineKeyboardButton("💬 JÁ DEPOSITEI, ENVIAR COMPROVANTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace('@', '' )}")]
        ]
        await context.bot.send_message(chat_id=user.id, text=mensagem, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    sistema_conversao = context.bot_data.get('sistema_conversao')
    if sistema_conversao:
        await sistema_conversao.processar_comprovante_deposito(user.id, user.first_name)
    else:
        await update.message.reply_text("✅ Comprovante recebido! Analisando...")

# --- AGENDAMENTOS (NOVA ESTRATÉGIA) ---
async def enviar_sinal_automatico(context: ContextTypes.DEFAULT_TYPE):
    jogo = random.choice(list(JOGOS_COMPLETOS.keys()))
    confianca_vip = random.uniform(0.90, 0.98)
    await enviar_sinal_jogo(context, jogo, VIP_CANAL_ID, confianca_vip)
    await asyncio.sleep(random.randint(15, 45))
    await enviar_sinal_jogo(context, jogo, FREE_CANAL_ID, confianca_vip)

async def enviar_marketing_automatico(context: ContextTypes.DEFAULT_TYPE):
    sistema_conversao = context.bot_data.get('sistema_conversao')
    if not sistema_conversao: return
    await sistema_conversao.enviar_campanha_marketing(FREE_CANAL_ID)

# --- FUNÇÃO PRINCIPAL ---
def main():
    logger.info("Iniciando o bot...")
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    sistema_conversao = SistemaConversaoVIP(app, URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM, URL_VIP_ACESSO)
    app.bot_data['sistema_conversao'] = sistema_conversao
    inicializar_estatisticas(app.bot_data)

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))

    jq = app.job_queue
    jq.run_repeating(enviar_sinal_automatico, interval=45 * 60, first=10)
    jq.run_repeating(enviar_marketing_automatico, interval=90 * 60, first=30)

    logger.info("🚀 Bot Apostas Milionárias V25.1 iniciado com sucesso!")
    logger.info(f"🎮 {len(JOGOS_COMPLETOS)} jogos disponíveis!")
    logger.info("💎 Sistema de conversão VIP ativado!")
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
