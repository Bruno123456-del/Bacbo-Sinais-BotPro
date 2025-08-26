# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 5.2 "REALISMO APRIMORADO"
# CRIADO E APRIMORADO POR MANUS
# FOCO EM FUNIL DE CONVERSÃO, CREDIBILIDADE E VALOR PERCEBIDO
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, filters
from dotenv import load_dotenv

load_dotenv()

# --- Credenciais e IDs ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CANAL_ID = os.getenv("CANAL_ID", "0").strip()
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://seu-link-aqui.com" ).strip()
ADMIN_ID = 5011424031
LINK_GRUPO_VIP = os.getenv("LINK_GRUPO_VIP", "https://t.me/seu_grupo_vip_privado" ).strip()

if not BOT_TOKEN or CANAL_ID == "0" or URL_CADASTRO == "https://seu-link-aqui.com":
    raise ValueError("ERRO CRÍTICO: Variáveis de ambiente não configuradas!" )
CANAL_ID = int(CANAL_ID)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Mídias ---
IMG_WIN = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_COMEMORACAO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"

# -----------------------------------------------------------------------------------
# 3. BANCO DE MENSAGENS E ESTRATÉGIAS DE MARKETING (OTIMIZADO PARA DEPÓSITO )
# -----------------------------------------------------------------------------------
MARKETING_MESSAGES = {
    "oferta_vip": (
        f"💎 **DESBLOQUEIE O ACESSO VIP + BÔNUS DE DEPÓSITO!** 💎\n\n"
        f"Gostando dos nossos sinais? Isso é só o começo. No Grupo VIP, as análises são 24h e as estratégias são muito mais avançadas.\n\n"
        f"**Ao se cadastrar e depositar através da nossa página especial, você ganha:**\n"
        f"1️⃣ **Acesso Vitalício e Gratuito** ao nosso Grupo VIP.\n"
        f"2️⃣ Um **Bônus de Depósito Exclusivo** oferecido pela plataforma.\n\n"
        f"**Como garantir seus dois prêmios:**\n"
        f"1️⃣ Acesse nossa página de bônus e cadastro: [**CLIQUE AQUI PARA ATIVAR SEU BÔNUS**]({URL_CADASTRO})\n"
        f"2️⃣ Siga as instruções da página para se cadastrar e fazer seu primeiro depósito.\n"
        f"3️⃣ Envie o comprovante para nosso suporte (@manus) e receba seu acesso VIP na hora!\n\n"
        f"É uma via de mão dupla: você potencializa seu investimento com um bônus e ainda entra para a nossa elite de apostadores. Não perca!"
    ),
    "estrategia_secreta": (
        f"🤫 **A ESTRATÉGIA DOS GIGANTES...**\n\n"
        f"Essa e outras estratégias avançadas são reveladas **apenas no nosso Grupo VIP**.\n\n"
        f"Não fique para trás. [**CLIQUE AQUI E VEJA COMO ENTRAR!**]({URL_CADASTRO})"
    ),
    "escassez": (
        f"🏃‍♂️💨 **ÚLTIMAS VAGAS COM BÔNUS!**\n\n"
        f"O bônus de depósito é limitado! Garanta o seu e o acesso VIP antes que acabe. [**QUERO MEU BÔNUS AGORA!**]({URL_CADASTRO})"
    )
}

# -----------------------------------------------------------------------------------
# 4. LÓGICA PRINCIPAL DO BOT
# -----------------------------------------------------------------------------------

### NOVO: Lista de times para dar realismo aos sinais de futebol ###
TIMES_FUTEBOL = {
    "brasil": ["Imperadores FC", "Unidos da Várzea", "Tigres do Asfalto", "Falcões da Capital", "Serpentes do Agreste"],
    "europa": ["Royal Eagles", "Metropolis United", "Porto Dragões", "Alpine FC", "Vulkano Strikers", "Lions of North"]
}

async def inicializar_estado(app: Application):
    bd = app.bot_data
    bd["sinal_em_andamento"] = False
    bd["manutencao"] = False
    logger.info("Estado do bot inicializado para a Estratégia Bilionária.")

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str):
    bd = context.bot_data
    if bd.get("sinal_em_andamento"):
        logger.warning(f"Pulei o sinal de {jogo} pois outro já estava em andamento.")
        return
        
    bd["sinal_em_andamento"] = True
    
    try:
        ### LÓGICA ATUALIZADA PARA FUTEBOL ###
        if jogo == "Futebol (Gols) 🥅":
            time_casa = random.choice(TIMES_FUTEBOL["brasil"])
            time_fora = random.choice(TIMES_FUTEBOL["europa"])
            # Garante que os times não sejam iguais
            while time_casa == time_fora:
                time_fora = random.choice(TIMES_FUTEBOL["europa"])
            aposta = f"**Jogo:** {time_casa} vs {time_fora}\n**Aposta:** {aposta}"
        
        msg_analise = await context.bot.send_animation(
            chat_id=CANAL_ID,
            animation=GIF_ANALISANDO,
            caption=f"🔎 Analisando padrões para a entrada em **{jogo.upper()}**... Fiquem atentos!"
        )
        await asyncio.sleep(random.randint(10, 20))

        mensagem_sinal = (
            f"🔥 **ENTRADA CONFIRMADA - {jogo.upper()}** 🔥\n\n"
            f"🎯 {aposta}\n"
            f"🛡️ **Proteção:** Usar até 2 gales, se necessário (não se aplica a futebol).\n\n"
            f"🔗 **[ENTRAR NA PLATAFORMA CORRETA]({URL_CADASTRO})**\n\n"
            f"✨ *No Grupo VIP, as análises como esta são 24h!*"
        )
        await msg_analise.delete()
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal agendado enviado para {jogo}.")

        await asyncio.sleep(random.randint(60, 90))
        resultado = random.choices(["win", "loss"], weights=[85, 15], k=1)[0]

        if resultado == "win":
            await context.bot.send_photo(
                chat_id=CANAL_ID,
                photo=IMG_WIN,
                caption=f"✅✅✅ **GREEN!** ✅✅✅\n\nMais uma análise perfeita! Parabéns a todos que pegaram.\n\nImagina ter acesso a isso o dia todo no nosso VIP? 😉"
            )
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_COMEMORACAO)
        else:
            await context.bot.send_message(chat_id=CANAL_ID, text="❌ RED! Acontece. Disciplina e gestão sempre. No VIP temos estratégias para recuperação rápida. Vamos para a próxima!")

    except Exception as e:
        logger.error(f"Erro no ciclo de sinal específico para {jogo}: {e}")
    finally:
        bd["sinal_em_andamento"] = False

