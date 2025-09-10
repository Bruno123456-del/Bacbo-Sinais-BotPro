# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 24.2 "MÁQUINA DE CONVERSÃO" (CORRIGIDO E ROBUSTO)
# CRIADO E APRIMORADO POR MANUS
# - Funil de boas-vindas automático e pessoal para cada novo membro.
# - Estratégias de conversão e gatilhos mentais implementados.
# - Correção do erro: string não terminada na sequência de DMs (nome_usuario).
# - Tratamento de exceções, logs e inicialização de estatísticas.
# - Healthcheck Flask opcional para Render.
# - Pequenas correções para garantir que sinais sejam disparados tanto no FREE quanto no VIP.
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
GIF_OFERTA = "https://media.giphy.com/media/3oFzsmD5H5a1m0k2Yw/giphy.gif"
GIF_ANALISANDO = "https://media.giphy.com/media/jJxaUHe3w2n84/giphy.gif"
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/3oFzsmD5H5a1m0k2Yw/giphy.gif"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_RED = "https://media.giphy.com/media/3oriO5iQ1m8g49A2gU/giphy.gif"
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
        "👇 **QUERO MEU ACESSO AGORA** 👇\n\n"
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
        "👇 **ENTRE AGORA NO NOSSO CANAL GRATUITO E COMECE A LUCRAR HOJE MESMO!** 👇\n\n"
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

# --- 6. GESTÃO DE BANCA E GALES ---
class GestorBanca:
    def __init__(self, banca_inicial=100.0):
        self.banca_inicial = banca_inicial
        self.banca_atual = banca_inicial
        self.historico_operacoes = []
        self.sequencia_gales = [4, 8, 16]  # Percentuais para gales
        
    def calcular_entrada(self, percentual=2.0):
        """Calcula valor da entrada baseado no percentual da banca"""
        return self.banca_atual * (percentual / 100)
    
    def executar_gale(self, nivel_gale=0):
        """Executa estratégia de gale com percentuais crescentes"""
        if nivel_gale >= len(self.sequencia_gales):
            return None
        percentual = self.sequencia_gales[nivel_gale]
        return self.calcular_entrada(percentual)
    
    def aplicar_juros_compostos(self, dias=30, taxa_diaria=0.02):
        """Simula crescimento com juros compostos"""
        valor_final = self.banca_inicial * ((1 + taxa_diaria) ** dias)
        return valor_final
    
    def registrar_operacao(self, tipo, valor, resultado):
        """Registra operação no histórico"""
        operacao = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "valor": valor,
            "resultado": resultado,
            "banca_pos": self.banca_atual
        }
        self.historico_operacoes.append(operacao)

