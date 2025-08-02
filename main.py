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
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a" ) # SEU LINK DE AFILIADO

if not BOT_TOKEN or CANAL_ID == "0":
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN ou CANAL_ID não foram encontrados no arquivo .env.")

CANAL_ID = int(CANAL_ID)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 2. BANCO DE MÍDIA E MENSAGENS DE MARKETING ---

# Links diretos para suas imagens no GitHub
IMG_WIN_ENTRADA = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
IMG_WIN_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
IMG_WIN_GALE2 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale2.png"
IMG_WIN_EMPATE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_empate.png"

GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

# Mensagem de marketing para ser usada após cada WIN
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

Nossa I.A. está buscando a melhor oportunidade na **1WIN**.
Aguarde, um sinal de alta precisão pode surgir a qualquer momento.
            """
        )
        logger.info("Fase de análise iniciada.")
        await asyncio.sleep(random.randint(15, 25))

        # ETAPA 2: ESCOLHA DO SINAL (INCLUINDO EMPATE)
        opcoes_de_aposta = ["Banker 🔴", "Player 🔵", "Empate 🟡"]
        pesos = [0.45, 0.45, 0.10]
        aposta_sugerida = random.choices(opcoes_de_aposta, weights=pesos, k=1)[0]

        botao_bonus = InlineKeyboardButton(
            text="💎 Cadastre-se na 1WIN e Ganhe Bônus 💎",
            url=URL_CADASTRO
        )
        teclado_sinal = InlineKeyboardMarkup([[botao_bonus]])
        
        if "Empate" in aposta_sugerida:
            mensagem_sinal = (
                f"🚨 **ALERTA DE OPORTUNIDADE RARA (Odd Alta)** 🚨\n\n"
                f"👇 **Apostar em:** {aposta_sugerida}\n"
                f"📈 **Estratégia:** Cobertura de Empate\n\n"
                f"**PLANO DE AÇÃO:**\n"
                f"1️⃣ **Entrada de 1% da banca no Empate**\n"
                f"2️⃣ **Cobrir com 1ª Proteção (Gale)** se necessário\n\n"
                f"⚠️ *Exclusivo para jogadores na 1WIN.*"
            )
        else:
            mensagem_sinal = (
                f"🔥 **SINAL VIP CONFIRMADO** 🔥\n\n"
                f"👇 **Apostar em:** {aposta_sugerida}\n"
                f"📈 **Estratégia:** Tendência Dominante v3\n\n"
                f"**PLANO DE AÇÃO:**\n"
                f"1️⃣ **Entrada Inicial**\n"
                f"2️⃣ **1ª Proteção (Gale 1)**\n"
                f"3️⃣ **2ª Proteção (Gale 2)**\n\n"
                f"⚠️ *Sinais otimizados para a 1WIN.*"
            )

        await msg_analise.delete()
        msg_sinal_enviada = await context.bot.send_message(
            chat_id=CANAL_ID,
            text=mensagem_sinal,
            parse_mode='Markdown',
            reply_markup=teclado_sinal
        )
        logger.info(f"Sinal enviado: {aposta_sugerida}. Aguardando resultado.")
        
        # ETAPA 3: RESULTADO
        
        # Lógica de Empate
        if "Empate" in aposta_sugerida:
            await asyncio.sleep(random.randint(80, 100))
            if random.random() < 0.40:
                bot_data['diario_win'] += 1
                placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
                resultado_msg = f"✅✅✅ **GREEN NO EMPATE!** ✅✅✅\n\n💰 **LUCRO MASSIVO!**\n\n{placar}"
                await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_EMPATE, caption=resultado_msg)
                await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
                return

        # Lógica normal para Player/Banker com gales
        # TENTATIVA 1: ENTRADA
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.65:
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NA ENTRADA!** ✅✅✅\n\n💰 **LUCRO: +4%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_ENTRADA, caption=resultado_msg)
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return

        # TENTATIVA 2: GALE 1
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ Atenção: Ativando **1ª Proteção (Gale 1)**.", reply_to_message_id=msg_sinal_enviada.message_id)
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.75:
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 1!** ✅✅✅\n\n💰 **LUCRO TOTAL: +8%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE1, caption=resultado_msg)
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return

        # TENTATIVA 3: GALE 2
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ Atenção: Ativando **2ª Proteção (Gale 2)**.", reply_to_message_id=msg_sinal_enviada.message_id)
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.85:
            bot_data['diario_win'] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 2!** ✅✅✅\n\n💰 **LUCRO TOTAL: +16%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE2, caption=resultado_msg)
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
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
