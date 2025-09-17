# -*- coding: utf-8 -*-
# ===================================================================================
# MAIN.PY - BOT DE SINAIS APOSTAS MILIONÁRIAS V27.0 - VERSÃO COMPLETA FINAL
# SISTEMA PROFISSIONAL COMPLETO DE CONVERSÃO PARA AFILIADOS
# DESENVOLVIDO POR MANUS COM MÁXIMA RETENÇÃO, CONVERSÃO E ESTRATÉGIAS AGRESSIVAS
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

# Importar sistemas personalizados
from sistema_conversao_vip import SistemaConversaoVIP

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
            "name": "Apostas-Milionarias-BotPro-V27.0-Completo", 
            "jogos": 15,
            "conversao": "maxima",
            "estrategias": "agressivas",
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
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger("bot_main")

# --- JOGOS E CONFIGURAÇÕES ESTRATÉGICAS ---
JOGOS_COMPLETOS = {
    "Fortune Tiger 🐅": {
        "apostas": ["10 Rodadas Turbo", "15 Rodadas Normal", "Aguardar Padrão Especial"],
        "assertividade": [75, 20, 5],
        "frases_analise": ["🐅 O tigrinho está rugindo de oportunidade...", "💰 Detectando padrão dourado no Tiger..."],
        "conversao_alta": True,
        "popularidade": 95
    },
    "Aviator ✈️": {
        "apostas": ["Sair em 1.50x", "Sair em 2.00x", "Dupla Aposta"],
        "assertividade": [82, 15, 3],
        "frases_analise": ["✈️ Calculando trajetória de voo perfeita...", "📈 Analisando histórico de multiplicadores..."],
        "conversao_alta": True,
        "popularidade": 90
    },
    "Mines 💣": {
        "apostas": ["3 Minas - 4 Cliques", "5 Minas - 2 Cliques", "Estratégia Segura"],
        "assertividade": [71, 24, 5],
        "frases_analise": ["💣 Mapeando campo minado com precisão...", "🗺️ Identificando zonas seguras..."],
        "conversao_alta": True,
        "popularidade": 85
    },
    "Bac Bo 🎲": {
        "apostas": ["Player", "Banker", "Tie (Empate)"],
        "assertividade": [78, 18, 4],
        "frases_analise": ["🎲 Analisando padrões das cartas no Bac Bo...", "📊 Processando histórico de empates..."],
        "conversao_alta": False,
        "popularidade": 70
    },
    "Dragon Tiger 🐉🐅": {
        "apostas": ["Dragon", "Tiger", "Tie (Empate)"],
        "assertividade": [76, 19, 5],
        "frases_analise": ["🐉 O dragão está se preparando para atacar...", "🐅 O tigre farejou uma oportunidade..."],
        "conversao_alta": False,
        "popularidade": 65
    },
    "Roleta Brasileira 🇧🇷": {
        "apostas": ["Vermelho", "Preto", "Par", "Ímpar", "1ª Dúzia"],
        "assertividade": [72, 23, 5],
        "frases_analise": ["🎡 Analisando padrões da roleta brasileira...", "🔴 Identificando sequências de cores..."],
        "conversao_alta": False,
        "popularidade": 75
    },
    "Spaceman 👨‍🚀": {
        "apostas": ["Sair em 1.80x", "Sair em 2.50x", "Estratégia Dupla"],
        "assertividade": [80, 17, 3],
        "frases_analise": ["👨‍🚀 Astronauta em missão espacial lucrativa...", "🚀 Calculando órbita perfeita..."],
        "conversao_alta": True,
        "popularidade": 80
    },
    "Penalty Shoot-Out ⚽": {
        "apostas": ["Gol", "Defesa", "Sequência de 3"],
        "assertividade": [77, 18, 5],
        "frases_analise": ["⚽ Analisando padrões de pênaltis...", "🥅 Estudando comportamento do goleiro..."],
        "conversao_alta": False,
        "popularidade": 60
    },
    "Fortune Rabbit 🐰": {
        "apostas": ["8 Rodadas Turbo", "12 Rodadas Normal", "Aguardar Coelho Dourado"],
        "assertividade": [73, 22, 5],
        "frases_analise": ["🐰 Coelhinho da sorte detectado...", "🥕 Padrão de cenouras identificado..."],
        "conversao_alta": False,
        "popularidade": 70
    },
    "Gates of Olympus ⚡": {
        "apostas": ["Ante Bet Ativo", "20 Rodadas Normal", "Aguardar Zeus"],
        "assertividade": [68, 27, 5],
        "frases_analise": ["⚡ Zeus está carregando seus poderes...", "🏛️ Portões do Olimpo se abrindo..."],
        "conversao_alta": False,
        "popularidade": 65
    },
    "Sweet Bonanza 🍭": {
        "apostas": ["Ante Bet 25%", "15 Rodadas Normal", "Aguardar Scatter"],
        "assertividade": [70, 25, 5],
        "frases_analise": ["🍭 Doces explosivos detectados...", "🍬 Padrão de multiplicadores formando..."],
        "conversao_alta": False,
        "popularidade": 68
    },
    "Plinko 🎯": {
        "apostas": ["16 Pinos - Médio", "12 Pinos - Alto", "Auto Drop"],
        "assertividade": [69, 26, 5],
        "frases_analise": ["🎯 Calculando trajetória da bolinha...", "📐 Analisando ângulos de queda..."],
        "conversao_alta": False,
        "popularidade": 55
    },
    "Crazy Time 🎪": {
        "apostas": ["Número 1", "Número 2", "Coin Flip", "Crazy Time"],
        "assertividade": [65, 30, 5],
        "frases_analise": ["🎪 Show maluco começando...", "🎡 Roda da fortuna girando..."],
        "conversao_alta": False,
        "popularidade": 60
    },
    "Lightning Roulette ⚡": {
        "apostas": ["Números Sortudos", "Vermelho", "Straight Up"],
        "assertividade": [70, 25, 5],
        "frases_analise": ["⚡ Raios de multiplicadores detectados...", "🎡 Roleta eletrificada ativada..."],
        "conversao_alta": False,
        "popularidade": 58
    },
    "Andar Bahar 🃏": {
        "apostas": ["Andar", "Bahar", "1st Card Joker"],
        "assertividade": [74, 21, 5],
        "frases_analise": ["🃏 Cartas indianas revelando segredos...", "🎴 Padrão tradicional identificado..."],
        "conversao_alta": False,
        "popularidade": 50
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
    for i in range(1, 20)
]

# Frases humanizadas e estratégicas
NOMES_HUMANIZADOS = ["Parceiro", "Amigo", "Guerreiro", "Campeão", "Vencedor", "Investidor", "Trader", "Craque"]
SAUDACOES = ["Olá, {nome}! 👋", "E aí, {nome}! 🔥", "Fala, {nome}! 💪", "Opa, {nome}! ⚡"]
FRASES_MOTIVACIONAIS = [
    "Hoje é o seu dia de sorte! 🍀",
    "A fortuna favorece os corajosos! 💪", 
    "Seus lucros estão chegando! 💰",
    "Prepare-se para lucrar! 🚀"
]

# Horários estratégicos para sinais
HORARIOS_FREE = [
    (9, 0), (11, 30), (14, 0), (16, 30), (19, 0), (21, 30)
]
HORARIOS_VIP = [
    (8, 30), (10, 45), (13, 15), (15, 45), (18, 30), (20, 45), (22, 15)
]

# Sistema de conversão VIP global
sistema_conversao = None

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
    bot_data.setdefault('usuarios_aquecidos', set())
    bot_data.setdefault('usuarios_vip', {})

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

def get_jogos_alta_conversao():
    """Retorna jogos com alta taxa de conversão"""
    return [jogo for jogo, dados in JOGOS_COMPLETOS.items() if dados.get("conversao_alta", False)]

def get_jogo_por_popularidade():
    """Retorna jogo baseado na popularidade"""
    jogos_ponderados = []
    for jogo, dados in JOGOS_COMPLETOS.items():
        popularidade = dados.get("popularidade", 50)
        jogos_ponderados.extend([jogo] * (popularidade // 10))
    
    return random.choice(jogos_ponderados)

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
        [InlineKeyboardButton("💎 OFERTA VIP ESPECIAL", callback_data="oferta_vip_especial")]
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
    
    # Registra usuário e inicia aquecimento
    bd = context.bot_data
    inicializar_estatisticas(bd)
    bd['usuarios_unicos'].add(user_id)
    
    # Agendar aquecimento do usuário via sistema de conversão
    if sistema_conversao:
        asyncio.create_task(sistema_conversao.processar_conversao_completa(user_id, nome_usuario, "urgencia"))
    
    logger.info(f"Comando /start executado por {nome_usuario} ({user_id})")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Acesso negado.")
        return

    bd = context.bot_data
    inicializar_estatisticas(bd)
    
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    
    # Estatísticas do sistema de conversão
    if sistema_conversao:
        stats_conversao = sistema_conversao.get_estatisticas_conversao()
    else:
        stats_conversao = {
            'usuarios_unicos': len(bd.get('usuarios_unicos', set())),
            'conversoes_total': bd.get('conversoes_vip', 0),
            'usuarios_vip_ativos': len([u for u in bd.get('usuarios_vip', {}).values() if u.get('ativo')]),
            'taxa_conversao': 0,
            'vagas_restantes': 47,
            'codigo_promocional': 'GESTAO'
        }
    
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
📊 **ESTATÍSTICAS - BOT V27.0 COMPLETO**

⏰ **Sistema:**
• Uptime: {uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m
• Jogos: {len(JOGOS_COMPLETOS)}
• Usuários: {stats_conversao['usuarios_unicos']}
• VIPs Ativos: {stats_conversao['usuarios_vip_ativos']}
• Conversões: {stats_conversao['conversoes_total']} ({stats_conversao['taxa_conversao']:.1f}%)

🆓 **Canal FREE:**
• Sinais: {stats_free['sinais']} | Wins: {stats_free['wins']} | Loss: {stats_free['loss']}
• Assertividade: {assertividade_free:.1f}%

💎 **Canal VIP:**
• Sinais: {stats_vip['sinais']} | Wins: {stats_vip['wins']} | Loss: {stats_vip['loss']}
• Assertividade: {assertividade_vip:.1f}%

🎯 **Conversão:**
• Vagas Restantes: {stats_conversao['vagas_restantes']}
• Código Ativo: {stats_conversao['codigo_promocional']}
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
        await enviar_sinal_estrategico_completo(context, jogo, target_id, confianca)

# --- SISTEMA DE SINAIS ESTRATÉGICO COMPLETO ---
async def enviar_sinal_estrategico_completo(context: ContextTypes.DEFAULT_TYPE, jogo: str, target_id: int, confianca: float = 0.75):
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
        
        # Mensagens de aquecimento estratégico mais agressivas
        mensagens_aquecimento = [
            "🔥 OPORTUNIDADE HISTÓRICA detectada! Esta é a chance que você esperava!",
            "⚡ PADRÃO EXPLOSIVO identificado! Os grandes fundos estão entrando AGORA!",
            "💎 SINAL DE ALTÍSSIMA PRECISÃO! Momento perfeito para multiplicar seu capital!",
            "🚀 JANELA DE OPORTUNIDADE DOURADA! Aproveite antes que os grandes players dominem!"
        ]
        
        mensagem_aquecimento = random.choice(mensagens_aquecimento)
        
        # Análise prévia com aquecimento
        await context.bot.send_animation(
            chat_id=target_id,
            animation=random.choice(GIFS_ANALISE),
            caption=f"🤖 **ANÁLISE ESTRATÉGICA EM ANDAMENTO** 🤖\n\n{mensagem_aquecimento}\n\n{frase_analise}\n\n⏳ **Processando 100.000+ dados por segundo...**"
        )
        
        await asyncio.sleep(random.randint(15, 25))
        
        # Ajustar confiança baseado no canal
        if channel_type == "vip":
            confianca = min(confianca + 0.12, 0.94)  # VIP tem mais confiança
            valor_entrada = random.uniform(75.0, 200.0)
        else:
            valor_entrada = random.uniform(25.0, 100.0)
        
        # Sinal principal
        estrelas = "⭐" * int(confianca * 5)
        nivel = "ALTÍSSIMA" if confianca > 0.8 else "ALTA" if confianca > 0.6 else "MÉDIA"
        
        if channel_type == "vip":
            mensagem_sinal = f"""
🔥 **SINAL VIP EXCLUSIVO | {jogo}** 🔥

🎯 **ENTRADA:** {aposta_escolhida}
💰 **Valor Sugerido:** R$ {valor_entrada:.2f}
📊 **Confiança:** {estrelas} ({nivel})
⚡ **Gales:** Automáticos (Estratégia Avançada dos Grandes Fundos)
🕐 **Tempo:** Entrar AGORA!

💎 **ACESSO VIP ATIVO - SINAIS ILIMITADOS**
🎁 **Bônus Ativo:** R$ 600 + Giros Grátis + E-books Exclusivos
📚 **Estratégia:** Aplicar Juros Compostos conforme e-book VIP

**Você está jogando como os grandes fundos de investimento!**
"""
            
            keyboard = [
                [InlineKeyboardButton(f"▶️ JOGAR {jogo} AGORA com R$600 de BÔNUS!", url=URL_CADASTRO_DEPOSITO)]
            ]
            
        else:
            mensagem_sinal = f"""
🔥 **SINAL CONFIRMADO | {jogo}** 🔥

🎯 **ENTRADA:** {aposta_escolhida}
💰 **Valor Sugerido:** R$ {valor_entrada:.2f}
📊 **Confiança:** {estrelas} ({nivel})
⚡ **Gales:** Automáticos
🕐 **Tempo:** Entrar AGORA!

🚨 **DIFERENÇA BRUTAL ENTRE FREE E VIP:**
• FREE: 1-2 sinais/dia, assertividade 65-75%
• VIP: Sinais ilimitados, assertividade 78-90%
• VIP: E-books de Juros Compostos (transforme R$ 100 em R$ 10.000!)
• VIP: Estratégias dos grandes fundos de investimento

💡 **IMAGINA se você tivesse acesso às estratégias que os milionários usam?**
"""
            
            keyboard = [
                [InlineKeyboardButton(f"▶️ JOGAR {jogo} AGORA com R$600 de BÔNUS!", url=URL_CADASTRO_DEPOSITO)],
                [InlineKeyboardButton("💎 UPGRADE VIP (Sinais Exclusivos + E-books + Prêmios)!", callback_data="upgrade_vip_urgente")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=target_id,
            text=mensagem_sinal,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

        bd[f'sinais_{channel_type}'] += 1
        logger.info(f"Sinal estratégico completo enviado para {channel_type} no jogo {jogo}")

        # Agendar resultado
        asyncio.create_task(processar_resultado_sinal_completo(context, target_id, jogo, confianca, channel_type))

    except Exception as e:
        logger.error(f"Erro ao enviar sinal estratégico completo para {channel_type} no jogo {jogo}: {e}")
    finally:
        bd[guard_key] = False

async def processar_resultado_sinal_completo(context: ContextTypes.DEFAULT_TYPE, canal_id: int, jogo: str, confianca: float, tipo_canal: str):
    """Processa o resultado do sinal com estratégias de conversão"""
    
    # Tempo de espera realista
    tempo_espera = random.randint(180, 480)  # 3 a 8 minutos
    await asyncio.sleep(tempo_espera)
    
    bd = context.bot_data
    sucesso = random.random() < confianca
    
    if sucesso:
        if random.random() < 0.78:  # 78% chance de green na primeira
            bd[f'win_primeira_{tipo_canal}'] += 1
            await enviar_resultado_green_primeira_completo(context, canal_id, jogo, tipo_canal)
        else:  # 22% chance de green no gale
            bd[f'win_gale_{tipo_canal}'] += 1
            await enviar_resultado_green_gale_completo(context, canal_id, jogo, tipo_canal)
    else:
        bd[f'loss_{tipo_canal}'] += 1
        await enviar_resultado_loss_estrategico_completo(context, canal_id, jogo, tipo_canal)

async def enviar_resultado_green_primeira_completo(context: ContextTypes.DEFAULT_TYPE, canal_id: int, jogo: str, tipo_canal: str):
    """Envia resultado green na primeira com máxima estratégia de conversão"""
    
    valores_lucro = [
        "R$ 847", "R$ 1.234", "R$ 2.156", "R$ 3.789", "R$ 1.567", "R$ 2.890"
    ]
    lucro = random.choice(valores_lucro)
    
    mensagem = f"""
✅ **GREEN NA PRIMEIRA! LUCRO DE {lucro} CONFIRMADO!** ✅

🎯 **{jogo}** - Sinal certeiro da nossa IA!
💰 **Resultado:** POSITIVO na primeira entrada!
📈 **Status:** LUCRO GARANTIDO!
🔥 **Mais uma vitória para nossa comunidade de vencedores!**

💡 **VOCÊ SABIA?** Este é exatamente o tipo de resultado que nossos e-books de Juros Compostos ensinam a maximizar!
"""
    
    if tipo_canal == "free":
        mensagem += f"""

💎 **IMAGINA NO VIP COM ESTRATÉGIAS AVANÇADAS:**
• Sinais com 15% mais assertividade
• E-books que ensinam como transformar {lucro} em R$ 10.000+
• Estratégias de juros compostos dos grandes fundos
• Acesso aos prêmios milionários (Lamborghini, Rolex, Dubai)

**Einstein disse: "Os juros compostos são a oitava maravilha do mundo!"**

👇 **MULTIPLIQUE SEUS RESULTADOS COM VIP!** 👇
"""
        keyboard = [
            [InlineKeyboardButton("💎 QUERO VIP (Mais Assertividade + E-books + Prêmios)!", callback_data="upgrade_vip_pos_green")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_animation(
            chat_id=canal_id,
            animation=random.choice(GIFS_VITORIA),
            caption=mensagem,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Trigger conversão via sistema
        if sistema_conversao and canal_id == FREE_CANAL_ID:
            # Aguardar um pouco e enviar campanha de conversão
            await asyncio.sleep(300)  # 5 minutos
            await sistema_conversao.executar_campanha_escassez_extrema(canal_id)
            
    else:
        await context.bot.send_animation(
            chat_id=canal_id,
            animation=random.choice(GIFS_VITORIA),
            caption=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )

async def enviar_resultado_green_gale_completo(context: ContextTypes.DEFAULT_TYPE, canal_id: int, jogo: str, tipo_canal: str):
    """Envia resultado green no gale com estratégia de conversão"""
    
    mensagem = f"""
✅ **GREEN NO GALE! RECUPERAÇÃO E LUCRO GARANTIDO!** ✅

🎯 **{jogo}** - Estratégia de gale funcionou perfeitamente!
💰 **Resultado:** POSITIVO no gale!
📈 **Status:** LUCRO GARANTIDO!

💡 **A gestão de banca é FUNDAMENTAL! Mais uma prova de que nossa estratégia funciona!**

🧠 **CURIOSIDADE:** Esta é exatamente a situação que nossos e-books de Gestão de Banca ensinam a dominar!
"""
    
    if tipo_canal == "free":
        mensagem += f"""

💎 **NO VIP VOCÊ TERIA ACESSO A:**
• E-books exclusivos de Gestão de Banca Inteligente
• Estratégias de Juros Compostos para maximizar gales
• Técnicas que os grandes fundos usam para proteger capital
• Sinais com maior assertividade para menos gales

**Aprenda como os milionários transformam até mesmo gales em oportunidades de crescimento exponencial!**

👇 **DOMINE A GESTÃO PROFISSIONAL COM VIP!** 👇
"""
        keyboard = [
            [InlineKeyboardButton("💎 QUERO GESTÃO PROFISSIONAL (VIP + E-books + Prêmios)!", callback_data="upgrade_vip_pos_gale")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_photo(
            chat_id=canal_id,
            photo=IMG_GALE,
            caption=mensagem,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await context.bot.send_photo(
            chat_id=canal_id,
            photo=IMG_GALE,
            caption=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )

async def enviar_resultado_loss_estrategico_completo(context: ContextTypes.DEFAULT_TYPE, canal_id: int, jogo: str, tipo_canal: str):
    """Envia resultado loss de forma estratégica para conversão máxima"""
    
    mensagem = f"""
❌ **LOSS - Faz parte da estratégia dos grandes investidores!** ❌

🎯 **{jogo}** - Resultado negativo
📊 **Análise:** Mercado imprevisível neste momento
💡 **LEMBRETE IMPORTANTE:** Nem todo sinal é green, mas a consistência e a gestão de banca nos levam ao lucro!

🔥 **PRÓXIMO SINAL EM BREVE!**

🧠 **VOCÊ SABIA?** Warren Buffett teve losses, mas aplicou estratégias de recuperação que o tornaram bilionário!
"""
    
    if tipo_canal == "free":
        mensagem += f"""

💎 **NO VIP VOCÊ TERIA PROTEÇÃO MÁXIMA:**
• Estratégias avançadas de recuperação de losses
• E-books que ensinam como transformar losses em oportunidades
• Sinais com 15% mais assertividade para minimizar perdas
• Técnicas de juros compostos para recuperação exponencial

**Os grandes fundos não evitam losses, eles os transformam em trampolins para lucros maiores!**

**Aprenda no nosso e-book "Juros Compostos nas Apostas" como recuperar e multiplicar após um loss!**

👇 **PROTEJA E MULTIPLIQUE SEU CAPITAL COM VIP!** 👇
"""
        keyboard = [
            [InlineKeyboardButton("💎 QUERO PROTEÇÃO VIP (Menos Losses + Recuperação + E-books)!", callback_data="upgrade_vip_pos_loss")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_animation(
            chat_id=canal_id,
            animation=GIF_RED,
            caption=mensagem,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Trigger conversão agressiva após loss
        if sistema_conversao and canal_id == FREE_CANAL_ID:
            await asyncio.sleep(180)  # 3 minutos
            await sistema_conversao.executar_campanha_escassez_extrema(canal_id)
            
    else:
        await context.bot.send_animation(
            chat_id=canal_id,
            animation=GIF_RED,
            caption=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )

# --- CALLBACKS ESTRATÉGICOS COMPLETOS ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    nome = user.first_name or "Amigo"
    data = query.data
    
    # Processar via sistema de conversão
    if sistema_conversao and data.startswith("upgrade_vip") or data in ["oferta_vip_especial", "quero_lucrar"]:
        contexto_map = {
            "upgrade_vip_pos_green": "pos_green",
            "upgrade_vip_pos_gale": "pos_gale", 
            "upgrade_vip_pos_loss": "pos_loss",
            "upgrade_vip_urgente": "urgencia",
            "oferta_vip_especial": "urgencia",
            "quero_lucrar": "urgencia"
        }
        
        contexto = contexto_map.get(data, "urgencia")
        await sistema_conversao.processar_conversao_completa(user.id, nome, contexto)
        return
    
    # Outros callbacks
    if data == "ver_jogos":
        mensagem = f"""
🎮 **NOSSOS 15 JOGOS EXCLUSIVOS COM SINAIS DE ALTA ASSERTIVIDADE**

{listar_jogos()}

💡 **Em cada jogo, você encontra:**
• Estratégias específicas validadas pelos melhores traders do mundo
• Horários otimizados baseados em análise de Big Data
• IA personalizada para maximizar seus ganhos
• Gestão de banca profissional dos grandes fundos

**No VIP, você não apenas joga, você DOMINA o mercado como os bilionários!**

🎁 **BÔNUS EXCLUSIVO:** Acesso aos e-books de Gestão de Banca e Juros Compostos que podem transformar sua vida financeira!

**Einstein disse: "Os juros compostos são a oitava maravilha do mundo!" - Aprenda este segredo no VIP!**
"""
        
        keyboard = [
            [InlineKeyboardButton("💎 QUERO DOMINAR COMO OS BILIONÁRIOS (VIP + E-BOOKS)!", callback_data="oferta_vip_especial")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(caption=mensagem, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    elif data == "ver_provas":
        # Seção de provas de lucro com ofertas de luxo
        mensagem_provas = f"""
✨ **VEJA QUEM JÁ ESTÁ LUCRANDO ALTO COM NOSSO VIP!** ✨

**Maldivas, Rolex, Lamborghini 💙**
Não é só para herdeiros — mas também para participantes do torneio VIP!

**Olha o que os jogadores ganharam da última vez:**

💰 Mala de dinheiro + viagem a Dubai para duas pessoas
🏎️ Lamborghini Urus
⌚ Rolex Datejust 41
🥊 Ingressos para o BKFC Dubai
💻 MacBook Pro 16"
📱 iPhone 16 Pro Max

**E o melhor: eles aprenderam a MULTIPLICAR esses ganhos usando as estratégias de Juros Compostos dos nossos e-books exclusivos!**

**Gostaria de ganhar o mesmo E aprender como os milionários multiplicam seu patrimônio?**

**"Somos feitos das oportunidades que tivemos e das escolhas que fizemos. Essa é a sua chance de lucrar como os grandes fundos fazem."**

👇 **Toque no botão abaixo e entre para o clube privado dos milionários.**
**O jogo pelos prêmios mais desejados começa aqui 🏆**
"""
        keyboard = [
            [InlineKeyboardButton("💎 QUERO MEU ACESSO VIP E PRÊMIOS MILIONÁRIOS!", callback_data="oferta_vip_especial")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Enviar uma prova social aleatória junto com a mensagem
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=random.choice(PROVAS_SOCIAIS),
            caption=mensagem_provas,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

# --- EVENTOS ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome = user.first_name or "Amigo"
    
    # Processar via sistema de conversão
    if sistema_conversao:
        await sistema_conversao.processar_comprovante_deposito(user.id, nome)
    else:
        # Fallback para o sistema original
        await update.message.reply_animation(
            animation=random.choice(GIFS_ANALISE),
            caption=f"✅ **Comprovante recebido, {nome}!**\n\nAnalisando... Aguarde que já libero seu VIP com todos os bônus! 🚀"
        )
        
        await asyncio.sleep(45)
        
        # Liberar VIP (versão simplificada)
        bd = context.bot_data
        bd['conversoes_vip'] = bd.get('conversoes_vip', 0) + 1

# --- AGENDAMENTOS ESTRATÉGICOS COMPLETOS ---
async def enviar_sinal_automatico_estrategico_completo(context: ContextTypes.DEFAULT_TYPE):
    """Envia sinais automáticos com estratégia completa"""
    
    # Escolher jogo baseado na popularidade para FREE
    jogo_free = get_jogo_por_popularidade()
    confianca_free = random.uniform(0.65, 0.78)
    
    # Enviar para FREE primeiro
    await enviar_sinal_estrategico_completo(context, jogo_free, FREE_CANAL_ID, confianca_free)
    
    # Esperar tempo estratégico (20-40 minutos)
    tempo_espera = random.randint(1200, 2400)
    await asyncio.sleep(tempo_espera)
    
    # Escolher jogo para VIP (preferencialmente de alta conversão)
    jogos_vip = get_jogos_alta_conversao()
    if random.random() < 0.7:  # 70% chance de usar jogo de alta conversão
        jogo_vip = random.choice(jogos_vip)
    else:
        jogo_vip = get_jogo_por_popularidade()
    
    confianca_vip = random.uniform(0.78, 0.92)
    
    # Enviar para VIP
    await enviar_sinal_estrategico_completo(context, jogo_vip, VIP_CANAL_ID, confianca_vip)

async def executar_campanha_conversao_mega_agressiva(context: ContextTypes.DEFAULT_TYPE):
    """Executa campanha mega agressiva de conversão"""
    
    if sistema_conversao:
        await sistema_conversao.executar_campanha_escassez_extrema(FREE_CANAL_ID)
        
        # Aguardar e enviar prova social
        await asyncio.sleep(1800)  # 30 minutos
        await sistema_conversao.enviar_prova_social_conversao(FREE_CANAL_ID)

def configurar_agendamentos_completos(app: Application):
    """Configura agendamentos com estratégia completa de conversão"""
    jq = app.job_queue
    
    # Sinais automáticos estratégicos a cada 1.5 horas
    jq.run_repeating(enviar_sinal_automatico_estrategico_completo, interval=3600 * 1.5, first=300)
    
    # Campanhas de conversão mega agressiva a cada 2.5 horas
    jq.run_repeating(executar_campanha_conversao_mega_agressiva, interval=3600 * 2.5, first=900)
    
    # Verificação de VIPs ativos a cada 6 horas
    if sistema_conversao:
        jq.run_repeating(sistema_conversao.verificar_usuarios_vip_ativos, interval=3600 * 6, first=1800)

# --- APLICAÇÃO PRINCIPAL ---
def build_application() -> Application:
    global sistema_conversao
    
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    # Inicializar sistema de conversão
    sistema_conversao = SistemaConversaoVIP(app, URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM)

    # Comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("sinal", sinal_command))

    # Callbacks
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Eventos
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))

    # Agendamentos estratégicos completos
    configurar_agendamentos_completos(app)

    return app

def main():
    # Flask em thread separada
    if _FLASK_AVAILABLE:
        threading.Thread(target=start_flask, daemon=True).start()
        logger.info("Servidor Flask iniciado")

    # Bot
    app = build_application()
    logger.info("🚀 Bot Apostas Milionárias V27.0 COMPLETO iniciado!")
    logger.info(f"🎮 {len(JOGOS_COMPLETOS)} jogos disponíveis!")
    logger.info("💎 Sistema de conversão MEGA AGRESSIVA ativado!")
    logger.info("📈 Foco MÁXIMO em juros compostos e gestão de banca!")
    logger.info("🏆 Estratégias dos grandes fundos implementadas!")
    
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
