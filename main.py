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

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CANAL_ID = os.getenv("CANAL_ID", "0").strip()
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a" )

if not BOT_TOKEN or CANAL_ID == "0":
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN ou CANAL_ID não foram encontrados no arquivo .env.")

CANAL_ID = int(CANAL_ID)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 2. BANCO DE MÍDIA E MENSAGENS DE MARKETING ---

IMG_WIN_ENTRADA = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
IMG_WIN_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
IMG_WIN_GALE2 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale2.png"
IMG_WIN_EMPATE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_empate.png"

GIFS_COMEMORACAO = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzVnb2dpcTYzb3ZkZ3k4aGg2M3NqZzZzZzRjZzZzZzRjZzZzZzRjZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abIileRivlGr8Nq/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaW9oZDN1dTY2a29uY2tqZzZzZzZzZzZzZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/a0h7sAqhlCQoM/giphy.gif"
]

GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

MENSAGEM_POS_WIN = f"""
🚀 **QUER RESULTADOS ASSIM?** 🚀

Nossos sinais são calibrados para a **1WIN**. Jogar em outra plataforma pode gerar resultados diferentes.

👉 [**Clique aqui para se cadastrar na 1WIN**]({URL_CADASTRO} ) e tenha acesso a:
✅ **Bônus Premium** de boas-vindas
🏆 **Sorteios Milionários** e até carros de luxo!

Não fique de fora! **Cadastre-se agora!**
"""

# --- 3. ESTADO DO BOT (Contadores) ---

async def inicializar_contadores(application: Application):
    application.bot_data.setdefault('diario_win', 0)
    application.bot_data.setdefault('diario_loss', 0)
    logger.info(f"Contadores inicializados: {application.bot_data}")

# --- 4. COMANDOS DO USUÁRIO (Para chat privado) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    botao_cadastro = InlineKeyboardButton("🏆 Quero meu Bônus e Sorteios 🏆", url=URL_CADASTRO)
    teclado = InlineKeyboardMarkup([[botao_cadastro]])
    await update.message.reply_html(
        f"Olá {user.mention_html()}! 👋\n\n"
        "Bem-vindo ao canal de sinais VIP! Para garantir que você tenha os mesmos resultados que nós e participe de todas as promoções, **é essencial que você jogue na plataforma certa.**\n\n"
        "Clique no botão abaixo para começar com tudo!",
        reply_markup=teclado
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Não há comandos para o canal. Apenas aguarde os sinais automáticos. Boa sorte! 🍀")

# --- 5. LÓGICA PRINCIPAL DOS SINAIS (CORRIGIDA) ---

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    
    try:
        # ETAPA 1: ANÁLISE
        msg_analise = await context.bot.send_animation(
            chat_id=CANAL_ID,
            animation=GIF_ANALISANDO,
            caption="""
📡 **Analisando padrões do mercado...**

Nossa I.A. está buscando a melhor oportunidade na **1WIN**.
Aguarde, um sinal de alta precisão pode surgir a qualquer momento.
            """
        )
        logger.info("Fase de análise iniciada.")
        await asyncio.sleep(random.randint(15, 25))

        # ETAPA 2: ENVIO DO SINAL COM ESTRATÉGIA DE COBERTURA
        aposta_principal = random.choice(["Banker 🔴", "Player 🔵"])
        
        botao_bonus = InlineKeyboardButton(
            text="💎 Cadastre-se na 1WIN e Ganhe Bônus 💎",
            url=URL_CADASTRO
        )
        teclado_sinal = InlineKeyboardMarkup([[botao_bonus]])
        
        mensagem_sinal = (
            f"🔥 **SINAL VIP CONFIRMADO** 🔥\n\n"
            f"👇 **APOSTA PRINCIPAL:** {aposta_principal}\n"
            f"🎯 **COBERTURA (Opcional):** Empate 🟡\n\n"
            f"**PLANO DE AÇÃO:**\n"
            f"1️⃣ **Entrada Principal (4% da banca)**\n"
            f"   ↳ *Opcional: 1% da banca no Empate*\n"
            f"2️⃣ **1ª Proteção (Gale 1 - 8% da banca)**\n"
            f"3️⃣ **2ª Proteção (Gale 2 - 16% da banca)**\n\n"
            f"⚠️ *Sinais otimizados para a 1WIN.*"
        )

        await msg_analise.delete()
        msg_sinal_enviada = await context.bot.send_message(
            chat_id=CANAL_ID,
            text=mensagem_sinal,
            parse_mode='Markdown',
            reply_markup=teclado_sinal
        )
        logger.info(f"Sinal enviado: {aposta_principal} com cobertura no Empate. Aguardando resultado.")
        
        # ETAPA 3: RESULTADO PASSO A PASSO
        
        # Simula se o resultado foi Empate (chance baixa)
        if random.random() < 0.10: # 10% de chance de dar empate
            await asyncio.sleep(random.randint(80, 100))
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO EMPATE!** ✅✅✅\n\n💰 **LUCRO MASSIVO!**\nA aposta principal foi devolvida e a cobertura no empate multiplicou a banca!\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_EMPATE, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return

        # TENTATIVA 1: ENTRADA PRINCIPAL
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.65: # 65% de chance de win na entrada
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NA ENTRADA!** ✅✅✅\n\n💰 **LUCRO: +4%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_ENTRADA, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return # Encerra o ciclo com sucesso

        # Se chegou aqui, a entrada não bateu. Avisa e vai para o GALE 1.
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Não bateu!** Vamos para a primeira proteção.\n\nAcionando **Gale 1**...", reply_to_message_id=msg_sinal_enviada.message_id)
        
        # TENTATIVA 2: GALE 1
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.75: # 75% de chance de win no gale 1
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 1!** ✅✅✅\n\n💰 **LUCRO TOTAL: +8%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE1, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return # Encerra o ciclo com sucesso

        # Se chegou aqui, o GALE 1 não bateu. Avisa e vai para o GALE 2.
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Ainda não veio!** Usando nossa última proteção.\n\nAcionando **Gale 2**...", reply_to_message_id=msg_sinal_enviada.message_id)

        # TENTATIVA 3: GALE 2
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.85: # 85% de chance de win no gale 2
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 2!** ✅✅✅\n\n💰 **LUCRO TOTAL: +16%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE2, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return # Encerra o ciclo com sucesso

        # Se chegou até aqui, todas as tentativas falharam. É RED.
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