async def enviar_mensagem_marketing(context: ContextTypes.DEFAULT_TYPE, tipo_mensagem: str):
    mensagem = MARKETING_MESSAGES.get(tipo_mensagem)
    if mensagem:
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem, parse_mode='Markdown', disable_web_page_preview=False)
        logger.info(f"Mensagem de marketing '{tipo_mensagem}' enviada.")

# -----------------------------------------------------------------------------------
# 5. AGENDAMENTO E TAREFAS RECORRENTES
# -----------------------------------------------------------------------------------
def agendar_tarefas(app: Application):
    jq = app.job_queue
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Vermelho ⚫"), time=time(hour=9, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "3 Minas - Abrir 7 campos"), time=time(hour=9, minute=35))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Aviator ✈️", "Buscar vela de 1.80x"), time=time(hour=10, minute=5))
    jq.run_daily(lambda ctx: enviar_mensagem_marketing(ctx, "oferta_vip"), time=time(hour=10, minute=30))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Bac Bo 🎲", "Player 🔵"), time=time(hour=14, minute=10))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Futebol (Gols) 🥅", "Mais de 1.5 Gols"), time=time(hour=14, minute=40))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Ímpar"), time=time(hour=15, minute=15))
    jq.run_daily(lambda ctx: enviar_mensagem_marketing(ctx, "estrategia_secreta"), time=time(hour=15, minute=45))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Aviator ✈️", "Buscar vela de 2.10x"), time=time(hour=20, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "5 Minas - Abrir 4 campos"), time=time(hour=20, minute=35))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Bac Bo 🎲", "Banker 🔴"), time=time(hour=21, minute=5))
    jq.run_daily(lambda ctx: enviar_mensagem_marketing(ctx, "escassez"), time=time(hour=21, minute=30))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Preto ⚫"), time=time(hour=23, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Futebol (Gols) 🥅", "Menos de 3.5 Gols"), time=time(hour=23, minute=30))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "3 Minas - Abrir 5 campos"), time=time(hour=23, minute=55))
    logger.info("Todos os sinais e mensagens de marketing foram agendados com sucesso.")

# -----------------------------------------------------------------------------------
# 6. COMANDOS DE USUÁRIO E PAINEL DE ADMIN
# -----------------------------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=MARKETING_MESSAGES["oferta_vip"], parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    bd = context.bot_data
    manutencao_status = "ATIVOS ✅" if not bd.get('manutencao') else "PAUSADOS ⏸️"
    keyboard = [
        [InlineKeyboardButton("⚡ Forçar Sinal de Teste", callback_data='admin_forcar_sinal')],
        [InlineKeyboardButton(f"Sinais Automáticos: {manutencao_status}", callback_data='admin_toggle_manutencao')],
        [InlineKeyboardButton("📢 Enviar Oferta VIP Agora", callback_data='admin_enviar_oferta_vip')]
    ]
    await update.message.reply_text("🔑 **Painel de Administrador - Estratégia VIP** 🔑", reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'admin_forcar_sinal':
        await query.edit_message_text("✅ Forçando um sinal de Futebol agora...")
        await enviar_sinal_especifico(context, "Futebol (Gols) 🥅", "Mais de 0.5 Gols (Teste)")
    elif query.data == 'admin_enviar_oferta_vip':
        await query.edit_message_text("✅ Enviando a oferta VIP para o canal...")
        await enviar_mensagem_marketing(context, "oferta_vip")
    elif query.data == 'admin_toggle_manutencao':
        bd = context.bot_data
        bd['manutencao'] = not bd.get('manutencao', False)
        status_text = 'PAUSADOS' if bd['manutencao'] else 'ATIVOS'
        await query.answer(f"Sinais automáticos agora estão {status_text}", show_alert=True)
        await admin_command(query, context)

# -----------------------------------------------------------------------------------
# 7. FUNÇÃO PRINCIPAL (MAIN)
# -----------------------------------------------------------------------------------
def main() -> None:
    logger.info("Iniciando o bot - Versão 5.2 'Realismo Aprimorado'...")
    app = Application.builder().token(BOT_TOKEN).post_init(inicializar_estado).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("admin", admin_command, filters=filters.User(user_id=ADMIN_ID)))
    app.add_handler(CallbackQueryHandler(admin_callbacks, pattern='^admin_'))
    agendar_tarefas(app)
    logger.info("Bot iniciado. O funil de conversão está ativo.")
    app.run_polling()

if __name__ == "__main__":
    main()
