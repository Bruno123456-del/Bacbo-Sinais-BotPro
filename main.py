# -*- coding: utf-8 -*-
# ===================================================================================
# MAIN.PY - BOT DE SINAIS APOSTAS MILIONÁRIAS V25.1
# ARQUIVO PRINCIPAL PARA EXECUÇÃO DO BOT
# CRIADO E APRIMORADO POR MANUS
# ===================================================================================

import os
import logging
import random
import asyncio
import threading
from datetime import time as dt_time, timedelta, datetime
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters, CallbackQueryHandler
)

# --- HEALTHCHECK FLASK ---
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
        return {
            "status": "ok", 
            "name": "Apostas-Milionarias-BotPro-V25.1", 
            "jogos": 15,
            "time": datetime.utcnow().isoformat()
        }

    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, threaded=True)

# --- CONFIGURAÇÕES ---
BOT_TOKEN = "7975008855:AAFQfTcSn3r5HiR0eXPaimJo0K3pX7osNfw"
FREE_CANAL_ID = -1002808626127  # Apostas Milionárias Free 🔥
VIP_CANAL_ID = -1003053055680   # Palpites Milionários VIP IA
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
URL_VIP_ACESSO = "https://t.me/+q2CCKi1CKmljMTFh"
SUPORTE_TELEGRAM = "@Superfinds_bot"

# Logging
logging.basicConfig(
    format="%(asctime )s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger("bot_main")

# --- JOGOS E CONFIGURAÇÕES ---
JOGOS_COMPLETOS = {
    "Fortune Tiger 🐅": {
        "apostas": ["10 Rodadas Turbo", "15 Rodadas Normal", "Aguardar Padrão Especial"],
        "assertividade": [75, 20, 5],
        "frases_analise": ["🐅 O tigrinho está rugindo de oportunidade...", "💰 Detectando padrão dourado no Tiger..."]
    },
    "Aviator ✈️": {
        "apostas": ["Sair em 1.50x", "Sair em 2.00x", "Dupla Aposta"],
        "assertividade": [82, 15, 3],
        "frases_analise": ["✈️ Calculando trajetória de voo perfeita...", "📈 Analisando histórico de multiplicadores..."]
    },
    "Mines 💣": {
        "apostas": ["3 Minas - 4 Cliques", "5 Minas - 2 Cliques", "Estratégia Segura"],
        "assertividade": [71, 24, 5],
        "frases_analise": ["💣 Mapeando campo minado com precisão...", "🗺️ Identificando zonas seguras..."]
    },
    "Bac Bo 🎲": {
        "apostas": ["Player", "Banker", "Tie (Empate)"],
        "assertividade": [78, 18, 4],
        "frases_analise": ["🎲 Analisando padrões das cartas no Bac Bo...", "📊 Processando histórico de empates..."]
    },
    "Dragon Tiger 🐉🐅": {
        "apostas": ["Dragon", "Tiger", "Tie (Empate)"],
        "assertividade": [76, 19, 5],
        "frases_analise": ["🐉 O dragão está se preparando para atacar...", "🐅 O tigre farejou uma oportunidade..."]
    },
    "Roleta Brasileira 🇧🇷": {
        "apostas": ["Vermelho", "Preto", "Par", "Ímpar", "1ª Dúzia"],
        "assertividade": [72, 23, 5],
        "frases_analise": ["🎡 Analisando padrões da roleta brasileira...", "🔴 Identificando sequências de cores..."]
    },
    "Spaceman 👨‍🚀": {
        "apostas": ["Sair em 1.80x", "Sair em 2.50x", "Estratégia Dupla"],
        "assertividade": [80, 17, 3],
        "frases_analise": ["👨‍🚀 Astronauta em missão espacial lucrativa...", "🚀 Calculando órbita perfeita..."]
    },
    "Penalty Shoot-Out ⚽": {
        "apostas": ["Gol", "Defesa", "Sequência de 3"],
        "assertividade": [77, 18, 5],
        "frases_analise": ["⚽ Analisando padrões de pênaltis...", "🥅 Estudando comportamento do goleiro..."]
    },
    "Fortune Rabbit 🐰": {
        "apostas": ["8 Rodadas Turbo", "12 Rodadas Normal", "Aguardar Coelho Dourado"],
        "assertividade": [73, 22, 5],
        "frases_analise": ["🐰 Coelhinho da sorte detectado...", "🥕 Padrão de cenouras identificado..."]
    },
    "Gates of Olympus ⚡": {
        "apostas": ["Ante Bet Ativo", "20 Rodadas Normal", "Aguardar Zeus"],
        "assertividade": [68, 27, 5],
        "frases_analise": ["⚡ Zeus está carregando seus poderes...", "🏛️ Portões do Olimpo se abrindo..."]
    },
    "Sweet Bonanza 🍭": {
        "apostas": ["Ante Bet 25%", "15 Rodadas Normal", "Aguardar Scatter"],
        "assertividade": [70, 25, 5],
        "frases_analise": ["🍭 Doces explosivos detectados...", "🍬 Padrão de multiplicadores formando..."]
    },
    "Plinko 🎯": {
        "apostas": ["16 Pinos - Médio", "12 Pinos - Alto", "Auto Drop"],
        "assertividade": [69, 26, 5],
        "frases_analise": ["🎯 Calculando trajetória da bolinha...", "📐 Analisando ângulos de queda..."]
    },
    "Crazy Time 🎪": {
        "apostas": ["Número 1", "Número 2", "Coin Flip", "Crazy Time"],
        "assertividade": [65, 30, 5],
        "frases_analise": ["🎪 Show maluco começando...", "🎡 Roda da fortuna girando..."]
    },
    "Lightning Roulette ⚡": {
        "apostas": ["Números Sortudos", "Vermelho", "Straight Up"],
        "assertividade": [70, 25, 5],
        "frases_analise": ["⚡ Raios de multiplicadores detectados...", "🎡 Roleta eletrificada ativada..."]
    },
    "Andar Bahar 🃏": {
        "apostas": ["Andar", "Bahar", "1st Card Joker"],
        "assertividade": [74, 21, 5],
        "frases_analise": ["🃏 Cartas indianas revelando segredos...", "🎴 Padrão tradicional identificado..."]
    }
}

# GIFs e mídias
GIFS_ANALISE = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tn33aiTi1jkl6H6/giphy.gif"
]

