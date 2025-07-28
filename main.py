# -*- coding: utf-8 -*-

import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ChatAction

# --- 1. CONFIGURAÇÃO INICIAL E SEGURA ---
load_dotenv()

# Validação para garantir que as variáveis de ambiente existem
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_STR = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://seulink.com" ) # Adicione uma URL padrão ou no seu .env

if not TOKEN or not CHAT_ID_STR:
    print("🚨 ERRO CRÍTICO: As variáveis de ambiente BOT_TOKEN e CHAT_ID não foram definidas.")
    exit()

try:
    CHAT_ID = int(CHAT_ID_STR)
except ValueError:
    print(f"🚨 ERRO CRÍTICO: O CHAT_ID '{CHAT_ID_STR}' não é um número válido.")
    exit()

# --- 2. BANCO DE MÍDIA E CONTEÚDO ---

# >> GIFs para uma experiência visualmente rica
GIF_ANALISE = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_WIN = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

# >> Opções de Sinais
CORES = ["🔴 Vermelho", "⚫ Preto"]
CASAS = ["🐲 Dragão", "🐯 Tigre"]

# >> Mapa de imagens para prova social
MAPA_IMAGEM_RESULTADO = {
    "win_entrada": "imagens/win_entrada.png",
    "win_gale1": "imagens/win_gale1.png",
    "win_gale2": "imagens/win_gale2.png"
}

# --- 3. FUNÇÕES PRINCIPAIS DO BOT ---

async def enviar_sinal(bot: Bot ):
    """
    Ciclo completo de um sinal: análise, envio do sinal e resultado.
    """
    try:
        # ETAPA 1: Análise (cria expectativa)
        msg_analise = await bot.send_animation(
            chat_id=CHAT_ID,
            animation=GIF_ANALISE,
            caption="""
            📡 **Analisando padrões...**
            
            Nossos algoritmos estão buscando a entrada com maior probabilidade de acerto.
            
            *Aguarde, a oportunidade perfeita está sendo preparada.*
            """
        )
        await asyncio.sleep(random.randint(5, 10))

        # ETAPA 2: Envio do Sinal (claro e com chamada para ação)
        cor = random.choice(CORES)
        casa = random.choice(CASAS)
        
        botao_plataforma = InlineKeyboardButton(text="💎 APOSTAR AGORA 💎", url=URL_CADASTRO)
        teclado_sinal = InlineKeyboardMarkup([[botao_plataforma]])
        
        mensagem_sinal = (
            f"**🔥 OPORTUNIDADE IDENTIFICADA! 🔥**\n\n"
            f"▪️ **Jogo:** `Dragon Tiger`\n"
            f"▪️ **Entrada:** `{cor}` na casa `{casa}`\n\n"
            f"**PLANO DE AÇÃO:**\n"
            f"1️⃣ **Entrada Principal**\n"
            f"2️⃣ **Proteção 1 (Gale)**\n"
            f"3️⃣ **Proteção 2 (Gale)**\n\n"
            f"⏳ **Validade:** 3 minutos\n\n"
            f"🚨 *Opere com gestão e precisão.*"
        )
        
        await msg_analise.delete()
        await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, parse_mode='Markdown', reply_markup=teclado_sinal)
        print("✅ Sinal enviado com sucesso.")

        # ETAPA 3: Resultado (mais realista, com chance de derrota)
        await asyncio.sleep(180) # Espera a validade do sinal
        
        resultado = random.choices(["win_entrada", "win_gale1", "win_gale2", "red"], weights=[0.4, 0.3, 0.2, 0.1])[0]

        if resultado.startswith("win"):
            mensagem_green = {
                "win_entrada": "✅ GREEN NA ENTRADA! 💸",
                "win_gale1": "✅ GREEN NO GALE 1! 🤑",
                "win_gale2": "✅ GREEN NO GALE 2! 🔥"
            }[resultado]
            
            await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN, caption=mensagem_green)
            await asyncio.sleep(2)
            
            # Enviar prova social após o Green
            imagem_path = MAPA_IMAGEM_RESULTADO.get(resultado)
            if imagem_path:
                try:
                    legenda = random.choice([
                        "📸 Comprovado! Nossos membros estão lucrando!",
                        "💰 Prova social: WIN confirmado agora mesmo.",
                        "🔥 É por isso que nossa sala VIP é a melhor!"
                    ])
                    await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem_path, 'rb'), caption=legenda)
                    print("✅ Print de prova social enviado.")
                except FileNotFoundError:
                    print(f"⚠️ Aviso: Imagem não encontrada em '{imagem_path}'.")
                except Exception as e:
                    print(f"❌ Erro ao enviar print: {e}")
        else:
            await bot.send_animation(chat_id=CHAT_ID, animation=GIF_RED, caption="❌ RED! O mercado não respeitou a análise. Mantenha a gestão e aguarde o próximo sinal. Disciplina é a chave!")

    except Exception as e:
        print(f"❌ Erro no ciclo de envio de sinal: {e}")

# --- 4. COMANDOS DO BOT ---
async def start_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Olá! Sou seu bot de sinais para Dragon Tiger. Fique atento às oportunidades!")

async def estrategia_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ **Nossa Estratégia:**\nBuscamos as melhores tendências e usamos um sistema de proteção com até 2 gales para maximizar as chances de acerto. A gestão de banca é fundamental!")

async def suporte_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💬 **Suporte:**\nPrecisa de ajuda? Fale com nosso suporte através do @seu_usuario_de_suporte.")

# --- 5. FUNÇÃO PRINCIPAL DE EXECUÇÃO ---
async def main():
    """Inicializa e executa o bot."""
    
    # Cria a aplicação do bot
    application = Application.builder().token(TOKEN).build()

    # Registra os comandos
    application.add_handler(CommandHandler("start", start_comando))
    application.add_handler(CommandHandler("estrategia", estrategia_comando))
    application.add_handler(CommandHandler("suporte", suporte_comando))

    # Agenda a tarefa de enviar sinais em segundo plano
    async def agendador_de_sinais():
        while True:
            await enviar_sinal(application.bot)
            # Intervalo entre os sinais (a cada 10 minutos)
            await asyncio.sleep(600)

    # Inicia o bot e o agendador
    await application.initialize()
    await application.start()
    
    # Mantém o bot rodando e a tarefa de agendamento em paralelo
    print("🚀 Bot iniciado e rodando. Aguardando para enviar o primeiro sinal...")
    await asyncio.gather(
        application.updater.start_polling(),
        agendador_de_sinais()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n✅ Bot desligado com sucesso.")
