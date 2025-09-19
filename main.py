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
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# --- CONFIGURAÇÕES GERAIS ---
URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
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
    bd = context.bot_data
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    sinais_vip = bd.get('sinais_vip', 0)
    conversoes = bd.get('conversoes_vip', 0)
    greens_vip = bd.get('win_primeira_vip', 0) + bd.get('win_gale_vip', 0)
    reds_vip = bd.get('loss_vip', 0)
    await update.message.reply_text(
        f"📊 **ESTATÍSTICAS VIP**\n"
        f"Uptime: {uptime}\n"
        f"Sinais VIP: {sinais_vip}\n"
        f"Greens: {greens_vip} | Reds: {reds_vip}\n"
        f"Conversões: {conversoes}"
    )

# --- LÓGICA DE SINAIS (NOVA ESTRATÉGIA) ---
async def enviar_sinal_jogo(context: ContextTypes.DEFAULT_TYPE, jogo: str, target_id: int, confianca: float):
    """
    Envia sinais de forma estratégica.
    - VIP: Envia o sinal completo para jogar.
    - FREE: Envia um "Sinal Fantasma" para gerar desejo e urgência.
    """
    bd = context.bot_data
    dados_jogo = JOGOS_COMPLETOS.get(jogo, {})
    aposta_escolhida = random.choice(dados_jogo.get("apostas", ["Aposta Padrão"]))

    if target_id == VIP_CANAL_ID:
        channel_type = 'vip'
        logger.info(f"Enviando sinal VIP completo para o jogo {jogo}.")
        await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_ANALISE), caption=f"🤖 Analisando padrões no {jogo}...")
        await asyncio.sleep(random.randint(8, 12))
        mensagem_sinal = f"💎 **SINAL VIP CONFIRMADO | {jogo}** 💎\n\n🎯 **ENTRADA:** {aposta_escolhida}\n🔥 **Confiança:** {'⭐' * int(confianca * 5)} (ALTÍSSIMA)\n\n🔗 **JOGAR AGORA:**\n[**>> CLIQUE AQUI PARA ACESSAR A PLATAFORMA <<**]({URL_CADASTRO_DEPOSITO})"
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
        total_sinais_vip = greens_vip + reds_vip
        assertividade_vip = (greens_vip / max(total_sinais_vip, 1)) * 100
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
# ===================================================================================
# SUBSTITUA A FUNÇÃO callback_handler ANTIGA EM main.py POR ESTA
# ===================================================================================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "quero_lucrar" or query.data == "oferta_vip":
        vagas_restantes = random.randint(5, 15) # Gera escassez dinâmica
        mensagem = f"""
🚨 **OFERTA HISTÓRICA LIBERADA PARA VOCÊ, {user.first_name}!** 🚨

Você viu o potencial. Agora é a sua hora de agir e entrar para o time que realmente lucra.

🔥 **Use o Código Promocional: `GESTAO`** 🔥

Ao fazer seu primeiro depósito de QUALQUER VALOR usando nosso link, você desbloqueia AGORA:

💰 **BÔNUS DE ATÉ R$ 600,00**
A plataforma dobra seu primeiro depósito, te dando mais caixa para aplicar nossas estratégias.

💎 **90 DIAS DE ACESSO VIP GRÁTIS**
Acesso total aos nossos sinais de altíssima assertividade, 24h por dia.

📚 **E-BOOK "JUROS COMPOSTOS NAS APOSTAS"**
O segredo dos milionários. Aprenda a transformar R$100 em R$10.000 com gestão e matemática.

🏆 **SORTEIOS MILIONÁRIOS**
Você concorre automaticamente a: Lamborghini, Rolex, Viagens para Dubai e Maldivas, e muito mais!

⚠️ **ATENÇÃO: RESTAM APENAS {vagas_restantes} VAGAS NESTA CONDIÇÃO!**

Este é o empurrão que você precisava. A decisão que separa os que olham dos que lucram.

**Passo 1:** Clique no botão abaixo e faça seu cadastro.
**Passo 2:** Use o código **GESTAO** e faça seu primeiro depósito.
**Passo 3:** Envie o comprovante para nosso suporte para liberação imediata.
"""
        keyboard = [
            [InlineKeyboardButton("🚀 ATIVAR OFERTA E USAR CÓDIGO 'GESTAO'", url=URL_CADASTRO_DEPOSITO)],
            [InlineKeyboardButton("💬 ENVIAR COMPROVANTE (SUPORTE 24/7)", url=f"https://t.me/{SUPORTE_TELEGRAM.replace('@', '' )}")]
        ]
        # Envia a mensagem no privado do usuário que clicou no botão
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
    """
    Agenda a nova estratégia de sinais:
    1. Envia o sinal real para o VIP.
    2. Envia o "Sinal Fantasma" para o FREE para criar desejo.
    """
    jogo = random.choice(list(JOGOS_COMPLETOS.keys()))
    confianca_vip = random.uniform(0.85, 0.98)
    await enviar_sinal_jogo(context, jogo, VIP_CANAL_ID, confianca_vip)
    await asyncio.sleep(random.randint(15, 45))
    await enviar_sinal_jogo(context, jogo, FREE_CANAL_ID, confianca_vip)