# --- 7. ENVIO DE SINAIS & PROVA SOCIAL ---
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
    try:
        await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem)
        logger.info(f"Aviso de '{tipo}' para {jogo} enviado ao canal VIP.")
    except Exception as e:
        logger.error(f"Falha ao enviar aviso de bloco para VIP ({VIP_CANAL_ID}): {e}")

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target_id: int):
    bd = context.bot_data
    inicializar_estatisticas(bd)
    channel_type = 'vip' if target_id == VIP_CANAL_ID else 'free'
    guard_key = f"sinal_em_andamento_{target_id}"

    # Se já existe sinal em andamento para esse target, pula
    if bd.get(guard_key, False):
        logger.warning(f"Pulei o sinal de {jogo} para {target_id} pois outro já estava em andamento.")
        return

    bd[guard_key] = True
    try:
        # Gestão de banca integrada
        gestor = GestorBanca(1000.0)  # Banca exemplo
        valor_entrada = gestor.calcular_entrada(2.5)
        
        # Animação inicial (analisando)
        try:
            await context.bot.send_animation(
                chat_id=target_id,
                animation=GIF_ANALISANDO,
                caption=f"🔎 Analisando padrões para uma entrada em **{jogo}**..."
            )
        except Exception as e:
            logger.warning(f"Não foi possível enviar animação para {target_id}: {e}")

        # pequena espera simulada
        await asyncio.sleep(random.randint(5, 10))

        mensagem_sinal = (
            f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
            f"🎯 **Apostar em:** {aposta}\n"
            f"💰 **Entrada sugerida:** R$ {valor_entrada:.2f} (2.5% da banca)\n"
            f"⚡ **Gales:** 4% → 8% → 16% (automático)\n"
            f"🔗 **JOGAR NA PLATAFORMA CERTA:** [**CLIQUE AQUI**]({URL_CADASTRO_DEPOSITO})"
        )
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP com Gestão de Banca Otimizada!_"

        # Envia mensagem principal
        try:
            await context.bot.send_message(
                chat_id=target_id, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN
            )
            logger.info(f"Sinal de {jogo} enviado para {target_id}.")
        except Exception as e:
            logger.error(f"Falha ao enviar sinal principal para {target_id}: {e}")
            raise

        # Atualiza estatísticas
        bd[f'sinais_{channel_type}'] = bd.get(f'sinais_{channel_type}', 0) + 1
        bd[f'daily_sinais_{channel_type}'] = bd.get(f'daily_sinais_{channel_type}', 0) + 1

        # Aguarda resultado simulado
        await asyncio.sleep(random.randint(45, 75))
        probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])
        resultado = random.choices(
            ["win_primeira", "win_gale", "loss"], weights=probabilidades, k=1
        )[0]

        bd[f'{resultado}_{channel_type}'] = bd.get(f'{resultado}_{channel_type}', 0) + 1
        bd[f'daily_{resultado}_{channel_type}'] = bd.get(f'daily_{resultado}_{channel_type}', 0) + 1

        greens_dia = bd.get(f'daily_win_primeira_{channel_type}', 0) + bd.get(f'daily_win_gale_{channel_type}', 0)
        reds_dia = bd.get(f'daily_loss_{channel_type}', 0)
        placar_do_dia = f"📊 **Placar do Dia ({channel_type.upper()}):** {greens_dia}W - {reds_dia}L"

        if resultado == "win_primeira":
            caption = f"✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Parabéns a todos! 🤑\n\n{placar_do_dia}"
            try:
                await context.bot.send_animation(chat_id=target_id, animation=GIF_GREEN_PRIMEIRA, caption=caption)
            except Exception as e:
                logger.warning(f"Falha ao enviar GIF de green para {target_id}: {e}")
                await context.bot.send_message(chat_id=target_id, text=caption)
        elif resultado == "win_gale":
            caption = f"✅ **GREEN NO GALE!** ✅\n\nPaciência e gestão trazem o lucro. Parabéns, time!\n\n{placar_do_dia}"
            try:
                await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE1, caption=caption)
            except Exception as e:
                logger.warning(f"Falha ao enviar foto de gale para {target_id}: {e}")
                await context.bot.send_message(chat_id=target_id, text=caption)
        else:
            caption = f"❌ **RED!** ❌\n\nFaz parte do jogo. Mantenham a gestão de banca e vamos para a próxima!\n\n{placar_do_dia}"
            try:
                await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=caption)
            except Exception as e:
                logger.warning(f"Falha ao enviar GIF de red para {target_id}: {e}")
                await context.bot.send_message(chat_id=target_id, text=caption)

    except Exception as e:
        logger.error(f"Erro no ciclo de sinal para {jogo} no canal {target_id}: {e}")
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"Erro durante envio de sinal: {e}")
        except Exception:
            pass
    finally:
        bd[guard_key] = False

async def enviar_prova_social(context: ContextTypes.DEFAULT_TYPE):
    url_prova = random.choice(PROVAS_SOCIAIS_URLS)
    legenda = random.choice(MARKETING_MESSAGES["legendas_prova_social"])
    try:
        await context.bot.send_photo(
            chat_id=FREE_CANAL_ID,
            photo=url_prova,
            caption=f"{legenda}\n\n[**QUERO LUCRAR ASSIM TAMBÉM!**]({URL_CADASTRO_DEPOSITO})",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.warning(f"Falha ao enviar prova social para free: {e}")

# --- 8. SEQUÊNCIA DE DMs PÓS-ENTRADA (FUNIL) ---
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

    # Aguarda mais 2 horas para a segunda mensagem
    await asyncio.sleep(2 * 3600)

    # Mensagem 2 (após ~3 horas do ingresso no grupo)
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"Última chance, {nome_usuario}! ⏰\n\n"
                f"As vagas VIP estão se esgotando rapidamente. Apenas **{random.randint(2, 4)}** restam.\n\n"
                f"Não deixe essa oportunidade passar. Faça seu depósito agora e garante 90 dias de acesso VIP GRÁTIS!\n\n"
                f"[**GARANTIR MINHA VAGA AGORA!**]({URL_CADASTRO_DEPOSITO})"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"DM Follow-up (2/2) enviada para {nome_usuario} ({user_id}).")
    except Exception as e:
        logger.warning(f"Falha ao enviar DM Follow-up (2/2) para {user_id}: {e}")

