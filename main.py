# -*- coding: utf-8 -*-

import logging
import os
import random
import asyncio
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÃO INICIAL ---

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega as credenciais do arquivo .env e usa .strip() para remover
# espaços ou quebras de linha acidentais. Esta é a correção para o erro anterior.
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CANAL_ID = os.getenv("CANAL_ID", "0").strip()

# Validação para garantir que as credenciais foram carregadas
if not BOT_TOKEN or CANAL_ID == "0":
    # Este erro aparecerá no log da Render se o .env estiver faltando ou vazio
    raise ValueError("Erro Crítico: BOT_TOKEN ou CANAL_ID não foram encontrados no arquivo .env. Verifique o arquivo.")

# Converte o CANAL_ID para número inteiro
CANAL_ID = int(CANAL_ID)

# Configura o sistema de logs para sabermos o que o bot está fazendo.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 2. BANCO DE MÍDIA E MENSAGENS ---

# URLs para os GIFs. É crucial usar links para rodar em servidores.
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
        "Eu sou o bot de sinais para Bac Bo. Os sinais são enviados automaticamente no canal oficial. "
        "Fique de olho por lá! 👀"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Não há comandos para o canal. Apenas aguarde os sinais automáticos. Boa sorte! 🍀")

# --- 5. LÓGICA PRINCIPAL DOS SINAIS ---

def definir_resultado():
    # Chance de 75% de WIN para simulação.
    return "win" if random.random() < 0.75 else "loss"

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

        # ETAPA 2: SINAL
        aposta_sugerida = random.choice(["Banker 🔴", "Player 🔵"])
        mensagem_sinal = (
            f"🔥 **SINAL VIP CONFIRMADO** 🔥\n\n"
            f"👇 **Apostar em:** {aposta_sugerida}\n"
            f"📈 **Estratégia:** Tendência Dominante v3\n\n"
            f"**PLANO DE AÇÃO:**\n"
            f"1️⃣ **Entrada Inicial**\n"
            f"2️⃣ **Cobrir com 1ª Proteção (Gale)** se necessário\n\n"
            f"⚠️ *Siga a gestão de banca. Opere com consciência.*"
        )
        await msg_analise.delete()
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal enviado: {aposta_sugerida}. Aguardando resultado.")
        
        # ETAPA 3: RESULTADO
        await asyncio.sleep(random.randint(80, 100))
        
        resultado = definir_resultado()
        if resultado == "win":
            bot_data['diario_win'] += 1
            resultado_msg = f"✅✅✅ **GREEN!** ✅✅✅\n\nMeta batida com sucesso! Parabéns a todos que seguiram o sinal."
            gif_url = GIF_WIN
        else:
            bot_data['diario_loss'] += 1
            resultado_msg = f"❌❌❌ **RED!** ❌❌❌\n\nO mercado não foi a nosso favor. Disciplina é a chave. Voltaremos mais fortes na próxima!"
            gif_url = GIF_LOSS
            
        await context.bot.send_animation(chat_id=CANAL_ID, animation=gif_url, caption=resultado_msg)
        logger.info(f"Resultado enviado: {resultado.upper()}. Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L")

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
