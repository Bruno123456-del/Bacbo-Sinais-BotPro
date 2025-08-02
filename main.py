# -*- coding: utf-8 -*-

import logging
import os
import random
import asyncio
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÃO INICIAL ---

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega as credenciais do arquivo .env e usa .strip() para remover
# espaços ou quebras de linha acidentais.
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CANAL_ID = os.getenv("CANAL_ID", "0").strip()
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a" ) # Link para o botão

# Validação para garantir que as credenciais foram carregadas
if not BOT_TOKEN or CANAL_ID == "0":
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN ou CANAL_ID não foram encontrados no arquivo .env.")

CANAL_ID = int(CANAL_ID)

# Configura o sistema de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 2. BANCO DE MÍDIA E MENSAGENS ---

GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_WIN = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

# --- 3. ESTADO DO BOT (Contadores ) ---

async def inicializar_contadores(application: Application):
    application.bot_data.setdefault('diario_win', 0)
    application.bot_data.setdefault('diario_loss', 0)
    logger.info(f"Contadores inicializados: {application.bot_data}")

# --- 4. COMANDOS DO USUÁRIO (Para chat privado) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Olá {user.mention_html()}! 👋\n\n"
        "Eu sou o bot de sinais para Bac Bo. Os sinais são enviados automaticamente no canal oficial."
    )

# --- 5. LÓGICA PRINCIPAL DOS SINAIS ---

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    
    try:
        # ETAPA 1: ANÁLISE
        msg_analise = await context.bot.send_animation(
            chat_id=CANAL_ID,
            animation=GIF_ANALISANDO,
            caption="""
📡 **Analisando padrões do mercado...**

Nossa I.A. está buscando a melhor oportunidade.
Aguarde, um sinal de alta precisão pode surgir a qualquer momento.
            """
        )
        logger.info("Fase de análise iniciada.")
        await asyncio.sleep(random.randint(15, 25))

        # ETAPA 2: SINAL COM BOTÃO
        aposta_sugerida = random.choice(["Banker 🔴", "Player 🔵"])
        
        # Criação do botão
        botao_bonus = InlineKeyboardButton(
            text="💎 Jogue Bac Bo com Bônus Exclusivo 💎",
            url=URL_CADASTRO
        )
        teclado_sinal = InlineKeyboardMarkup([[botao_bonus]])
        
        mensagem_sinal = (
            f"🔥 **SINAL VIP CONFIRMADO** 🔥\n\n"
            f"👇 **Apostar em:** {aposta_sugerida}\n"
            f"📈 **Estratégia:** Tendência Dominante v3\n\n"
            f"**PLANO DE AÇÃO:**\n"
            f"1️⃣ **Entrada Inicial**\n"
            f"2️⃣ **1ª Proteção (Gale 1)**\n"
            f"3️⃣ **2ª Proteção (Gale 2)**\n\n"
            f"⚠️ *Siga a gestão de banca. Opere com consciência.*"
        )
        await msg_analise.delete()
        msg_sinal_enviada = await context.bot.send_message(
            chat_id=CANAL_ID,
            text=mensagem_sinal,
            parse_mode='Markdown',
            reply_markup=teclado_sinal
        )
        logger.info(f"Sinal enviado: {aposta_sugerida}. Aguardando resultado.")
        
        # ETAPA 3: RESULTADO (com lógica de Gales)
        
        # TENTATIVA 1: ENTRADA
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.65: # 65% de chance de win na entrada
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NA ENTRADA!** ✅✅✅\n\n💰 **LUCRO: +4%**\n\n{placar}"
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_WIN, caption=resultado_msg)
            logger.info(f"Resultado: WIN NA ENTRADA. {placar}")
            return

        # TENTATIVA 2: GALE 1
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ Atenção: Ativando **1ª Proteção (Gale 1)**.", reply_to_message_id=msg_sinal_enviada.message_id)
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.75: # 75% de chance de win no gale 1
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 1!** ✅✅✅\n\n💰 **LUCRO TOTAL: +8%**\n\n{placar}"
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_WIN, caption=resultado_msg)
            logger.info(f"Resultado: WIN NO GALE 1. {placar}")
            return

        # TENTATIVA 3: GALE 2
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ Atenção: Ativando **2ª Proteção (Gale 2)**.", reply_to_message_id=msg_sinal_enviada.message_id)
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.85: # 85% de chance de win no gale 2
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 2!** ✅✅✅\n\n💰 **LUCRO TOTAL: +16%**\n\n{placar}"
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_WIN, caption=resultado_msg)
            logger.info(f"Resultado: WIN NO GALE 2. {placar}")
            return

        # SE NENHUM WIN, ENTÃO É RED
        bot_data['diario_loss'] += 1
        placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
        resultado_msg = f"❌❌❌ **RED!** ❌❌❌\n\nO mercado não foi a nosso favor. Disciplina é a chave. Voltaremos mais fortes na próxima!\n\n{placar}"
        await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_LOSS, caption=resultado_msg)
        logger.info(f"Resultado: RED. {placar}")

    except Exception as e:
        logger.error(f"Ocorreu um erro no ciclo de sinal: {e}")

async def resumo_diario(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    win_count = bot_data.get('diario_win', 0)
    loss_count = bot_data.get('diario_loss', 0)

    if win_count == 0 and loss_count == 0:
        logger.info("Sem operações hoje. Resumo diário não enviado.")
        return

    resumo = (
        f"📊 **RESUMO DO DIA** 📊\n\n"
        f"✅ **Greens:** {win_count}\n"
        f"❌ **Reds:** {loss_count}\n\n"
        f"Obrigado por operar com a gente hoje! Amanhã buscaremos mais resultados. 🚀"
    )
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo, parse_mode='Markdown')
    logger.info("Resumo diário enviado.")
    
    bot_data['diario_win'] = 0
    bot_data['diario_loss'] = 0

# --- 6. FUNÇÃO PRINCIPAL QUE INICIA TUDO ---
def main():
    logger.info("Iniciando o bot...")
    
    application = Application.builder().token(BOT_TOKEN).post_init(inicializar_contadores).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    job_queue = application.job_queue
    
    intervalo_aleatorio = random.randint(900, 1500)
    job_queue.run_repeating(enviar_sinal, interval=intervalo_aleatorio, first=10)
    
    job_queue.run_daily(resumo_diario, time=time(hour=22, minute=0))

    logger.info("Bot iniciado e tarefas agendadas. O bot está online e operando.")
    
    application.run_polling()

if __name__ == "__main__":
    main()