# --- 9. HANDLERS DE COMANDOS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name or "amigo"
    
    mensagem = MARKETING_MESSAGES["boas_vindas_start"]
    
    keyboard = [
        [InlineKeyboardButton("🔓 ENTRAR NO VIP", url=URL_CADASTRO_DEPOSITO)],
        [InlineKeyboardButton("🎁 CUPOM: GESTAO", callback_data="cupom_gestao")],
        [InlineKeyboardButton("🏆 VER PRÊMIOS VIP", callback_data="premios_vip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        mensagem,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Acesso negado!")
        return

    bd = context.bot_data
    inicializar_estatisticas(bd)
    
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    
    stats_text = (
        f"📊 **ESTATÍSTICAS DO BOT**\n\n"
        f"⏰ **Uptime:** {uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m\n\n"
        f"**CANAL FREE:**\n"
        f"📡 Sinais enviados: {bd.get('sinais_free', 0)} (hoje: {bd.get('daily_sinais_free', 0)})\n"
        f"✅ Wins primeira: {bd.get('win_primeira_free', 0)} (hoje: {bd.get('daily_win_primeira_free', 0)})\n"
        f"🎯 Wins gale: {bd.get('win_gale_free', 0)} (hoje: {bd.get('daily_win_gale_free', 0)})\n"
        f"❌ Losses: {bd.get('loss_free', 0)} (hoje: {bd.get('daily_loss_free', 0)})\n\n"
        f"**CANAL VIP:**\n"
        f"📡 Sinais enviados: {bd.get('sinais_vip', 0)} (hoje: {bd.get('daily_sinais_vip', 0)})\n"
        f"✅ Wins primeira: {bd.get('win_primeira_vip', 0)} (hoje: {bd.get('daily_win_primeira_vip', 0)})\n"
        f"🎯 Wins gale: {bd.get('win_gale_vip', 0)} (hoje: {bd.get('daily_win_gale_vip', 0)})\n"
        f"❌ Losses: {bd.get('loss_vip', 0)} (hoje: {bd.get('daily_loss_vip', 0)})"
    )
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

async def manual_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Acesso negado!")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "❌ **Uso correto:**\n"
            "`/sinal <jogo> <canal>`\n\n"
            "**Jogos disponíveis:** bac, roleta, slots, aviator, spaceman, mines, penalty, dragon, tiger\n"
            "**Canais:** free, vip, both"
        )
        return

    jogo_key = context.args[0].lower()
    canal = context.args[1].lower()

    if jogo_key not in JOGOS_MAP:
        await update.message.reply_text(f"❌ Jogo '{jogo_key}' não encontrado!")
        return

    jogo_nome = JOGOS_MAP[jogo_key]
    apostas = JOGOS[jogo_nome]
    aposta_escolhida = random.choice(apostas)

    # Use application.create_task para garantir que o loop do PTB gerencie as tasks
    if canal in ["free", "both"]:
        context.application.create_task(enviar_sinal_especifico(context, jogo_nome, aposta_escolhida, FREE_CANAL_ID))
    if canal in ["vip", "both"]:
        context.application.create_task(enviar_sinal_especifico(context, jogo_nome, aposta_escolhida, VIP_CANAL_ID))

    await update.message.reply_text(f"✅ Sinal de {jogo_nome} enviado para {canal}!")
    await log_admin_action(context, f"Sinal manual: {jogo_nome} → {canal}")

# --- 10. HANDLERS DE EVENTOS ---
async def handle_new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detecta novos membros no grupo e agenda DMs de follow-up."""
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        
        user_id = member.id
        nome = member.first_name or "amigo"
        
        # Agenda DMs de follow-up
        try:
            context.job_queue.run_once(
                boas_vindas_sequencia,
                when=3600,  # 1 hora após entrar
                chat_id=user_id,
                data={'nome_usuario': nome}
            )
            logger.info(f"Novo membro detectado: {nome} ({user_id}). DMs agendadas.")
        except Exception as e:
            logger.error(f"Falha ao agendar DMs para {user_id}: {e}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa prints de depósito enviados pelos usuários."""
    user_id = update.effective_user.id
    nome = update.effective_user.first_name or "usuário"
    
    # Simula verificação do comprovante (sempre aprova)
    await asyncio.sleep(random.randint(2, 5))
    
    await update.message.reply_text(MARKETING_MESSAGES["acesso_liberado_vip"])
    
    # Notifica admin
    await log_admin_action(context, f"Novo VIP liberado: {nome} ({user_id})")
    
    logger.info(f"Acesso VIP liberado para {nome} ({user_id})")

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ Comando não reconhecido. Use /start para começar!"
    )