GIFS_VITORIA = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26u4cqiYI30juCOGY/giphy.gif"
]

GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

IMG_GALE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"

PROVAS_SOCIAIS = [
    f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png"
    for i in range(1, 20 )
]

# Frases humanizadas
NOMES_HUMANIZADOS = ["Parceiro", "Amigo", "Guerreiro", "Campeão", "Vencedor", "Investidor", "Trader", "Craque"]
SAUDACOES = ["Olá, {nome}! 👋", "E aí, {nome}! 🔥", "Fala, {nome}! 💪", "Opa, {nome}! ⚡"]
FRASES_MOTIVACIONAIS = [
    "Hoje é o seu dia de sorte! 🍀",
    "A fortuna favorece os corajosos! 💪", 
    "Seus lucros estão chegando! 💰",
    "Prepare-se para lucrar! 🚀"
]

# --- FUNÇÕES AUXILIARES ---
def inicializar_estatisticas(bot_data: dict):
    if 'start_time' not in bot_data:
        bot_data['start_time'] = datetime.now()
    
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bot_data.setdefault(f'{stat}_{ch}', 0)
            bot_data.setdefault(f'daily_{stat}_{ch}', 0)
    
    bot_data.setdefault('usuarios_unicos', set())
    bot_data.setdefault('conversoes_vip', 0)

def get_jogo_por_palavra(palavra):
    """Encontra jogo por palavra-chave"""
    palavra_lower = palavra.lower()
    mapeamento = {
        "tiger": "Fortune Tiger 🐅", "tigrinho": "Fortune Tiger 🐅",
        "aviator": "Aviator ✈️", "aviao": "Aviator ✈️",
        "mines": "Mines 💣", "minas": "Mines 💣",
        "bac": "Bac Bo 🎲", "bacbo": "Bac Bo 🎲",
        "dragon": "Dragon Tiger 🐉🐅", "tiger": "Dragon Tiger 🐉🐅",
        "roleta": "Roleta Brasileira 🇧🇷", "brasileira": "Roleta Brasileira 🇧🇷",
        "spaceman": "Spaceman 👨‍🚀", "astronauta": "Spaceman 👨‍🚀",
        "penalty": "Penalty Shoot-Out ⚽", "penalti": "Penalty Shoot-Out ⚽",
        "rabbit": "Fortune Rabbit 🐰", "coelho": "Fortune Rabbit 🐰",
        "gates": "Gates of Olympus ⚡", "olympus": "Gates of Olympus ⚡",
        "sweet": "Sweet Bonanza 🍭", "bonanza": "Sweet Bonanza 🍭",
        "plinko": "Plinko 🎯",
        "crazy": "Crazy Time 🎪", "time": "Crazy Time 🎪",
        "lightning": "Lightning Roulette ⚡",
        "andar": "Andar Bahar 🃏", "bahar": "Andar Bahar 🃏"
    }
    return mapeamento.get(palavra_lower)

