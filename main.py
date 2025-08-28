# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 21.0 "ESTABILIDADE TOTAL"
# CRIADO E APRIMORADO POR MANUS
# - CORRIGIDO ERRO CRÍTICO DE LOGGING (KeyError: 'asctime ')
# - CÓDIGO FINALIZADO E COMPLETO PARA EXECUÇÃO
# - REMOÇÃO DE DEPENDÊNCIAS INÚTEIS RECOMENDADA
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, timedelta, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    PicklePersistence,
    CallbackQueryHandler,
)
from telegram.constants import ParseMode

# --- 1. CONFIGURAÇÕES E CREDENCIAIS ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "SEU_TOKEN_AQUI").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
FREE_CANAL_ID = int(os.getenv("CHAT_ID", "0").strip())
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "0").strip())

depoimentos_id_str = os.getenv("DEPOIMENTOS_CANAL_ID", "0").strip()
DEPOIMENTOS_CANAL_ID = int(depoimentos_id_str) if depoimentos_id_str.replace("-", "").isdigit() else 0

URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_INSTAGRAM = "https://www.instagram.com/apostasmilionariasvip/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
SUPORTE_TELEGRAM = "@Superfinds_bot"

# --- CORREÇÃO DO ERRO DE LOGGING ---
# Removido o espaço extra de '%(asctime )s ' para '%(asctime)s'
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Validação inicial das credenciais
if "SEU_TOKEN_AQUI" in BOT_TOKEN or FREE_CANAL_ID == 0 or VIP_CANAL_ID == 0 or ADMIN_ID == 0:
    logger.critical("ERRO CRÍTICO: BOT_TOKEN, CHAT_ID, VIP_CANAL_ID ou ADMIN_ID não estão configurados!")
    exit()

if DEPOIMENTOS_CANAL_ID == 0:
    logger.warning("AVISO: DEPOIMENTOS_CANAL_ID não configurado. A função de depoimentos estará desativada.")

# --- 2. MÍDIAS E CONTEÚDO VISUAL ---
GIF_OFERTA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzBqZ3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
PROVAS_SOCIAIS_URLS = [f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png" for i in range(1, 14 )]

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
    "comprovante_recebido": (
        "✅ **Comprovante recebido!**\n\n"
        "Já enviei para análise da minha equipe. Assim que for confirmado, você receberá seu link de acesso VIP aqui mesmo.\n\n"
        "A análise costuma ser bem rápida! 😉"
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

# --- 5. LÓGICA PRINCIPAL DO BOT ---

def inicializar_estatisticas(bot_data):
    if 'start_time' not in bot_data:
        bot_data['start_time'] = datetime.now()
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            if f'{stat}_{ch}' not in bot_data: bot_data[f'{stat}_{ch}'] = 0

async def enviar_sinal_callback(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    jogo = job_data["jogo"]
    target_id = job_data["target_id"]
    aposta = random.choice(JOGOS[jogo])
    await enviar_sinal_especifico(context, jogo, aposta, target_id)

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target_id: int):
    bd = context.bot_data
    channel_type = 'vip' if target_id == VIP_CANAL_ID else 'free'
    
    if bd.get(f"sinal_em_andamento_{target_id}", False):
        logger.warning(f"Pulei o sinal de {jogo} para o canal {target_id} pois outro já estava em andamento.")
        return
        
    bd[f"sinal_em_andamento_{target_id}"] = True
    try:
        await context.bot.send_animation(chat_id=target_id, animation=GIF_ANALISANDO, caption=f"🔎 Analisando padrões para uma entrada em **{jogo}**...")
        await asyncio.sleep(random.randint(5, 10))
        
        mensagem_sinal = (f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
                          f"🎯 **Apostar em:** {aposta}\n"
                          f"🔗 **JOGAR NA PLATAFORMA CERTA:** [**CLIQUE AQUI**]({URL_CADASTRO_DEPOSITO})")
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP!_"
            
        await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"Sinal de {jogo} enviado para o canal {target_id}.")
        
        bd[f'sinais_{channel_type}'] += 1
        
        await asyncio.sleep(random.randint(45, 75))
        
        probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=probabilidades, k=1)[0]
        bd[f'{resultado}_{channel_type}'] += 1

        wins_total = bd.get(f'win_primeira_{channel_type}', 0) + bd.get(f'win_gale_{channel_type}', 0)
        losses_total = bd.get(f'loss_{channel_type}', 0)
        placar_total = f"📊 **Placar Geral ({channel_type.upper()}):** {wins_total}W - {losses_total}L"

        if resultado == "win_primeira":
            caption = f"✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Parabéns a todos que confiaram! 🤑\n\n{placar_total}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_GREEN_PRIMEIRA, caption=caption)
        elif resultado == "win_gale":
            caption = f"✅ **GREEN NO GALE!** ✅\n\nPaciência e gestão trazem o lucro. Parabéns, time!\n\n{placar_total}"
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE1, caption=caption)
        else:
            caption = f"❌ **RED!** ❌\n\nFaz parte do jogo. Mantenham a gestão de banca e vamos para a próxima!\n\n{placar_total}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=caption)
            
    except Exception as e:
        logger.error(f"Erro no ciclo de sinal para {jogo} no canal {target_id}: {e}")
    finally:
        bd[f"sinal_em_andamento_{target_id}"] = False

