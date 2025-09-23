# -*- coding: utf-8 -*-
# ===================================================================================
# MAIN.PY - BOT DE SINAIS APOSTAS MILIONÁRIAS V27.3 (PERSONALIDADE JÚNIOR MOREIRA)
# ARQUIVO PRINCIPAL PARA EXECUÇÃO DO BOT - VERSÃO FINAL COM MARKETING REATIVADO
# CRIADO E APRIMORADO POR MANUS
# ===================================================================================

import os
import logging
import random
import asyncio
from datetime import datetime

try:
    from sistema_conversao_vip import SistemaConversaoVIP
except ImportError:
    print("ERRO CRÍTICO: O arquivo 'sistema_conversao_vip.py' não foi encontrado.")
    exit()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import Conflict, BadRequest
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PicklePersistence,
    MessageHandler, filters, CallbackQueryHandler
)

# --- CONFIGURAÇÕES DE SEGURANÇA ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("ERRO CRÍTICO: A variável de ambiente BOT_TOKEN não foi encontrada ou está vazia.")
    exit()

FREE_CANAL_ID = int(os.getenv("FREE_CANAL_ID", "-1002808626127"))
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "-1003053055680"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "5011424031"))

# --- CONFIGURAÇÕES GERAIS ---
URL_CADASTRO_DEPOSITO = "https://lkwn.cc/f1c1c45a"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
URL_VIP_ACESSO = "https://t.me/+q2CCKi1CKmljMTFh"
SUPORTE_TELEGRAM = "@Superfinds_bot"

# --- CONFIGURAÇÃO DE LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime )s - %(name)s - %(levelname)s - %(message)s",
    style='%'
)
logging.getLogger("httpx" ).setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logger = logging.getLogger("bot_main")

# --- DADOS DO BOT ---
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
GIFS_VITORIA = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"]
GIFS_ANALISE = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"]
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
IMG_GALE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"

# --- FUNÇÕES AUXILIARES E DE ERRO ---
def inicializar_estatisticas(bot_data: dict ):
    logger.info("Inicializando/Verificando estatísticas...")
    bot_data.setdefault('start_time', datetime.now())
    bot_data.setdefault('usuarios_unicos', set())
    bot_data.setdefault('conversoes_vip', 0)
    bot_data.setdefault('sinais_vip', 0)
    bot_data.setdefault('win_primeira_vip', 0)
    bot_data.setdefault('win_gale_vip', 0)
    bot_data.setdefault('loss_vip', 0)
    logger.info("Estatísticas OK.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exceção ao manipular uma atualização: {context.error}", exc_info=context.error)
    if isinstance(context.error, Conflict):
        logger.warning("ERRO DE CONFLITO DETECTADO. Outra instância do bot pode estar rodando.")
    elif isinstance(context.error, BadRequest):
        chat_id = update.effective_chat.id if update and hasattr(update, 'effective_chat') else "desconhecido"
        logger.error(f"Erro de BadRequest no chat {chat_id}: {context.error}")
    elif isinstance(context.error, KeyError):
        logger.critical(f"KeyError: {context.error}. Isso pode indicar um problema de inicialização. Forçando reinicialização das estatísticas.")
        inicializar_estatisticas(context.bot_data)