def listar_jogos():
    """Lista todos os jogos formatados"""
    categorias = {
        "🃏 CARTAS": ["Bac Bo 🎲", "Dragon Tiger 🐉🐅", "Andar Bahar 🃏"],
        "🎰 SLOTS": ["Fortune Tiger 🐅", "Fortune Rabbit 🐰", "Gates of Olympus ⚡", "Sweet Bonanza 🍭"],
        "🎲 CRASH": ["Aviator ✈️", "Spaceman 👨‍🚀"],
        "🎯 ESPECIAIS": ["Mines 💣", "Plinko 🎯", "Penalty Shoot-Out ⚽", "Crazy Time 🎪"],
        "🎡 ROLETA": ["Roleta Brasileira 🇧🇷", "Lightning Roulette ⚡"]
    }
    
    resultado = []
    for categoria, jogos in categorias.items():
        resultado.append(f"\n{categoria}")
        for jogo in jogos:
            resultado.append(f"• {jogo}")
    
    return "\n".join(resultado)

# --- COMANDOS PRINCIPAIS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    nome_usuario = user.first_name or "Amigo"
    
    nome_personalizado = random.choice(NOMES_HUMANIZADOS)
    saudacao = random.choice(SAUDACOES).format(nome=nome_personalizado)
    frase_motivacional = random.choice(FRASES_MOTIVACIONAIS)
    
    mensagem = f"""
{saudacao}

🎉 **Bem-vindo à revolução das apostas inteligentes!** 🎉

{frase_motivacional}

🤖 **Nosso sistema conta com 15 JOGOS DIFERENTES:**

{listar_jogos()}

💎 **O que você ganha aqui:**
✅ Sinais com IA avançada para 15 jogos
✅ Estratégias específicas para cada jogo  
✅ Horários otimizados de entrada
✅ Gestão de banca profissional
✅ Comunidade de +20.000 vencedores

**Pronto para começar a lucrar?**
"""
    
    keyboard = [
        [InlineKeyboardButton("🚀 QUERO LUCRAR AGORA!", callback_data="quero_lucrar")],
        [InlineKeyboardButton("🎮 VER TODOS OS JOGOS", callback_data="ver_jogos")],
        [InlineKeyboardButton("📊 VER PROVAS DE LUCRO", callback_data="ver_provas")],
        [InlineKeyboardButton("💎 OFERTA VIP ESPECIAL", callback_data="oferta_vip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    gif_celebracao = random.choice(GIFS_VITORIA)
    await context.bot.send_animation(
        chat_id=user_id,
        animation=gif_celebracao,
        caption=mensagem,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Registra usuário
    bd = context.bot_data
    inicializar_estatisticas(bd)
    bd['usuarios_unicos'].add(user_id)
    
    logger.info(f"Comando /start executado por {nome_usuario} ({user_id})")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Acesso negado.")
        return

    bd = context.bot_data
    inicializar_estatisticas(bd)
    
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    usuarios_unicos = len(bd.get('usuarios_unicos', set()))
    conversoes = bd.get('conversoes_vip', 0)
    taxa_conversao = (conversoes / max(usuarios_unicos, 1)) * 100
    
    stats_free = {
        'sinais': bd.get('sinais_free', 0),
        'wins': bd.get('win_primeira_free', 0) + bd.get('win_gale_free', 0),
        'loss': bd.get('loss_free', 0)
    }
    
    stats_vip = {
        'sinais': bd.get('sinais_vip', 0),
        'wins': bd.get('win_primeira_vip', 0) + bd.get('win_gale_vip', 0),
        'loss': bd.get('loss_vip', 0)
    }
    
    assertividade_free = (stats_free['wins'] / max(stats_free['sinais'], 1)) * 100
    assertividade_vip = (stats_vip['wins'] / max(stats_vip['sinais'], 1)) * 100
    
    mensagem = f"""
📊 **ESTATÍSTICAS - BOT V25.1**

⏰ **Sistema:**
• Uptime: {uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m
• Jogos: {len(JOGOS_COMPLETOS)}
• Usuários: {usuarios_unicos}
• Conversões VIP: {conversoes} ({taxa_conversao:.1f}%)

🆓 **Canal FREE:**
• Sinais: {stats_free['sinais']} | Wins: {stats_free['wins']} | Loss: {stats_free['loss']}
• Assertividade: {assertividade_free:.1f}%

💎 **Canal VIP:**
• Sinais: {stats_vip['sinais']} | Wins: {stats_vip['wins']} | Loss: {stats_vip['loss']}
• Assertividade: {assertividade_vip:.1f}%
"""
    
    await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)

async def sinal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Acesso negado.")
        return

    args = context.args
    if len(args) < 1:
        jogos_lista = "\n".join([f"• {jogo}" for jogo in JOGOS_COMPLETOS.keys()])
        await update.message.reply_text(
            f"❌ **Uso:** `/sinal <jogo> [canal] [confianca]`\n\n"
            f"**Jogos:**\n{jogos_lista}\n\n"
            f"**Exemplos:**\n"
            f"`/sinal tiger vip 0.8`\n"
            f"`/sinal aviator free 0.75`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    jogo_input = args[0].lower()
    canal = args[1] if len(args) > 1 else "free"
    confianca = float(args[2]) if len(args) > 2 and args[2].replace('.', '').isdigit() else 0.75

    jogo = get_jogo_por_palavra(jogo_input)
    if not jogo:
        await update.message.reply_text(f"❌ Jogo '{jogo_input}' não encontrado.")
        return

    canais = []
    if canal.lower() in ["free", "f"]:
        canais = [FREE_CANAL_ID]
    elif canal.lower() in ["vip", "v"]:
        canais = [VIP_CANAL_ID]
    elif canal.lower() in ["both", "b", "ambos"]:
        canais = [FREE_CANAL_ID, VIP_CANAL_ID]
    else:
        await update.message.reply_text("❌ Canal: free, vip ou both")
        return

    await update.message.reply_text(
        f"✅ **Sinal ativado!**\n\n"
        f"🎮 **Jogo:** {jogo}\n"
        f"📺 **Canal:** {canal}\n"
        f"⭐ **Confiança:** {confianca*100:.0f}%",
        parse_mode=ParseMode.MARKDOWN
    )

    await asyncio.sleep(3)

    for target_id in canais:
        await enviar_sinal_jogo(context, jogo, target_id, confianca)

# --- SISTEMA DE SINAIS ---
async def enviar_sinal_jogo(context: ContextTypes.DEFAULT_TYPE, jogo: str, target_id: int, confianca: float = 0.75):
    bd = context.bot_data
    inicializar_estatisticas(bd)
    channel_type = 'vip' if target_id == VIP_CANAL_ID else 'free'
    guard_key = f"sinal_{target_id}_{jogo}"

    if bd.get(guard_key, False):
        return

    bd[guard_key] = True
    
    try:
        dados_jogo = JOGOS_COMPLETOS.get(jogo, {})
        apostas = dados_jogo.get("apostas", ["Aposta Padrão"])
        assertividade = dados_jogo.get("assertividade", [70, 25, 5])
        frases_analise = dados_jogo.get("frases_analise", ["🤖 Analisando padrões..."])
        
        aposta_escolhida = random.choice(apostas)
        frase_analise = random.choice(frases_analise)
        
        # Análise
        gif_analise = random.choice(GIFS_ANALISE)
        await context.bot.send_animation(
            chat_id=target_id,
            animation=gif_analise,
            caption=frase_analise
        )
        
        await asyncio.sleep(random.randint(8, 15))
        
        # Sinal
        valor_entrada = 25.0 * (1 + (confianca - 0.5))
        estrelas = "⭐" * int(confianca * 5)
        nivel = "ALTÍSSIMA" if confianca > 0.8 else "ALTA" if confianca > 0.6 else "MÉDIA"
        
        mensagem_sinal = f"""
🔥 **SINAL CONFIRMADO | {jogo}** 🔥

🎯 **ENTRADA:** {aposta_escolhida}
💰 **Valor:** R$ {valor_entrada:.2f}
📊 **Confiança:** {estrelas} ({nivel})
⚡ **Gales:** Automáticos

🔗 **JOGAR:**
[**🚀 ACESSAR PLATAFORMA**]({URL_CADASTRO_DEPOSITO})
"""
        
        if target_id == VIP_CANA
L_ID:
            mensagem_sinal += f"\n\n**Atenção:** Este é um sinal exclusivo para membros VIP. A assertividade e frequência são maiores no nosso grupo principal."
        
        msg_sinal = await context.bot.send_message(
            chat_id=target_id,
            text=mensagem_sinal,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False
        )
        
        bd[f'sinais_{channel_type}'] = bd.get(f'sinais_{channel_type}', 0) + 1
        bd[f'daily_sinais_{channel_type}'] = bd.get(f'daily_sinais_{channel_type}', 0) + 1

        # Simulação de resultado
        await asyncio.sleep(random.randint(240, 480)) # 4 a 8 minutos
        
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=assertividade, k=1)[0]
        
        if resultado == "win_primeira":
            bd[f'win_primeira_{channel_type}'] = bd.get(f'win_primeira_{channel_type}', 0) + 1
            bd[f'daily_win_primeira_{channel_type}'] = bd.get(f'daily_win_primeira_{channel_type}', 0) + 1
            gif_resultado = random.choice(GIFS_VITORIA)
            texto_resultado = "✅✅✅ GREEN! ✅✅✅"
        elif resultado == "win_gale":
            bd[f'win_gale_{channel_type}'] = bd.get(f'win_gale_{channel_type}', 0) + 1
            bd[f'daily_win_gale_{channel_type}'] = bd.get(f'daily_win_gale_{channel_type}', 0) + 1
            gif_resultado = IMG_GALE
            texto_resultado = "✅✅ GREEN NO GALE 1 ✅✅"
        else: # loss
            bd[f'loss_{channel_type}'] = bd.get(f'loss_{channel_type}', 0) + 1
            bd[f'daily_loss_{channel_type}'] = bd.get(f'daily_loss_{channel_type}', 0) + 1
            gif_resultado = GIF_RED
            texto_resultado = "❌❌ RED! ❌❌"

        await context.bot.send_animation(
            chat_id=target_id,
            animation=gif_resultado,
            caption=texto_resultado,
            reply_to_message_id=msg_sinal.message_id
        )

    except Exception as e:
        logger.error(f"Erro ao enviar sinal para {jogo} em {target_id}: {e}")
    finally:
        bd[guard_key] = False
        await asyncio.sleep(120) # Cooldown de 2 minutos

# --- CALLBACK HANDLER ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.effective_user
    nome = user.first_name or "Amigo"
    data = query.data
    
    if data == "quero_lucrar":
        mensagem = f"""
🚀 **Perfeito, {nome}! Decisão certa!** 🚀

🤖 **NOSSA TECNOLOGIA:**
• IA analisa 15 jogos simultaneamente
• +100.000 dados processados por segundo
• Assertividade média de 78% no VIP
• Estratégias específicas por jogo

🏆 **COMUNIDADE VENCEDORA:**
• +20.000 membros ativos
• Resultados comprovados diariamente
• Suporte 24/7
• Networking com investidores

**Pronto para começar?**
"""
        
        keyboard = [
            [InlineKeyboardButton("💎 SIM! QUERO VIP", callback_data="acesso_vip")],
            [InlineKeyboardButton("🆓 SINAIS GRATUITOS", url=URL_TELEGRAM_FREE)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(caption=mensagem, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif data == "acesso_vip":
        vagas = random.randint(4, 9)
        tempo = random.choice(["2 horas", "3 horas", "4 horas"])
        
        mensagem = f"""
🚨 **OFERTA ESPECIAL, {nome}!** 🚨

🔥 **ACESSO VIP - 15 JOGOS**

✅ **VOCÊ GANHA:**
• Sinais ilimitados para 15 jogos
• Estratégias exclusivas
• Suporte prioritário 24/7
• Comunidade VIP

💰 **CONDIÇÃO SIMPLES:**
• Faça depósito (qualquer valor)
• Envie comprovante
• Acesso VIP instantâneo

⏰ **{vagas} vagas restantes!**
🕐 **Expira em {tempo}**
"""
        
        keyboard = [
            [InlineKeyboardButton("🚀 FAZER DEPÓSITO", url=URL_CADASTRO_DEPOSITO)],
            [InlineKeyboardButton("💬 SUPORTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace('@', '' )}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_animation(
            chat_id=query.message.chat_id,
            animation=random.choice(GIFS_VITORIA),
            caption=mensagem,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "ver_jogos":
        mensagem = f"""
🎮 **NOSSOS 15 JOGOS EXCLUSIVOS**

{listar_jogos()}

💡 **Cada jogo tem:**
• Estratégias específicas
• Horários otimizados
• Análise de IA personalizada

**No VIP você domina todos!**
"""
        
        keyboard = [
            [InlineKeyboardButton("💎 ACESSAR VIP", url=URL_CADASTRO_DEPOSITO)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(caption=mensagem, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# --- EVENTOS ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome = user.first_name or "Amigo"
    
    await update.message.reply_animation(
        animation=random.choice(GIFS_ANALISE),
        caption=f"✅ **Comprovante recebido, {nome}!**\n\nAnalisando... Aguarde que já libero seu VIP! 🚀"
    )
    
    await asyncio.sleep(45)
    
    mensagem = f"""
🎉 **ACESSO VIP LIBERADO, {nome}!** 🎉

🔗 **SEU LINK VIP:**
{URL_VIP_ACESSO}

🎮 **15 JOGOS LIBERADOS:**
{listar_jogos()}

🎁 **BENEFÍCIOS ATIVADOS:**
✅ Sinais ilimitados
✅ Estratégias exclusivas  
✅ Suporte prioritário
✅ Comunidade VIP

**Bem-vindo à elite!** 🏆
"""
    
    await context.bot.send_animation(
        chat_id=user.id,
        animation=random.choice(GIFS_VITORIA),
        caption=mensagem,
        parse_mode=ParseMode.MARKDOWN
    )
    
    bd = context.bot_data
    bd['conversoes_vip'] = bd.get('conversoes_vip', 0) + 1

# --- AGENDAMENTOS ---
async def enviar_sinal_automatico(context: ContextTypes.DEFAULT_TYPE):
    jogo = random.choice(list(JOGOS_COMPLETOS.keys()))
    confianca = random.uniform(0.7, 0.85)
    
    # FREE
    await enviar_sinal_jogo(context, jogo, FREE_CANAL_ID, confianca)
    
    # VIP (com confiança maior)
    await asyncio.sleep(1800)  # 30 min depois
    await enviar_sinal_jogo(context, jogo, VIP_CANAL_ID, min(confianca + 0.1, 0.9))

async def enviar_prova_social(context: ContextTypes.DEFAULT_TYPE):
    try:
        imagem = random.choice(PROVAS_SOCIAIS)
        jogo = random.choice(list(JOGOS_COMPLETOS.keys()))
        
        mensagens = [
            f"🔥 **MAIS UM GREEN!** 🔥\n\nMembro VIP lucrando no {jogo}! 💰\n\nE você? Vai ficar de fora?",
            f"💎 **RESULTADO VIP!** 💎\n\nMais uma vitória no {jogo}! 📈\n\nIsso é o poder da nossa IA!",
            f"🎯 **PRECISÃO TOTAL!** 🎯\n\nNossa análise do {jogo} foi perfeita! ✅\n\nResultados diários no VIP!"
        ]
        
        mensagem = random.choice(mensagens)
        vagas = random.randint(3, 8)
        
        mensagem_completa = f"""
{mensagem}

🚨 **{vagas} VAGAS VIP RESTANTES!**

👇 **GARANTIR AGORA** 👇
[**💎 ACESSAR VIP**]({URL_CADASTRO_DEPOSITO})
"""
        
        await context.bot.send_photo(
            chat_id=FREE_CANAL_ID,
            photo=imagem,
            caption=mensagem_completa,
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Erro prova social: {e}")

def configurar_agendamentos(app: Application):
    jq = app.job_queue
    
    # Sinais automáticos a cada 2 horas
    jq.run_repeating(enviar_sinal_automatico, interval=3600 * 2, first=300)
    
    # Provas sociais a cada 4 horas
    jq.run_repeating(enviar_prova_social, interval=3600 * 4, first=600)

# --- APLICAÇÃO PRINCIPAL ---
def build_application() -> Application:
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    # Comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("sinal", sinal_command))

    # Callbacks
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Eventos
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))

    # Agendamentos
    configurar_agendamentos(app)

    return app

def main():
    # Flask em thread separada
    if _FLASK_AVAILABLE:
        threading.Thread(target=start_flask, daemon=True).start()
        logger.info("Servidor Flask iniciado")

    # Bot
    app = build_application()
    logger.info("🚀 Bot Apostas Milionárias V25.1 iniciado!")
    logger.info(f"🎮 {len(JOGOS_COMPLETOS)} jogos disponíveis!")
    logger.info("💎 Sistema conversivo ativado!")
    
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