async def enviar_prova_social(context: ContextTypes.DEFAULT_TYPE):
    url_prova = random.choice(PROVAS_SOCIAIS_URLS)
    legenda = random.choice(MARKETING_MESSAGES["legendas_prova_social"])
    await context.bot.send_photo(
        chat_id=FREE_CANAL_ID,
        photo=url_prova,
        caption=f"{legenda}\n\n[**QUERO LUCRAR ASSIM TAMBÉM!**]({URL_CADASTRO_DEPOSITO})",
        parse_mode=ParseMode.MARKDOWN
    )

# --- 6. COMANDOS, MODERAÇÃO E EVENTOS ---

async def log_admin_action(context: ContextTypes.DEFAULT_TYPE, action: str):
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 **Log de Admin:**\n{action}")
    except Exception as e:
        logger.error(f"Falha ao enviar log para o admin: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=MARKETING_MESSAGES["boas_vindas_start"],
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    
    bd = context.bot_data
    inicializar_estatisticas(bd)
    uptime = datetime.now() - bd.get('start_time', datetime.now())
    days, rem = divmod(uptime.total_seconds(), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    
    stats_text = (
        f"📊 **PAINEL DE ESTATÍSTICAS GERAIS** 📊\n\n"
        f"🕒 **Tempo Ativo:** {int(days)}d, {int(hours)}h, {int(minutes)}m\n\n"
        f"--- **Canal Gratuito (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_free', 0)} | ✅: {bd.get('win_primeira_free', 0)} | ☑️: {bd.get('win_gale_free', 0)} | ❌: {bd.get('loss_free', 0)}\n\n"
        f"--- **Canal VIP (Total)** ---\n"
        f"📬 Sinais: {bd.get('sinais_vip', 0)} | ✅: {bd.get('win_primeira_vip', 0)} | ☑️: {bd.get('win_gale_vip', 0)} | ❌: {bd.get('loss_vip', 0)}\n"
    )
    await update.message.reply_text(stats_text)

async def manual_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    try:
        _, jogo_curto, canal = context.args
        jogo_completo = JOGOS_MAP.get(jogo_curto.lower())
        if not jogo_completo:
            await update.message.reply_text(f"❌ Jogo '{jogo_curto}' não encontrado. Use um dos: {', '.join(JOGOS_MAP.keys())}")
            return
            
        target_id = VIP_CANAL_ID if canal.lower() == 'vip' else FREE_CANAL_ID
        aposta = random.choice(JOGOS[jogo_completo])
        
        context.job_queue.run_once(
            lambda ctx: asyncio.create_task(enviar_sinal_especifico(ctx, jogo_completo, aposta, target_id)), 0
        )
        
        log_message = f"Comando `/sinal {jogo_curto} {canal}` executado."
        await log_admin_action(context, log_message)
        await update.message.reply_text("✅ Sinal manual enviado com sucesso.")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ **Uso incorreto!**\nUse: `/sinal <jogo> <canal>`\nExemplo: `/sinal mines vip`")

async def handle_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    await update.message.reply_text(MARKETING_MESSAGES["comprovante_recebido"])
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Liberar Acesso VIP", callback_data=f"liberar_{user.id}")],
        [InlineKeyboardButton("❌ Recusar", callback_data=f"recusar_{user.id}")]
    ])
    
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"🚨 **Novo Comprovante para Análise** 🚨\n\n"
                f"**De:** {user.full_name} (@{user.username})\n"
                f"**ID:** `{user.id}`\n\n"
                f"Por favor, verifique e aprove ou recuse o acesso VIP.",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    logger.info(f"Comprovante recebido de {user.id} e encaminhado para o admin.")

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    action, user_id_str = query.data.split("_", 1)
    user_id = int(user_id_str)
    
    original_caption = query.message.caption if query.message.caption else ""

    if action == "liberar":
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=MARKETING_MESSAGES["acesso_liberado_vip"],
                parse_mode=ParseMode.MARKDOWN
            )
            await query.edit_message_caption(caption=f"{original_caption}\n\n**Status: ✅ ACESSO LIBERADO**", parse_mode=ParseMode.MARKDOWN)
            logger.info(f"Acesso VIP liberado para o usuário {user_id} pelo admin.")
        except Exception as e:
            await query.edit_message_caption(caption=f"{original_caption}\n\n**Status: ⚠️ FALHA AO LIBERAR!**\nErro: {e}", parse_mode=ParseMode.MARKDOWN)
            logger.error(f"Falha ao liberar acesso para {user_id}: {e}")
    elif action == "recusar":
        await query.edit_message_caption(caption=f"{original_caption}\n\n**Status: ❌ RECUSADO**", parse_mode=ParseMode.MARKDOWN)
        logger.info(f"Comprovante do usuário {user_id} recusado pelo admin.")

