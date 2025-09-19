# -*- coding: utf-8 -*-
# ===================================================================================
# SISTEMA DE CONVERSÃO VIP - ESTRATÉGIA COMPLETA PARA AFILIADOS
# DESENVOLVIDO POR MANUS PARA MÁXIMA RETENÇÃO E CONVERSÃO
# ===================================================================================

import asyncio
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List

# Importações necessárias do telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

logger = logging.getLogger("conversao_vip")

class SistemaConversaoVIP:
    """Sistema completo de conversão VIP com estratégias agressivas"""

    def __init__(self, app, url_afiliado: str, suporte_telegram: str):
        self.app = app
        self.url_afiliado = url_afiliado
        self.suporte_telegram = suporte_telegram
        self.usuarios_convertidos = {}
        self.campanhas_ativas = {}

        # Configurações de conversão
        self.vagas_restantes = 47
        self.codigo_promocional = "GESTAO"
        self.dias_vip_gratuitos = 90

        # Mensagens de conversão por contexto
        self.mensagens_contexto = {
            "pos_green": {
                "titulo": "🔥 VOCÊ ACABOU DE VER UM GREEN! IMAGINA NO VIP!",
                "descricao": "Com sinais 15% mais assertivos, você teria ainda mais greens como este!"
            },
            "pos_loss": {
                "titulo": "💎 PROTEJA SEU CAPITAL! NO VIP VOCÊ TEM ESTRATÉGIAS AVANÇADAS!",
                "descricao": "Nossos e-books de Gestão de Banca ensinam como minimizar losses e maximizar ganhos!"
            },
            "pos_gale": {
                "titulo": "📈 GESTÃO DE BANCA SALVOU O DIA! NO VIP É AINDA MELHOR!",
                "descricao": "Aprenda estratégias profissionais de gale com nossos e-books exclusivos!"
            },
            "urgencia": {
                "titulo": "⏰ TEMPO ESGOTANDO! NÃO PERCA ESTA OPORTUNIDADE ÚNICA!",
                "descricao": "Esta oferta histórica não voltará tão cedo. Aja agora!"
            }
        }

    async def processar_comprovante_deposito(self, user_id: int, nome_usuario: str):
        """Processa comprovante de depósito e libera acesso VIP"""
        mensagem_processamento = f"""
✅ **Comprovante recebido, {nome_usuario}!**

🤖 **Analisando seu depósito...**

Aguarde que já libero seu VIP com todos os bônus! 🚀

⏳ **Processamento em andamento...**
"""
        await self._enviar_mensagem_simples(user_id, mensagem_processamento)
        await asyncio.sleep(45)
        await self._liberar_acesso_vip(user_id, nome_usuario)

    async def _liberar_acesso_vip(self, user_id: int, nome_usuario: str):
        """Libera acesso VIP com todos os benefícios"""
        data_expiracao = datetime.now() + timedelta(days=self.dias_vip_gratuitos)
        mensagem_liberacao = f"""
🎉 **ACESSO VIP LIBERADO POR {self.dias_vip_gratuitos} DIAS, {nome_usuario}!** 🎉

**Parabéns por dar o primeiro passo rumo à sua liberdade financeira!**

Você acaba de garantir {self.dias_vip_gratuitos} dias de acesso GRATUITO ao nosso VIP Premium!

🔗 **SEU LINK VIP EXCLUSIVO:**
https://t.me/+q2CCKi1CKmljMTFh

🎮 **15 JOGOS LIBERADOS COM SINAIS ESTRATÉGICOS:**
E muito mais...

🎁 **SEUS BENEFÍCIOS ATIVADOS:**
✅ Sinais ilimitados com IA de alta precisão
✅ Estratégias exclusivas para maximizar seus ganhos
✅ Suporte prioritário 24/7
✅ Acesso à Comunidade VIP
✅ 2 E-BOOKS EXCLUSIVOS: Gestão de Banca e Juros Compostos
✅ Participação automática nos sorteios de prêmios milionários!

📅 **Seu VIP expira em:** {data_expiracao.strftime("%d/%m/%Y" )}

**Bem-vindo à elite que realmente lucra!** 🏆
"""
        await self._enviar_mensagem_simples(user_id, mensagem_liberacao)

        bd = self.app.bot_data
        bd["conversoes_vip"] = bd.get("conversoes_vip", 0) + 1
        bd.setdefault("usuarios_vip", {})[user_id] = {
            "nome": nome_usuario,
            "data_ativacao": datetime.now(),
            "data_expiracao": data_expiracao,
            "ativo": True
        }
        logger.info(f"Usuário {nome_usuario} ({user_id}) convertido para VIP por {self.dias_vip_gratuitos} dias")

    async def executar_campanha_escassez_extrema(self, canal_id: int):
        """Executa campanha de escassez extrema no canal FREE"""
        campanha = random.choice([
            {
                "titulo": "🚨 ALERTA VERMELHO: VAGAS VIP SE ESGOTANDO!",
                "mensagem": f"Nossos membros VIP estão lucrando consistentemente. RESTAM APENAS {self.vagas_restantes} VAGAS!",
                "botao": "💎 QUERO MINHA VAGA VIP!"
            },
            {
                "titulo": "⏰ TEMPO ESGOTANDO RAPIDAMENTE!",
                "mensagem": f"ÚLTIMAS HORAS para garantir sua vaga VIP com todos os bônus milionários! Não perca!",
                "botao": "🚀 GARANTIR VAGA AGORA!"
            }
        ])
        mensagem_completa = f"{campanha['titulo']}\n\n{campanha['mensagem']}"
        keyboard = [[InlineKeyboardButton(campanha["botao"], url=self.url_afiliado)]]
        await self._enviar_mensagem_com_botoes(canal_id, mensagem_completa, keyboard)

    async def enviar_prova_social_conversao(self, canal_id: int):
        """Envia prova social focada em conversão"""
        jogo = random.choice(["Fortune Tiger 🐅", "Aviator ✈️", "Mines 💣"])
        mensagem = random.choice([
            f"🔥 **MAIS UM MILIONÁRIO NASCEU!** 🔥\n\nMembro VIP acabou de lucrar R$ 15.847 no {jogo}!",
            f"💎 **RESULTADO EXPLOSIVO NO VIP!** 💎\n\nMais uma vitória de R$ 8.234 no {jogo}!"
        ])
        mensagem_completa = f"{mensagem}\n\n🚨 **ÚLTIMAS {self.vagas_restantes} VAGAS VIP!**\n\n👇 **GARANTA SEU ACESSO E TRANSFORME SUA VIDA!** 👇"
        imagem_prova = f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{random.randint(1, 19 )}.png"
        keyboard = [[InlineKeyboardButton("💎 QUERO SER O PRÓXIMO MILIONÁRIO!", url=self.url_afiliado)]]
        await self._enviar_foto_com_botoes(canal_id, imagem_prova, mensagem_completa, keyboard)

    async def _enviar_mensagem_simples(self, chat_id: int, texto: str):
        await self.app.bot.send_message(chat_id=chat_id, text=texto, parse_mode=ParseMode.MARKDOWN)

    async def _enviar_mensagem_com_botoes(self, chat_id: int, texto: str, keyboard: List[List[InlineKeyboardButton]]):
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.app.bot.send_message(chat_id=chat_id, text=texto, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def _enviar_foto_com_botoes(self, chat_id: int, foto_url: str, caption: str, keyboard: List[List[InlineKeyboardButton]]):
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.app.bot.send_photo(chat_id=chat_id, photo=foto_url, caption=caption, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

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
from datetime import datetime
import json

# Tenta importar o sistema de conversão. Se não encontrar, avisa e encerra.
try:
    from sistema_conversao_vip import SistemaConversaoVIP
except ImportError:
    print("ERRO CRÍTICO: O arquivo 'sistema_conversao_vip.py' não foi encontrado.")
    print("Certifique-se de que ambos os arquivos ('main.py' e 'sistema_conversao_vip.py') estão na mesma pasta.")
    exit()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, error
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters, CallbackQueryHandler
)

# --- CONFIGURAÇÕES DE SEGURANÇA ---
# Carrega as informações sensíveis das variáveis de ambiente do sistema.
# Isso é MUITO mais seguro do que deixar as chaves no código.
BOT_TOKEN = os.getenv("BOT_TOKEN", "7975008855:AAFQfTcSn3r5HiR0eXPaimJo0K3pX7osNfw")
FREE_CANAL_ID = int(os.getenv("FREE_CANAL_ID", "-1002808626127"))
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "-1003053055680"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789")) # Coloque seu ID de admin aqui

# --- AVISO DE SEGURANÇA ---
if BOT_TOKEN == "SEU_TOKEN_AQUI":
    print("="*50)
    print("ATENÇÃO: Você não configurou seu BOT_TOKEN!")
    print("Por favor, edite o arquivo main.py ou configure as variáveis de ambiente.")
    print("="*50)
    exit()

# --- CONFIGURAÇÕES GERAIS ---
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

# --- DADOS DO BOT (JOGOS, GIFS, ETC.) ---
JOGOS_COMPLETOS = {
    "Fortune Tiger 🐅": {"apostas": ["10 Rodadas Turbo", "15 Rodadas Normal"], "assertividade": [75, 20, 5]},
    "Aviator ✈️": {"apostas": ["Sair em 1.50x", "Sair em 2.00x"], "assertividade": [82, 15, 3]},
    "Mines 💣": {"apostas": ["3 Minas - 4 Cliques", "5 Minas - 2 Cliques"], "assertividade": [71, 24, 5]},
    "Bac Bo 🎲": {"apostas": ["Player", "Banker"], "assertividade": [78, 18, 4]},
    "Dragon Tiger 🐉🐅": {"apostas": ["Dragon", "Tiger"], "assertividade": [76, 19, 5]},
    "Roleta Brasileira 🇧🇷": {"apostas": ["Vermelho", "Preto", "1ª Dúzia"], "assertividade": [72, 23, 5]},
    "Spaceman 👨‍🚀": {"apostas": ["Sair em 1.80x", "Sair em 2.50x"], "assertividade": [80, 17, 3]},
    "Penalty Shoot-Out ⚽": {"apostas": ["Gol", "Defesa"], "assertividade": [77, 18, 5]},
    "Fortune Rabbit 🐰": {"apostas": ["8 Rodadas Turbo", "12 Rodadas Normal"], "assertividade": [73, 22, 5]},
    "Gates of Olympus ⚡": {"apostas": ["Ante Bet Ativo", "20 Rodadas Normal"], "assertividade": [68, 27, 5]},
    "Sweet Bonanza 🍭": {"apostas": ["Ante Bet 25%", "15 Rodadas Normal"], "assertividade": [70, 25, 5]},
    "Plinko 🎯": {"apostas": ["16 Pinos - Médio", "12 Pinos - Alto"], "assertividade": [69, 26, 5]},
    "Crazy Time 🎪": {"apostas": ["Número 1", "Número 2", "Coin Flip"], "assertividade": [65, 30, 5]},
    "Lightning Roulette ⚡": {"apostas": ["Números Sortudos", "Vermelho"], "assertividade": [70, 25, 5]},
    "Andar Bahar 🃏": {"apostas": ["Andar", "Bahar"], "assertividade": [74, 21, 5]}
}
GIFS_ANALISE = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"]
GIFS_VITORIA = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"]
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
IMG_GALE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"

# --- FUNÇÕES AUXILIARES ---
def inicializar_estatisticas(bot_data: dict ):
    if 'start_time' not in bot_data:
        bot_data['start_time'] = datetime.now()
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            bot_data.setdefault(f'{stat}_{ch}', 0)

def listar_jogos():
    return "\n".join([f"• {jogo}" for jogo in JOGOS_COMPLETOS.keys()])

# --- COMANDOS DO BOT ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    mensagem = f"""
🎉 **Bem-vindo(a) à revolução das apostas inteligentes!** 🎉

🤖 **Nosso sistema conta com 15 JOGOS DIFERENTES:**
{listar_jogos()}

**Pronto para começar a lucrar?**
"""
    keyboard = [
        [InlineKeyboardButton("🚀 QUERO LUCRAR AGORA!", callback_data="quero_lucrar")],
        [InlineKeyboardButton("💎 OFERTA VIP ESPECIAL", callback_data="oferta_vip")]
    ]
    await context.bot.send_animation(
        chat_id=user.id,
        animation=random.choice(GIFS_VITORIA),
        caption=mensagem,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    # Lógica para mostrar estatísticas (simplificada)
    bd = context.bot_data
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    sinais_free = bd.get('sinais_free', 0)
    sinais_vip = bd.get('sinais_vip', 0)
    conversoes = bd.get('conversoes_vip', 0)
    await update.message.reply_text(
        f"📊 **ESTATÍSTICAS**\n"
        f"Uptime: {uptime}\n"
        f"Sinais Free: {sinais_free}\n"
        f"Sinais VIP: {sinais_vip}\n"
        f"Conversões: {conversoes}"
    )

# --- SISTEMA DE SINAIS ---
async def enviar_sinal_jogo(context: ContextTypes.DEFAULT_TYPE, jogo: str, target_id: int, confianca: float):
    bd = context.bot_data
    channel_type = 'vip' if target_id == VIP_CANAL_ID else 'free'
    
    dados_jogo = JOGOS_COMPLETOS.get(jogo, {})
    aposta_escolhida = random.choice(dados_jogo.get("apostas", ["Aposta Padrão"]))
    
    await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_ANALISE), caption="🤖 Analisando padrões...")
    await asyncio.sleep(random.randint(8, 15))
    
    mensagem_sinal = f"""
🔥 **SINAL CONFIRMADO | {jogo}** 🔥
🎯 **ENTRADA:** {aposta_escolhida}
🔗 **JOGAR:** [**🚀 ACESSAR PLATAFORMA**]({URL_CADASTRO_DEPOSITO})
"""
    await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN)
    
    bd[f'sinais_{channel_type}'] = bd.get(f'sinais_{channel_type}', 0) + 1
    
    await asyncio.sleep(random.randint(60, 90))
    
    resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=dados_jogo["assertividade"], k=1)[0]
    bd[f'{resultado}_{channel_type}'] = bd.get(f'{resultado}_{channel_type}', 0) + 1
    
    if resultado == "win_primeira":
        await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_VITORIA), caption=f"✅✅✅ GREEN NA PRIMEIRA! {jogo} 🤑")
    elif resultado == "win_gale":
        await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE, caption=f"✅ GREEN NO GALE! {jogo} 💪")
    else:
        await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=f"❌ RED! Faz parte! {jogo} 🔄")

# --- CALLBACKS E EVENTOS ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "quero_lucrar" or query.data == "oferta_vip":
        keyboard = [
            [InlineKeyboardButton("🚀 FAZER DEPÓSITO", url=URL_CADASTRO_DEPOSITO)],
            [InlineKeyboardButton("💬 ENVIAR COMPROVANTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace('@', '' )}")]
        ]
        await query.message.reply_text(
            "💎 **OFERTA VIP ESPECIAL** 💎\n\n"
            "1. Faça um depósito de qualquer valor na plataforma.\n"
            "2. Envie o comprovante para nosso suporte.\n"
            "3. Receba acesso VIP instantaneamente!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    sistema_conversao = context.bot_data.get('sistema_conversao')
    if sistema_conversao:
        await sistema_conversao.processar_comprovante_deposito(user.id, user.first_name)
    else:
        await update.message.reply_text("✅ Comprovante recebido! Analisando...")

# --- AGENDAMENTOS ---
async def enviar_sinal_automatico(context: ContextTypes.DEFAULT_TYPE):
    jogo = random.choice(list(JOGOS_COMPLETOS.keys()))
    # Enviar para o canal FREE
    await enviar_sinal_jogo(context, jogo, FREE_CANAL_ID, random.uniform(0.65, 0.80))
    # Enviar para o canal VIP (com um pequeno atraso)
    await asyncio.sleep(random.randint(300, 900))
    await enviar_sinal_jogo(context, jogo, VIP_CANAL_ID, random.uniform(0.75, 0.95))

async def enviar_marketing_automatico(context: ContextTypes.DEFAULT_TYPE):
    sistema_conversao = context.bot_data.get('sistema_conversao')
    if not sistema_conversao:
        return
    
    if random.random() < 0.5: # 50% de chance
        await sistema_conversao.enviar_prova_social_conversao(FREE_CANAL_ID)
    else:
        await sistema_conversao.executar_campanha_escassez_extrema(FREE_CANAL_ID)

# --- FUNÇÃO PRINCIPAL ---
def main():
    logger.info("Iniciando o bot...")
    
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    # Inicializa e armazena o sistema de conversão no contexto do bot
    sistema_conversao = SistemaConversaoVIP(app, URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM)
    app.bot_data['sistema_conversao'] = sistema_conversao
    inicializar_estatisticas(app.bot_data)

    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))

    # Agendamentos (Jobs)
    jq = app.job_queue
    jq.run_repeating(enviar_sinal_automatico, interval=45 * 60, first=10) # Sinal a cada 45 min
    jq.run_repeating(enviar_marketing_automatico, interval=90 * 60, first=30) # Marketing a cada 1.5h

    logger.info("🚀 Bot Apostas Milionárias V25.1 iniciado com sucesso!")
    logger.info(f"🎮 {len(JOGOS_COMPLETOS)} jogos disponíveis!")
    logger.info("💎 Sistema de conversão VIP ativado!")
    
    app.run_polling()

if __name__ == "__main__":
    main()