# ===================================================================================
# SUBSTITUA A FUNÇÃO enviar_marketing_automatico ANTIGA EM main.py POR ESTA
# ===================================================================================
async def enviar_marketing_automatico(context: ContextTypes.DEFAULT_TYPE):
    """
    Envia campanhas de marketing poderosas e variadas no canal gratuito.
    """
    sistema_conversao = context.bot_data.get('sistema_conversao')
    if not sistema_conversao:
        return

    # Sorteia qual tipo de campanha enviar para manter o canal dinâmico
    tipo_campanha = random.choice(["juros_compostos", "escassez_extrema", "prova_social"])

    if tipo_campanha == "juros_compostos":
        logger.info("Enviando campanha de marketing: Juros Compostos.")
        vagas = random.randint(4, 12)
        mensagem = f"""
🧠 **O SEGREDO QUE OS MILIONÁRIOS NÃO TE CONTAM...**

Einstein disse: "Juros compostos são a oitava maravilha do mundo".

Imagine transformar R$100 em R$10.000. Parece impossível? Não com matemática.

No nosso E-book exclusivo VIP, "Juros Compostos nas Apostas", ensinamos o método exato.

**Exemplo real de um membro VIP:**
- Semana 1: R$100 -> R$250
- Semana 2: R$250 -> R$625
- Semana 3: R$625 -> R$1.560
- Semana 4: R$1.560 -> R$3.900

Isso não é sorte. É estratégia. E está esperando por você no VIP.

🚨 **LIBERAMOS MAIS {vagas} VAGAS PARA A OFERTA DE 90 DIAS GRÁTIS + BÔNUS DE R$600!**
"""
        keyboard = [[InlineKeyboardButton("📈 QUERO APRENDER O SEGREDO DOS JUROS COMPOSTOS", callback_data="oferta_vip")]]
        await context.bot.send_message(FREE_CANAL_ID, mensagem, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

    elif tipo_campanha == "escassez_extrema":
        logger.info("Enviando campanha de marketing: Escassez Extrema.")
        horas = random.randint(2, 4)
        mensagem = f"""
🔥🔥 **ÚLTIMA CHAMADA - TUDO OU NADA!** 🔥🔥

A diretoria vai **ENCERRAR A OFERTA** de 90 dias VIP grátis + Bônus de R$600 nas próximas **{horas} HORAS**!

Depois disso, o acesso VIP será apenas para convidados e com valor muito superior.

Você tem duas escolhas:
1. Continuar olhando os outros lucrarem.
2. Agir agora, garantir sua vaga e ter a chance de concorrer a uma Lamborghini, Rolex e viagens de luxo.

A decisão é sua. O tempo está correndo. ⏳
"""
        keyboard = [[InlineKeyboardButton(f"⚡️ EU QUERO! ÚLTIMA CHANCE (EXPIRA EM {horas}H)", callback_data="oferta_vip")]]
        await context.bot.send_message(FREE_CANAL_ID, mensagem, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

    else: # prova_social
        logger.info("Enviando campanha de marketing: Prova Social.")
        await sistema_conversao.enviar_prova_social_conversao(FREE_CANAL_ID)


# --- FUNÇÃO PRINCIPAL ---
def main():
    logger.info("Iniciando o bot...")
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    sistema_conversao = SistemaConversaoVIP(app, URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM)
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
