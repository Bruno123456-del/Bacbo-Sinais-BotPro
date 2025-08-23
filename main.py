# -*- coding: utf-8 -*-

import logging
import os
import random
import asyncio
from datetime import time, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
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

PROVAS_SOCIAIS = [
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova1.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova2.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova3.png"
]

GIFS_COMEMORACAO = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzVnb2dpcTYzb3ZkZ3k4aGg2M3NqZzZzZzRjZzZzZzRjZzZzZzRjZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abIileRivlGr8Nq/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif",
    "https://media.giphy.com/media/a0h7sAqhlCQoM/giphy.gif"
]

GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.giphy.gif"

MENSAGEM_POS_WIN = f"""
🚀 **QUER RESULTADOS ASSIM?** 🚀

Nossos sinais são calibrados para a plataforma que recomendamos. Jogar em outra pode gerar resultados diferentes.

👉 [**Clique aqui para se cadastrar e tenha acesso a:**]({URL_CADASTRO} )
✅ **Bônus Premium** de boas-vindas
🏆 **Sorteios Milionários** e até carros de luxo!

Não fique de fora! **Cadastre-se agora!**
"""

# --- 3. ESTADO DO BOT (Contadores e Controle de Sinais) ---

async def inicializar_contadores(application: Application):
    application.bot_data.setdefault("diario_win", 0)
    application.bot_data.setdefault("diario_loss", 0)
    application.bot_data.setdefault("sinal_em_andamento", False)
    application.bot_data.setdefault("ultimo_sinal_timestamp", 0)
    logger.info(f"Contadores inicializados: {application.bot_data}")