# --- COMANDOS E INTERAÇÕES DO BOT ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome_usuario = user.first_name or "Campeão"
    if user.id not in context.bot_data.get('usuarios_unicos', set()):
        context.bot_data['usuarios_unicos'].add(user.id)
        logger.info(f"Novo usuário capturado pelo funil: {nome_usuario} ({user.id})")

    mensagem = f"""
Olá, {nome_usuario}! Sou o Júnior Moreira, especialista em análise de dados para jogos online. Seja muito bem-vindo(a).

Se você chegou até aqui, é porque busca uma forma consistente de lucrar. Eu desenvolvi um sistema que analisa 15 jogos 24h por dia para encontrar as melhores oportunidades para nós.

Preparei uma **condição especial para você começar a lucrar comigo hoje**:

1️⃣ **Faça seu cadastro e primeiro depósito** na plataforma que eu uso e confio. Use o código `GESTAO` para ganhar um bônus de até R$600.
2️⃣ **Me envie o comprovante** e eu vou te liberar **90 dias de acesso GRÁTIS** ao meu Grupo VIP de sinais.

Vamos começar a investir de forma inteligente.

Abraço,
**Júnior Moreira**
"""
    keyboard = [
        [InlineKeyboardButton("1️⃣ CADASTRAR E PEGAR BÔNUS", url=URL_CADASTRO_DEPOSITO)],
        [InlineKeyboardButton("2️⃣ ENVIAR COMPROVANTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace('@', ''  )}")],
        [InlineKeyboardButton("🤔 Quero ver seu canal grátis primeiro", url=URL_TELEGRAM_FREE)]
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

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "oferta_vip":
        mensagem = f"""
🚨 **Ótima decisão, {user.first_name}!** 🚨
Estou aqui para te ajudar a lucrar. Siga os passos:

🔥 **Use o Código Promocional: `GESTAO`** 🔥

Com ele, você garante:
💰 **BÔNUS DE ATÉ R$ 600,00**
💎 **90 DIAS DE ACESSO VIP GRÁTIS**
📚 **MEU E-BOOK "JUROS COMPOSTOS"**
🏆 **SORTEIOS MILIONÁRIOS**

⚠️ **ATENÇÃO: ESTOU LIBERANDO POUCAS VAGAS!**
"""
        keyboard = [
            [InlineKeyboardButton("1️⃣ ATIVAR OFERTA E USAR CÓDIGO", url=URL_CADASTRO_DEPOSITO)],
            [InlineKeyboardButton("2️⃣ ENVIAR COMPROVANTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace('@', ''  )}")],
        ]
        await context.bot.send_message(
            chat_id=user.id,
            text=mensagem,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"✅ Comprovante recebido, {user.first_name}! Minha equipe já vai analisar e te dar o acesso VIP. Obrigado pela confiança!"
    )
    context.bot_data['conversoes_vip'] += 1
    logger.info(f"Conversão VIP registrada para o usuário {user.first_name} ({user.id}).")
    
    mensagem_liberacao = f"""
🎉 **ACESSO VIP LIBERADO, {user.first_name}!** 🎉

Parabéns! Você agora faz parte da elite.

🔗 **SEU LINK VIP EXCLUSIVO:**
{URL_VIP_ACESSO}

Bem-vindo ao time! 🏆
"""
    await context.bot.send_message(chat_id=user.id, text=mensagem_liberacao, parse_mode=ParseMode.MARKDOWN)

# --- LÓGICA DE SINAIS ---
async def enviar_sinal_jogo(context: ContextTypes.DEFAULT_TYPE, jogo: str, target_id: int, confianca: float):
    bd = context.bot_data
    dados_jogo = JOGOS_COMPLETOS.get(jogo, {})
    aposta_escolhida = random.choice(dados_jogo.get("apostas", ["Aposta Padrão"]))

    if target_id == VIP_CANAL_ID:
        logger.info(f"Enviando sinal VIP completo para o jogo {jogo}.")
        await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_ANALISE), caption=f"Pessoal, estou analisando o {jogo} agora... Fiquem atentos.")
        await asyncio.sleep(random.randint(8, 12))
        mensagem_sinal = f"💎 **ENTRADA CONFIRMADA | {jogo}** 💎\n\nPessoal, podem entrar!\n\n🎯 **Aposta:** {aposta_escolhida}\n🔥 **Confiança da Análise:** Altíssima\n\n🔗 **JOGAR AGORA:**\n[**>> CLIQUE AQUI PARA ACESSAR A PLATAFORMA <<**]({URL_CADASTRO_DEPOSITO})\n\nVamos pra cima! 🚀"
        await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN)
        
        bd['sinais_vip'] += 1
        await asyncio.sleep(random.randint(60, 90))
        
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=dados_jogo["assertividade"], k=1)[0]
        bd[f'{resultado}_vip'] += 1
        
        if resultado == "win_primeira":
            await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_VITORIA), caption=f"✅✅✅ GREEN! É dinheiro no bolso da galera! {jogo} 🤑")
        elif resultado == "win_gale":
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE, caption=f"✅ GREEN NO GALE! Quem seguiu a gestão, lucrou! {jogo} 💪")
        else:
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=f"❌ RED! Acontece, pessoal. Disciplina e gestão de banca que a gente recupera na próxima. {jogo} 🔄")

    elif target_id == FREE_CANAL_ID:
        logger.info(f"Enviando Sinal Fantasma (marketing) para o jogo {jogo}.")
        await context.bot.send_animation(chat_id=target_id, animation=random.choice(GIFS_ANALISE), caption=f"Fala, pessoal! Júnior Moreira aqui. Acabei de identificar uma oportunidade no {jogo}...")
        await asyncio.sleep(random.randint(5, 8))
        msg_oportunidade = f"🚨 **OPORTUNIDADE DE LUCRO IDENTIFICADA!** 🚨\n\nMinha análise encontrou um padrão com **{confianca*100:.0f}% de confiança** no **{jogo}**.\n\n🔥 **ACABEI DE ENVIAR O SINAL PARA O GRUPO VIP!** 🔥\n\nO pessoal já está fazendo a entrada. Se você quer parar de só olhar e começar a lucrar comigo, a hora é agora."
        keyboard = [[InlineKeyboardButton("💎 EU QUERO ENTRAR NO VIP, JÚNIOR!", callback_data="oferta_vip")]]
        await context.bot.send_message(chat_id=target_id, text=msg_oportunidade, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        
        await asyncio.sleep(random.randint(70, 100))
        
        greens_vip = bd.get('win_primeira_vip', 0) + bd.get('win_gale_vip', 0)
        reds_vip = bd.get('loss_vip', 0)
        assertividade_vip = (greens_vip / max(greens_vip + reds_vip, 1)) * 100
        
        msg_resultado = f"✅✅ **GREEN NO VIP!** ✅✅\n\nComo eu disse, pessoal! O sinal que enviei no **{jogo}** bateu. A entrada foi: **{aposta_escolhida}**.\n\nMeu grupo VIP acabou de colocar mais dinheiro no bolso! 🤑\n\n📊 **Meu placar de hoje (VIP):**\n**{greens_vip} ✅ x {reds_vip} ❌** ({assertividade_vip:.1f}% de Assertividade)\n\nCansado de perder dinheiro? Vem lucrar com quem entende do assunto."
        keyboard_resultado = [[InlineKeyboardButton("🚀 QUERO LUCRAR COM VOCÊ, JÚNIOR!", callback_data="oferta_vip")]]
        
        url_foto = f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{random.randint(1, 19  )}.png"
        await context.bot.send_photo(chat_id=target_id, photo=url_foto, caption=msg_resultado, reply_markup=InlineKeyboardMarkup(keyboard_resultado), parse_mode=ParseMode.MARKDOWN)

# --- AGENDAMENTOS ---
async def enviar_sinal_automatico(context: ContextTypes.DEFAULT_TYPE):
    jogo = random.choice(list(JOGOS_COMPLETOS.keys()))
    confianca_vip = random.uniform(0.90, 0.98)
    await enviar_sinal_jogo(context, jogo, VIP_CANAL_ID, confianca_vip)
    await asyncio.sleep(random.randint(15, 45))
    await enviar_sinal_jogo(context, jogo, FREE_CANAL_ID, confianca_vip)

async def enviar_marketing_automatico(context: ContextTypes.DEFAULT_TYPE):
    sistema_conversao = context.bot_data.get('sistema_conversao')
    if not sistema_conversao: 
        logger.warning("Sistema de conversão não encontrado para marketing automático.")
        return
    
    # Alterna entre prova social e campanha de escassez
    if random.random() < 0.6: # 60% de chance de enviar prova social
        await sistema_conversao.enviar_prova_social_conversao(FREE_CANAL_ID)
    else: # 40% de chance de enviar campanha de escassez
        await sistema_conversao.executar_campanha_escassez_extrema(FREE_CANAL_ID)

# --- FUNÇÃO PRINCIPAL ---
def main():
    logger.info("Iniciando o bot...")
    persistence = PicklePersistence(filepath="bot_data.pkl")
    
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()
    inicializar_estatisticas(app.bot_data)

    # A instância do SistemaConversaoVIP é necessária para o marketing
    sistema_conversao = SistemaConversaoVIP(app, URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM, URL_VIP_ACESSO)
    app.bot_data['sistema_conversao'] = sistema_conversao

    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command, filters=filters.User(user_id=ADMIN_ID)))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))

    jq = app.job_queue
    jq.run_repeating(enviar_sinal_automatico, interval=45 * 60, first=10)
    # REATIVANDO A LINHA DE MARKETING
    jq.run_repeating(enviar_marketing_automatico, interval=90 * 60, first=30)

    logger.info("🚀 Bot do Júnior Moreira V27.3 iniciado com sucesso!")
    logger.info(f"🎮 {len(JOGOS_COMPLETOS)} jogos sendo analisados!")
    logger.info("💎 Sistema de conversão VIP ativado!")
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