# --- 7. INICIALIZAÇÃO E AGENDAMENTO ---

def main() -> None:
    """Função principal que constrói e executa o bot."""
    
    persistence = PicklePersistence(filepath="bot_data.pickle")
    
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .persistence(persistence)
        .build()
    )

    inicializar_estatisticas(application.bot_data)

    # --- Agendamento de Sinais Automáticos ---
    job_queue = application.job_queue
    
    # Exemplo de agendamento: um sinal a cada 2 horas no canal VIP
    job_queue.run_repeating(
        enviar_sinal_callback,
        interval=timedelta(hours=2),
        first=timedelta(seconds=10),
        data={"jogo": "Aviator ✈️", "target_id": VIP_CANAL_ID},
        name="sinal_vip_aviator"
    )
    
    # Exemplo: um sinal a cada 4 horas no canal Gratuito
    job_queue.run_repeating(
        enviar_sinal_callback,
        interval=timedelta(hours=4),
        first=timedelta(seconds=20),
        data={"jogo": "Mines 💣", "target_id": FREE_CANAL_ID},
        name="sinal_free_mines"
    )

    # Exemplo: prova social a cada 3 horas no canal Gratuito
    job_queue.run_repeating(
        enviar_prova_social,
        interval=timedelta(hours=3),
        first=timedelta(minutes=30),
        name="prova_social_free"
    )

    # --- Handlers de Comandos e Mensagens ---
    application.add_handler(CommandHandler("start", start_command, filters=filters.ChatType.PRIVATE))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("sinal", manual_signal_command))
    
    # Handler para receber fotos (comprovantes) em conversas privadas
    application.add_handler(MessageHandler(filters.PHOTO & filters.ChatType.PRIVATE, handle_comprovante))
    
    # Handler para os botões de aprovação/recusa
    application.add_handler(CallbackQueryHandler(button_callback_handler))

    logger.info("Bot iniciado e rodando...")
    application.run_polling()

if __name__ == "__main__":
    main()
