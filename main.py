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
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a")

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

PROVAS_SOCIAIS = [
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova1.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova2.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova3.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova4.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova5.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova6.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova7.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova8.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova9.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova10.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova11.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova12.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova13.png"
]

GIFS_COMEMORACAO = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzVnb2dpcTYzb3ZkZ3k4aGg2M3NqZzZzZzRjZzZzZzRjZzZzZzRjZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abIileRivlGr8Nq/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif",
    "https://giphy.com/gifs/a0h7sAqhlCQoM/giphy.gif"
]

GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"

# Corrigido: removido ".giphy.gif" repetido no final da URL
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

MENSAGEM_POS_WIN = f"""
🚀 **QUER RESULTADOS ASSIM?** 🚀

Nossos sinais são calibrados para a **1WIN**. Jogar em outra plataforma pode gerar resultados diferentes.

👉 [**Clique aqui para se cadastrar na 1WIN**]({URL_CADASTRO}) e tenha acesso a:
✅ **Bônus Premium** de boas-vindas
🏆 **Sorteios Milionários** e até carros de luxo!

Não fique de fora! **Cadastre-se agora!**
"""

# --- 3. ESTADO DO BOT (Contadores) ---

async def inicializar_contadores(application: Application):
    application.bot_data.setdefault("diario_win", 0)
    application.bot_data.setdefault("diario_loss", 0)
    logger.info(f"Contadores inicializados: {application.bot_data}")

# --- 4. COMANDOS DO USUÁRIO (Para chat privado) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    mensagem_boas_vindas = (
        f"Olá {user.mention_html()}! 👋\n\n"
        "Bem-vindo(a) ao canal! 🎉\n\n"
        "Para começar a lucrar com nossos sinais VIP, cadastre-se na 1WIN e garanta seu bônus exclusivo!\n\n"
        "🔗 Link do Canal: https://t.me/ApostasMilionariaVIP\n"
    )
    botao_1win = InlineKeyboardButton("💎 Cadastre-se na 1WIN", url=URL_CADASTRO)
    teclado_boas_vindas = InlineKeyboardMarkup([[botao_1win]])
    await update.message.reply_html(mensagem_boas_vindas, reply_markup=teclado_boas_vindas)

    mensagem_fixa_texto = (
        "📌 BEM-VINDO AO BAC BO IGNITE\n"
        "🎲 Estratégia, inteligência e lucros todos os dias!\n\n"
        "🚨 Acesse agora nosso hub exclusivo com:\n"
        "✅ Sinais automáticos com gestão profissional\n"
        "✅ Tutorial completo para dominar o jogo\n"
        "✅ Bônus de boas-vindas, cashback e prêmios\n"
        "✅ Plataforma oficial com software verificado\n\n"
        "🔗 ACESSE AGORA:\n"
        "👉 https://bac-bo-ignite.lovable.app/\n\n"
        "🧠 Jogue com estratégia, receba suporte e lucre com confiança!"
    )
    botao_apostar = InlineKeyboardButton("🚀 Começar a Apostar", url="https://bac-bo-ignite.lovable.app/")
    teclado_fixa = InlineKeyboardMarkup([[botao_apostar]])
    await update.message.reply_text(mensagem_fixa_texto, reply_markup=teclado_fixa, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Não há comandos para o canal. Apenas aguarde os sinais automáticos. Boa sorte! 🍀")

# --- 5. LÓGICA PRINCIPAL DOS SINAIS ---

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    
    try:
        # Enviar GIF analisando com tratamento de erro
        try:
            msg_analise = await context.bot.send_animation(
                chat_id=CANAL_ID,
                animation=GIF_ANALISANDO,
                caption="""📡 **Analisando padrões do mercado...**

Nossa I.A. está buscando a melhor oportunidade na **1WIN**.
Aguarde, um sinal de alta precisão pode surgir a qualquer momento."""
            )
        except Exception as e:
            logger.error(f"Erro ao enviar GIF analisando: {e}")
            return  # Se não conseguir enviar, interrompe o envio desse sinal

        logger.info("Fase de análise iniciada.")
        await asyncio.sleep(random.randint(15, 25))

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

        # Enviar prova social aleatória
        try:
            prova_social_url = random.choice(PROVAS_SOCIAIS)
            await context.bot.send_photo(chat_id=CANAL_ID, photo=prova_social_url, caption=f"""
✨ **Nossos membros estão lucrando!** ✨

Veja os resultados reais da nossa comunidade. Junte-se a nós e comece a transformar seus dias!

👉 [**Clique aqui para se cadastrar na 1WIN e lucrar também!**]({URL_CADASTRO})
""", parse_mode='Markdown')
            logger.info(f"Prova social enviada junto com o sinal: {prova_social_url}")
        except Exception as e:
            logger.error(f"Erro ao enviar prova social junto com o sinal: {e}")
        
        # Resultado EMPATE
        if random.random() < 0.10:
            await asyncio.sleep(random.randint(80, 100))
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NO EMPATE!** ✅✅✅\n\n💰 **LUCRO MASSIVO!**\nA aposta principal foi devolvida e a cobertura no empate multiplicou a banca!\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_EMPATE, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # Resultado ENTRADA
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.65:
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NA ENTRADA!** ✅✅✅\n\n💰 **LUCRO: +4%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_ENTRADA, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # Gale 1
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Não bateu!** Vamos para a primeira proteção.\n\nAcionando **Gale 1**...", reply_to_message_id=msg_sinal_enviada.message_id)

        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.75:
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 1!** ✅✅✅\n\n💰 **LUCRO TOTAL: +8%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE1, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # Gale 2
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Ainda não veio!** Usando nossa última proteção.\n\nAcionando **Gale 2**...", reply_to_message_id=msg_sinal_enviada.message_id)

        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.85:
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 2!** ✅✅✅\n\n💰 **LUCRO TOTAL: +16%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE2, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # RED
        bot_data["diario_loss"] += 1
        placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
        resultado_msg = f"❌❌❌ **RED!** ❌❌❌\n\nO mercado não foi a nosso favor. Disciplina é a chave. Voltaremos mais fortes na próxima!\n\n{placar}"
        try:
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_LOSS, caption=resultado_msg)
        except Exception as e:
            logger.error(f"Erro ao enviar GIF de loss: {e}")
            # Se falhar, tenta enviar como texto simples
            await context.bot.send_message(chat_id=CANAL_ID, text=resultado_msg)
        logger.info(f"Resultado: RED. {placar}")

    except Exception as e:
        logger.error(f"Ocorreu um erro no ciclo de sinal: {e}")

async def resumo_diario(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    win_count = bot_data.get("diario_win", 0)
    loss_count = bot_data.get("diario_loss", 0)

    if win_count == 0 and loss_count == 0:
        logger.info("Sem operações hoje. Resumo diário não enviado.")
        return

    resumo = (
        f"📊 **RESUMO DO DIA** 📊\n\n"
        f"✅ **Greens:** {win_count}\n"
        f"❌ **Reds:** {loss_count}\n\n"
        f"Obrigado por operar com a gente hoje! Amanhã buscaremos mais resultados. 🚀"
    )
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo, parse_mode=\'Markdown\')
    logger.info("Resumo diário enviado.")
    
    bot_data["diario_win"] = 0
    bot_data["diario_loss"] = 0

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

if __name__ == "__main__":
    application.run_polling()