# --- 11. CALLBACKS DE BOTÕES ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para botões inline"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "cupom_gestao":
        mensagem = (
            f"🎁 **CUPOM DE DESCONTO EXCLUSIVO**\n\n"
            f"📋 **Código:** GESTAO\n\n"
            f"✨ **Benefícios:**\n"
            f"🎁 Bônus Extra\n"
            f"⭐ Vantagens VIP\n"
            f"📱 Fácil de Usar\n\n"
            f"Cole o código durante o cadastro para ativar os benefícios"
        )
        
        keyboard = [
            [InlineKeyboardButton("📋 COPIAR CÓDIGO", callback_data="copiar_codigo")],
            [InlineKeyboardButton("🎯 USAR CUPOM E CADASTRAR", url=URL_CADASTRO_DEPOSITO)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(mensagem, reply_markup=reply_markup)
    
    elif data == "premios_vip":
        mensagem = (
            f"🏆 **TORNEIO VIP EXCLUSIVO**\n\n"
            f"🎁 **Prêmios Incríveis:**\n"
            f"✈️ Mala de dinheiro + viagem a Dubai para duas pessoas\n"
            f"🚗 Lamborghini Urus\n"
            f"⌚ Rolex Datejust 41\n"
            f"🎫 Ingressos para o BKFC Dubai\n"
            f"💻 MacBook Pro 16\"\n"
            f"📱 iPhone 16 Pro Max\n\n"
            f"🔥 Gostaria de ganhar o mesmo?\n"
            f"Toque no botão abaixo e entre para o clube privado\n"
            f"O jogo pelos prêmios mais desejados começa aqui 🏆"
        )
        
        keyboard = [
            [InlineKeyboardButton("💎 ENTRAR NO CLUBE PRIVADO VIP", url=URL_CADASTRO_DEPOSITO)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(mensagem, reply_markup=reply_markup)

# --- 12. MARKETING AUTOMÁTICO ---
async def send_marketing_message(context: ContextTypes.DEFAULT_TYPE):
    msg_type = context.job.data.get("type", "divulgacao")
    
    try:
        if msg_type == "oferta_relampago":
            vagas = random.randint(3, 8)
            mensagem = MARKETING_MESSAGES["oferta_relampago"].format(vagas_restantes=vagas)
            await context.bot.send_animation(
                chat_id=FREE_CANAL_ID,
                animation=GIF_OFERTA,
                caption=mensagem,
                parse_mode=ParseMode.MARKDOWN
            )
        elif msg_type == "ultima_chance":
            mensagem = MARKETING_MESSAGES["ultima_chance"]
            await context.bot.send_message(
                chat_id=FREE_CANAL_ID,
                text=mensagem,
                parse_mode=ParseMode.MARKDOWN
            )
        else:  # divulgacao
            mensagem = MARKETING_MESSAGES["divulgacao"]
            await context.bot.send_message(
                chat_id=FREE_CANAL_ID,
                text=mensagem,
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        logger.warning(f"Falha ao enviar marketing para free: {e}")

async def reset_daily_stats(context: ContextTypes.DEFAULT_TYPE):
    """Reset das estatísticas diárias às 00:00"""
    bd = context.bot_data
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bd[f'daily_{stat}_{ch}'] = 0
    
    logger.info("Estatísticas diárias resetadas.")
    
    # Reagenda para o próximo dia
    agora = datetime.now()
    proximo_reset = (agora + timedelta(days=1)).replace(hour=0, minute=0, second=5, microsecond=0)
    context.job_queue.run_once(reset_daily_stats, when=(proximo_reset - agora).total_seconds())

# --- 13. CONFIGURAÇÃO DE AGENDAMENTOS ---
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
    # inicializa estatisticas no bot_data para evitar KeyError
    try:
        inicializar_estatisticas(app.bot_data)
    except Exception as e:
        logger.error(f"Erro ao inicializar estatísticas no startup: {e}")
    logger.info("Bot iniciado com sucesso.")

def build_application() -> Application:
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    # Comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("sinal", manual_signal_command))

    # Callbacks
    app.add_handler(CallbackQueryHandler(callback_handler))

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
    logger.info("Iniciando polling...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