# --- 4. COMANDOS DO USUÁRIO (Para chat privado) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    mensagem_boas_vindas = (
        f"🌟 Olá {user.mention_html()}! 🌟\n\n"
        "🚀 **BEM-VINDO AO FUTURO DOS SINAIS iGAMING** 🚀\n\n"
        "⚡ **SISTEMA I.A. AVANÇADO ATIVADO** ⚡\n"
        "🔮 Sinais de alta precisão para múltiplos jogos\n"
        "💎 Gestão profissional de banca\n"
        "🎯 Estratégias comprovadas\n"
        "🏆 Comunidade de traders vencedores\n\n"
        "🌈 **ESCOLHA SUA JORNADA PARA O SUCESSO:**"
    )
    keyboard = [
        [InlineKeyboardButton("🎮 JOGAR AGORA", url=URL_CADASTRO)],
        [InlineKeyboardButton("📊 RESULTADOS HOJE", callback_data='resultados'),
         InlineKeyboardButton("🎲 ESCOLHER JOGO", callback_data='escolher_jogo')],
        [InlineKeyboardButton("📚 TUTORIAIS VIP", callback_data='menu_tutoriais'),
         InlineKeyboardButton("🎁 BÔNUS EXCLUSIVO", url=URL_CADASTRO)],
        [InlineKeyboardButton("💪 DESAFIO SEMANAL", callback_data='desafio_semanal'),
         InlineKeyboardButton("⚡ MOTIVAÇÃO DIÁRIA", callback_data='motivacao_diaria')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_html(mensagem_boas_vindas, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Não há comandos para o canal. Apenas aguarde os sinais automáticos. Boa sorte! 🍀")

async def estrategia_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Nossas estratégias são baseadas em análise de IA. Use /gestao para dicas de banca.")

async def gestao_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Gestão de banca: Use 2-5% por sinal, defina stop loss/gain diário.")

async def tutorial_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🎯 Gestão de Banca", callback_data='tutorial_gestao')],
        [InlineKeyboardButton("🔍 Leitura de Sinais", callback_data='tutorial_sinais')],
        [InlineKeyboardButton("🧠 Psicologia do Trader", callback_data='tutorial_psicologia')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 **TUTORIAIS DISPONÍVEIS** 📚\n\nEscolha o tutorial:", reply_markup=reply_markup)

async def desafio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    desafio_atual = random.choice(DESAFIOS_SEMANAIS)
    await update.message.reply_text(f"{desafio_atual['titulo']}\n\n{desafio_atual['descricao']}")

async def motivacao_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(random.choice(MENSAGENS_MOTIVACIONAIS))

async def suporte_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Para suporte, entre em contato com o administrador do canal.")

# --- 5. LÓGICA PRINCIPAL DOS SINAIS ---

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    bot_data["sinal_em_andamento"] = True
    try:
        msg_analise = await context.bot.send_animation(
            chat_id=CANAL_ID,
            animation=GIF_ANALISANDO,
            caption="""
📡 **Analisando padrões do mercado...**

Nossa I.A. está buscando a melhor oportunidade. Aguarde...
            """
        )
        logger.info("Fase de análise iniciada.")
        await asyncio.sleep(random.randint(15, 25))

        jogos_disponiveis = {
            "Bac Bo": {"apostas": ["Banker 🔴", "Player 🔵"], "cobertura": "Empate 🟡"},
            "Roleta": {"apostas": ["Preto ⚫", "Vermelho 🔴", "Par 🔢", "Ímpar 🔢"], "cobertura": "Zero 🟢"},
        }
        
        jogo_escolhido = random.choice(list(jogos_disponiveis.keys()))
        sinal_info = jogos_disponiveis[jogo_escolhido]
        aposta_principal = random.choice(sinal_info["apostas"])
        cobertura = sinal_info.get("cobertura", "")

        botao_cadastro = InlineKeyboardButton(text="🎮 Jogar Agora", url=URL_CADASTRO)
        teclado_sinal = InlineKeyboardMarkup([[botao_cadastro]])
        
        mensagem_sinal = (
            f"🔥 **SINAL VIP CONFIRMADO - {jogo_escolhido.upper()}** 🔥\n\n"
            f"🎯 **APOSTA PRINCIPAL:** {aposta_principal}\n"
        )
        if cobertura:
            mensagem_sinal += f"🛡️ **COBERTURA (Opcional):** {cobertura}\n\n"
        
        mensagem_sinal += (
            "**PLANO DE AÇÃO:**\n"
            "1️⃣ **Entrada Principal (4% da banca)**\n"
            "2️⃣ **1ª Proteção (Gale 1 - 8% da banca)**\n"
            "3️⃣ **2ª Proteção (Gale 2 - 16% da banca)**\n\n"
            f"⚠️ *Sinais otimizados para a plataforma recomendada.*"
        )

        await msg_analise.delete()
        msg_sinal_enviada = await context.bot.send_message(
            chat_id=CANAL_ID, text=mensagem_sinal, parse_mode='Markdown', reply_markup=teclado_sinal
        )
        logger.info(f"Sinal enviado para {jogo_escolhido}: {aposta_principal}.")
        
        # Simulação de resultado
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.65: # Win na entrada
            bot_data["diario_win"] += 1
            img = IMG_WIN_ENTRADA
            msg = "✅✅✅ **GREEN NA ENTRADA!** ✅✅✅"
        elif random.random() < 0.75: # Win no Gale 1
            bot_data["diario_win"] += 1
            img = IMG_WIN_GALE1
            msg = "✅✅✅ **GREEN NO GALE 1!** ✅✅✅"
        elif random.random() < 0.85: # Win no Gale 2
            bot_data["diario_win"] += 1
            img = IMG_WIN_GALE2
            msg = "✅✅✅ **GREEN NO GALE 2!** ✅✅✅"
        else: # Loss
            bot_data["diario_loss"] += 1
            img = GIF_LOSS
            msg = "❌❌❌ **RED!** ❌❌❌"

        placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
        
        if "GREEN" in msg:
            await context.bot.send_photo(chat_id=CANAL_ID, photo=img, caption=f"{msg}\n\n{placar}")
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
        else:
            await context.bot.send_animation(chat_id=CANAL_ID, animation=img, caption=f"{msg}\n\n{placar}")

    except Exception as e:
        logger.error(f"Ocorreu um erro no ciclo de sinal: {e}")
    finally:
        bot_data["sinal_em_andamento"] = False
        bot_data["ultimo_sinal_timestamp"] = datetime.now().timestamp()

async def verificar_e_enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    agora = datetime.now()
    
    # Não envia sinais de madrugada (0h às 7h)
    if not 7 <= agora.hour < 24:
        return

    if bot_data.get("sinal_em_andamento", False):
        return

    # Define a probabilidade de enviar um sinal por minuto
    probabilidade = 1/15 # Média de 1 sinal a cada 15 minutos

    if random.random() < probabilidade:
        logger.info("Decidiu enviar um sinal baseado na probabilidade.")
        await enviar_sinal(context)

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
        "Obrigado por operar com a gente! Amanhã tem mais. 🚀"
    )
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo, parse_mode='Markdown')
    logger.info("Resumo diário enviado.")
    
    bot_data["diario_win"] = 0
    bot_data["diario_loss"] = 0

# --- CONTEÚDO ADICIONAL ---

TUTORIAIS = {
    "gestao_banca": """
🎯 **TUTORIAL: GESTÃO DE BANCA** 🎯
A gestão de banca é a chave para o lucro.
- **Regra dos 5%:** Nunca aposte mais que 5% da sua banca.
- **Stop Loss/Gain:** Defina limites diários de perda e ganho.
- **Disciplina:** Siga seu plano sem emoção.
    """,
    "leitura_sinais": """
🔍 **TUTORIAL: LENDO NOSSOS SINAIS** 🔍
- **APOSTA PRINCIPAL:** Onde você deve entrar.
- **COBERTURA:** Proteção opcional.
- **Gales:** Use as proteções (Gale 1, Gale 2) se a entrada principal falhar.
    """,
    "psicologia_trader": """
🧠 **PSICOLOGIA DO TRADER** 🧠
- **Controle Emocional:** Não aposte com raiva.
- **Visão de Longo Prazo:** Foque no lucro mensal.
- **Paciência:** Espere os melhores sinais.
    """
}

DESAFIOS_SEMANAIS = [
    {"titulo": "🏆 DESAFIO: DISCIPLINA TOTAL", "descricao": "Siga a gestão de banca em todos os sinais."},
    {"titulo": "💎 DESAFIO: TRADER CONSISTENTE", "descricao": "Obtenha lucro em 5 dos 7 dias."},
]

MENSAGENS_MOTIVACIONAIS = [
    "💪 Cada trader de sucesso começou onde você está.",
    "🎯 Disciplina hoje = Liberdade financeira amanhã!",
    "🚀 Você está investindo no seu futuro!",
]

MENSAGENS_CONFIANCA = [
    "🛡️ **POR QUE CONFIAR EM NÓS?** 🛡️\n✅ I.A. Avançada\n✅ Histórico Comprovado\n✅ Transparência Total",
    "📊 **NOSSOS NÚMEROS** 📊\n📈 Alta assertividade\n💰 Lucro médio consistente\n👥 Milhares de membros",
]

async def enviar_prova_social_agendada(context: ContextTypes.DEFAULT_TYPE):
    try:
        prova_social_url = random.choice(PROVAS_SOCIAIS)
        await context.bot.send_photo(chat_id=CANAL_ID, photo=prova_social_url, caption=f"""
✨ **Nossos membros estão lucrando!** ✨
Junte-se a nós e comece a transformar seus dias!
👉 [**Cadastre-se e lucre também!**]({URL_CADASTRO})
""", parse_mode='Markdown')
        logger.info(f"Prova social enviada: {prova_social_url}")
    except Exception as e:
        logger.error(f"Erro ao enviar prova social: {e}")

# --- Funções para botões interativos ---

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'resultados':
        win = context.application.bot_data.get("diario_win", 0)
        loss = context.application.bot_data.get("diario_loss", 0)
        await query.edit_message_text(text=f"📊 **Resultados de Hoje:** {win}W / {loss}L")
    elif data.startswith('tutorial_'):
        tipo = data.replace('tutorial_', '')
        await query.edit_message_text(text=TUTORIAIS.get(tipo, "Tutorial não encontrado."))
    # Adicione mais lógicas de botão se necessário

# --- 6. FUNÇÃO PRINCIPAL QUE INICIA TUDO ---

def main():
    logger.info("Iniciando o bot...")
    
    application = Application.builder().token(BOT_TOKEN).post_init(inicializar_contadores).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("estrategia", estrategia_command))
    application.add_handler(CommandHandler("gestao", gestao_command))
    application.add_handler(CommandHandler("suporte", suporte_command))
    application.add_handler(CommandHandler("tutorial", tutorial_command))
    application.add_handler(CommandHandler("desafio", desafio_command))
    application.add_handler(CommandHandler("motivacao", motivacao_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    job_queue = application.job_queue
    
    # Agendador principal que verifica a cada minuto se deve enviar um sinal
    job_queue.run_repeating(verificar_e_enviar_sinal, interval=60, first=10)
    
    # Agendamento do resumo diário
    job_queue.run_daily(resumo_diario, time=time(hour=22, minute=0))

    # Agendamento das provas sociais
    job_queue.run_daily(enviar_prova_social_agendada, time=time(hour=9, minute=30))
    job_queue.run_daily(enviar_prova_social_agendada, time=time(hour=14, minute=15))
    job_queue.run_daily(enviar_prova_social_agendada, time=time(hour=18, minute=45))

    logger.info("Bot iniciado e tarefas agendadas.")
    application.run_polling()

if __name__ == "__main__":
    main()
