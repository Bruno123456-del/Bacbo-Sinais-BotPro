# -*- coding: utf-8 -*-

import logging
import os
import random
import asyncio
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
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

# Imagens de resultado (genéricas, sem nome de casa de aposta)
IMG_WIN_ENTRADA = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
IMG_WIN_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
IMG_WIN_GALE2 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale2.png"
IMG_WIN_EMPATE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_empate.png"

# Novas provas sociais (simuladas, estilo WhatsApp)
PROVAS_SOCIAIS = [
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova1.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova2.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova3.png"
]

GIFS_COMEMORACAO = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzVnb2dpcTYzb3ZkZ3k4aGg2M3NqZzZzZzRjZzZzZzRjZzZzZzRjZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abIileRivlGr8Nq/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif",
    "https://giphy.com/gifs/a0h7sAqhlCQoM/giphy.gif"
]

GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.giphy.gif"

MENSAGEM_POS_WIN = f"""
🚀 **QUER RESULTADOS ASSIM?** 🚀

Nossos sinais são calibrados para a plataforma que recomendamos. Jogar em outra pode gerar resultados diferentes.

👉 [**Clique aqui para se cadastrar e tenha acesso a:**]({URL_CADASTRO})
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
    
    # Mensagem de boas-vindas com visual futurista (preto + neon roxo/verde)
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
    
    # Botões com visual futurista
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

    # Guia rápido com visual aprimorado
    await update.message.reply_text(
        """
💰 **🔥 GUIA RÁPIDO: GESTÃO DE BANCA PROFISSIONAL 🔥** 💰

🎯 **REGRAS DE OURO PARA O SUCESSO:**

🟢 **1. LIMITE DIÁRIO:** Nunca aposte mais que 20% da sua banca total por dia
🟣 **2. ENTRADA SEGURA:** Use 2-5% da banca por sinal
🟢 **3. STOP LOSS:** Pare ao perder 15% da banca diária
🟣 **4. STOP GAIN:** Retire 50% dos lucros ao dobrar a banca
🟢 **5. DISCIPLINA:** Siga SEMPRE o plano, sem exceções

⚡ **LEMBRE-SE:** Consistência > Grandes apostas
🚀 **OBJETIVO:** Crescimento sustentável e lucrativo

🛡️ **SUA SEGURANÇA É NOSSA PRIORIDADE!**
        """,
        parse_mode='Markdown'
    )

    # FAQ com design futurista
    await update.message.reply_text(
        """
🤖 **CENTRAL DE COMANDOS DISPONÍVEIS** 🤖

⚡ **COMANDOS RÁPIDOS:**
/tutorial - 📚 Tutoriais completos
/desafio - 🏆 Desafio semanal atual  
/motivacao - 💪 Dose de motivação
/estrategia - 🧠 Nossas estratégias
/gestao - 📊 Gestão avançada de banca
/suporte - 🤝 Suporte técnico

🔮 **DICA PRO:** Use os botões interativos para uma experiência mais fluida!
        """,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Não há comandos para o canal. Apenas aguarde os sinais automáticos. Boa sorte! 🍀")

async def estrategia_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
        📈 **NOSSAS ESTRATÉGIAS** 📈

        Nossos sinais são gerados por uma inteligência artificial avançada que analisa padrões de mercado em tempo real. Utilizamos uma combinação de análise técnica e probabilística para identificar as melhores oportunidades em diversos jogos.

        **Principais características:**
        - **Multi-jogos:** Sinais para Bac Bo, Roleta, Blackjack, Aviator, Mines, Crash e Apostas Esportivas.
        - **Gestão de Risco:** Nossos sinais incluem sugestões de gestão de banca (entrada principal e proteção/gales) para otimizar seus resultados.
        - **Atualizações Constantes:** A I.A. está sempre aprendendo e se adaptando para oferecer a maior precisão possível.

        Lembre-se: Nenhuma estratégia é 100% infalível. Jogue com responsabilidade!
        """
    )

async def gestao_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
        📊 **GESTÃO DE BANCA AVANÇADA** 📊

        Uma boa gestão de banca é crucial para o sucesso a longo prazo. Considere estas abordagens:

        1. **Porcentagem Fixa:** Aposte sempre uma porcentagem fixa da sua banca (ex: 2% por aposta). Isso protege seu capital em dias ruins e aumenta seus ganhos em dias bons.
        2. **Martingale (com cautela):** Aumente o valor da aposta após uma perda para recuperar o valor perdido e obter lucro. **CUIDADO:** Esta estratégia exige uma banca grande e pode levar a perdas rápidas se não for bem gerenciada.
        3. **Stop Loss/Stop Gain:** Defina limites diários de perda e ganho. Ao atingir um desses limites, pare de operar no dia.

        **Exemplo de Plano de Ação (sugerido nos sinais):**
        - Entrada Principal: 4% da banca
        - 1ª Proteção (Gale 1): 8% da banca (se a entrada principal não der GREEN)
        - 2ª Proteção (Gale 2): 16% da banca (se o Gale 1 não der GREEN)

        Adapte sua gestão ao seu perfil de risco!
        """
    )

async def tutorial_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🎯 Gestão de Banca", callback_data='tutorial_gestao')],
        [InlineKeyboardButton("🔍 Leitura de Sinais", callback_data='tutorial_sinais')],
        [InlineKeyboardButton("🧠 Psicologia do Trader", callback_data='tutorial_psicologia')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📚 **TUTORIAIS DISPONÍVEIS** 📚\n\nEscolha o tutorial que deseja acessar:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def desafio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    desafio_atual = random.choice(DESAFIOS_SEMANAIS)
    await update.message.reply_text(
        f"{desafio_atual['titulo']}\n\n"
        f"📋 **DESCRIÇÃO:** {desafio_atual['descricao']}\n\n"
        f"🎯 **META:** {desafio_atual['meta']}\n\n"
        f"🏆 **PRÊMIO:** {desafio_atual['premio']}\n\n"
        f"💪 **Aceite o desafio e prove que você é um trader de elite!**",
        parse_mode='Markdown'
    )

async def motivacao_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensagem = random.choice(MENSAGENS_MOTIVACIONAIS)
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def suporte_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
        🤝 **SUPORTE AO USUÁRIO** 🤝

        Se você tiver dúvidas, problemas ou precisar de assistência, entre em contato conosco:

        📧 **Email:** suporte@seubot.com (Exemplo, substitua pelo seu email)
        💬 **Chat:** Em breve, um canal de suporte direto!

        Estamos aqui para ajudar você a ter a melhor experiência!
        """
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

Nossa I.A. está buscando a melhor oportunidade na plataforma que recomendamos.
Aguarde, um sinal de alta precisão pode surgir a qualquer momento.
            """
        )
        logger.info("Fase de análise iniciada.")
        await asyncio.sleep(random.randint(15, 25))

        # Sistema avançado de sinais para múltiplos jogos
        jogos_disponiveis = {
            "Bac Bo": {
                "apostas": ["Banker 🔴", "Player 🔵"], 
                "cobertura": "Empate 🟡",
                "estrategia": "Análise de padrões das últimas 20 rodadas",
                "odds": "1.95x",
                "tempo_rodada": "30-45 segundos"
            },
            "Roleta": {
                "apostas": ["Preto ⚫", "Vermelho 🔴", "Par 🔢", "Ímpar 🔢", "1-18 📊", "19-36 📊"], 
                "cobertura": "Zero 🟢",
                "estrategia": "Sequência de Fibonacci + análise de setores",
                "odds": "2.0x",
                "tempo_rodada": "60-90 segundos"
            },
            "Blackjack": {
                "apostas": ["Player 🃏", "Dealer 🃏"], 
                "cobertura": "Empate 🃏",
                "estrategia": "Contagem básica + gestão de cartas",
                "odds": "1.95x",
                "tempo_rodada": "45-60 segundos"
            },
            "Aviator": {
                "apostas": ["Sair em 1.5x ✈️", "Sair em 2.0x ✈️", "Sair em 3.0x ✈️", "Aguardar 5x+ ✈️"], 
                "cobertura": "",
                "estrategia": "Análise de volatilidade e padrões de crash",
                "odds": "Variável",
                "tempo_rodada": "8-15 segundos"
            },
            "Mines": {
                "apostas": ["3 Minas ⛏️", "5 Minas ⛏️", "7 Minas ⛏️", "10 Minas ⛏️"], 
                "cobertura": "",
                "estrategia": "Probabilidade matemática + padrões de campo",
                "odds": "Variável (1.2x - 50x)",
                "tempo_rodada": "Instantâneo"
            },
            "Crash": {
                "apostas": ["Sair em 1.5x 💥", "Sair em 2.0x 💥", "Aguardar 3x+ 💥"], 
                "cobertura": "",
                "estrategia": "Análise de tendências e multiplicadores históricos",
                "odds": "Variável",
                "tempo_rodada": "5-20 segundos"
            },
            "Futebol": {
                "apostas": ["Over 2.5 Gols ⚽", "Under 2.5 Gols ⚽", "Ambos Marcam ✅", "Casa Vence 🏠", "Fora Vence 🚗"], 
                "cobertura": "Empate ⚖️",
                "estrategia": "Análise estatística + forma atual dos times",
                "odds": "1.80x - 2.50x",
                "tempo_rodada": "90 minutos + acréscimos"
            },
            "UFC": {
                "apostas": ["Lutador A Vence 🥊", "Lutador B Vence 🥊", "Vai para Decisão ⏱️", "Finalização 🎯"], 
                "cobertura": "",
                "estrategia": "Análise de histórico + estilo de luta",
                "odds": "1.50x - 4.00x",
                "tempo_rodada": "15-25 minutos"
            },
            "Basquete": {
                "apostas": ["Over Total Pontos 🏀", "Under Total Pontos 🏀", "Casa +5.5 📊", "Fora +5.5 📊"], 
                "cobertura": "",
                "estrategia": "Análise de ritmo de jogo + defesas",
                "odds": "1.85x - 2.10x",
                "tempo_rodada": "48 minutos (4 quartos)"
            }
        }
        
        jogo_escolhido = random.choice(list(jogos_disponiveis.keys()))
        sinal_info = jogos_disponiveis[jogo_escolhido]
        aposta_principal = random.choice(sinal_info["apostas"])
        cobertura = sinal_info["cobertura"]

        botao_cadastro = InlineKeyboardButton(
            text="🎮 Jogar Agora e Cadastrar",
            url=URL_CADASTRO
        )
        teclado_sinal = InlineKeyboardMarkup([[botao_cadastro]])
        
        mensagem_sinal = (
            f"🔥 **SINAL VIP CONFIRMADO - {jogo_escolhido.upper()}** 🔥\n\n"
            f"🎯 **APOSTA PRINCIPAL:** {aposta_principal}\n"
            f"📊 **ODDS:** {sinal_info['odds']}\n"
            f"⏱️ **TEMPO DE RODADA:** {sinal_info['tempo_rodada']}\n"
            f"🧠 **ESTRATÉGIA:** {sinal_info['estrategia']}\n"
        )
        if cobertura:
            mensagem_sinal += f"🛡️ **COBERTURA (Opcional):** {cobertura}\n\n"
        else:
            mensagem_sinal += "\n"

        # Gestão de banca específica por tipo de jogo
        if jogo_escolhido in ["Aviator", "Mines", "Crash"]:
            mensagem_sinal += (
                f"**PLANO DE AÇÃO (JOGOS RÁPIDOS):**\n"
                f"1️⃣ **Entrada Principal (2% da banca)**\n"
                f"2️⃣ **1ª Proteção (4% da banca)**\n"
                f"3️⃣ **2ª Proteção (8% da banca)**\n\n"
            )
        elif jogo_escolhido in ["Futebol", "UFC", "Basquete"]:
            mensagem_sinal += (
                f"**PLANO DE AÇÃO (APOSTAS ESPORTIVAS):**\n"
                f"1️⃣ **Aposta Única (5% da banca)**\n"
                f"💡 *Não recomendamos gales em esportes*\n\n"
            )
        else:
            mensagem_sinal += (
                f"**PLANO DE AÇÃO (CASSINO):**\n"
                f"1️⃣ **Entrada Principal (4% da banca)**\n"
            )
            if cobertura:
                mensagem_sinal += f"   ↳ *Opcional: 1% da banca na Cobertura*\n"
            
            mensagem_sinal += (
                f"2️⃣ **1ª Proteção (Gale 1 - 8% da banca)**\n"
                f"3️⃣ **2ª Proteção (Gale 2 - 16% da banca)**\n\n"
            )

        mensagem_sinal += f"⚠️ *Sinais otimizados para a plataforma que recomendamos.*"

        await msg_analise.delete()
        msg_sinal_enviada = await context.bot.send_message(
            chat_id=CANAL_ID,
            text=mensagem_sinal,
            parse_mode='Markdown',
            reply_markup=teclado_sinal
        )
        logger.info(f"Sinal enviado para {jogo_escolhido}: {aposta_principal}. Aguardando resultado.")
        
        # ETAPA 3: RESULTADO PASSO A PASSO
        
        # Simula se o resultado foi Cobertura (chance baixa)
        if cobertura and random.random() < 0.10: # 10% de chance de dar cobertura
            await asyncio.sleep(random.randint(80, 100))
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NA COBERTURA!** ✅✅✅\n\n💰 **LUCRO MASSIVO!**\nA aposta principal foi devolvida e a cobertura multiplicou a banca!\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_EMPATE, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return

        # TENTATIVA 1: ENTRADA PRINCIPAL
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.65: # 65% de chance de win na entrada
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NA ENTRADA!** ✅✅✅\n\n💰 **LUCRO!**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_ENTRADA, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return # Encerra o ciclo com sucesso

        # Se chegou aqui, a entrada não bateu. Avisa e vai para o GALE 1.
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Não bateu!** Vamos para a primeira proteção.\n\nAcionando **Gale 1**...", reply_to_message_id=msg_sinal_enviada.message_id)
        
        # TENTATIVA 2: GALE 1
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.75: # 75% de chance de win no gale 1
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 1!** ✅✅✅\n\n💰 **LUCRO!**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE1, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return # Encerra o ciclo com sucesso

        # Se chegou aqui, o GALE 1 não bateu. Avisa e vai para o GALE 2.
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Ainda não veio!** Usando nossa última proteção.\n\nAcionando **Gale 2**...", reply_to_message_id=msg_sinal_enviada.message_id)

        # TENTATIVA 3: GALE 2
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.85: # 85% de chance de win no gale 2
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 2!** ✅✅✅\n\n💰 **LUCRO!**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE2, caption=resultado_msg)
            await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode='Markdown', disable_web_page_preview=False)
            return # Encerra o ciclo com sucesso

        # Se chegou até aqui, todas as tentativas falharam. É RED.
        bot_data["diario_loss"] += 1
        placar = f"📊 Placar do dia: {bot_data['diario_win']}W / {bot_data['diario_loss']}L"
        resultado_msg = f"❌❌❌ **RED!** ❌❌❌\n\nO mercado não foi a nosso favor. Disciplina é a chave. Voltaremos mais fortes na próxima!\n\n{placar}"
        await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_LOSS, caption=resultado_msg)
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
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo, parse_mode='Markdown')
    logger.info("Resumo diário enviado.")
    
    bot_data["diario_win"] = 0
    bot_data["diario_loss"] = 0

# --- Tutoriais rápidos e dicas ---
TUTORIAIS = {
    "gestao_banca": """
🎯 **TUTORIAL RÁPIDO: GESTÃO DE BANCA** 🎯

A gestão de banca é a diferença entre lucrar consistentemente e perder tudo. Siga estas regras de ouro:

📊 **Regra dos 5%:** Nunca aposte mais que 5% da sua banca total em uma única entrada.

🔄 **Progressão Segura:** 
- Entrada: 2-4% da banca
- Gale 1: 4-8% da banca  
- Gale 2: 8-16% da banca

🛑 **Stop Loss:** Defina um limite diário de perda (ex: 20% da banca) e PARE ao atingir.

💰 **Stop Gain:** Ao lucrar 50-100% da banca, retire parte dos lucros.

🧠 **Disciplina:** A emoção é inimiga do lucro. Siga sempre seu plano!
    """,
    
    "leitura_sinais": """
🔍 **TUTORIAL: COMO LER NOSSOS SINAIS** 🔍

Nossos sinais são estruturados para maximizar seus lucros:

🎯 **APOSTA PRINCIPAL:** Onde você deve focar sua entrada
📊 **ODDS:** Multiplicador esperado do retorno
⏱️ **TEMPO:** Duração estimada da rodada
🧠 **ESTRATÉGIA:** Método usado pela nossa I.A.
🛡️ **COBERTURA:** Proteção opcional (quando disponível)

💡 **DICA PRO:** Sempre aguarde a confirmação completa do sinal antes de apostar!

🚨 **IMPORTANTE:** Sinais são otimizados para a plataforma que recomendamos. Outras casas podem ter resultados diferentes.
    """,
    
    "psicologia_trader": """
🧠 **PSICOLOGIA DO TRADER VENCEDOR** 🧠

O sucesso no iGaming é 80% mental e 20% técnico:

😌 **Controle Emocional:** Nunca aposte com raiva ou desespero
📈 **Visão de Longo Prazo:** Foque no lucro mensal, não diário
🎯 **Disciplina:** Siga SEMPRE seu plano de gestão
💪 **Resiliência:** Perdas fazem parte. Aprenda e evolua.
🧘 **Paciência:** Os melhores sinais valem a espera

🏆 **MINDSET VENCEDOR:** "Eu sou um investidor, não um apostador"
    """
}

# --- Desafios semanais ---
DESAFIOS_SEMANAIS = [
    {
        "titulo": "🏆 DESAFIO DA SEMANA: DISCIPLINA TOTAL",
        "descricao": "Siga EXATAMENTE a gestão de banca sugerida em todos os sinais desta semana",
        "premio": "🎁 Bônus especial de 50% no próximo depósito",
        "meta": "7 dias seguindo a gestão correta"
    },
    {
        "titulo": "💎 DESAFIO: TRADER CONSISTENTE", 
        "descricao": "Obtenha lucro positivo em pelo menos 5 dos 7 dias da semana",
        "premio": "🏅 Acesso antecipado aos sinais VIP por 1 semana",
        "meta": "5 dias lucrativos na semana"
    },
    {
        "titulo": "🚀 DESAFIO: MULTIPLICADOR MASTER",
        "descricao": "Acerte 3 sinais consecutivos seguindo nossa estratégia",
        "premio": "💰 Cashback de 25% nas perdas da próxima semana", 
        "meta": "3 greens seguidos"
    }
]

# --- Mensagens motivacionais ---
MENSAGENS_MOTIVACIONAIS = [
    "💪 **LEMBRE-SE:** Cada grande trader começou exatamente onde você está agora!",
    "🎯 **FOCO:** Disciplina hoje = Liberdade financeira amanhã!",
    "🚀 **MINDSET:** Você não está apostando, está INVESTINDO no seu futuro!",
    "💎 **PERSISTÊNCIA:** Os diamantes são formados sob pressão. Continue firme!",
    "🏆 **SUCESSO:** Não é sobre acertar sempre, é sobre gerenciar bem quando erra!",
    "🧠 **INTELIGÊNCIA:** O trader inteligente sabe quando parar e quando continuar!",
    "💰 **RIQUEZA:** Pequenos lucros consistentes constroem grandes fortunas!",
    "⚡ **ENERGIA:** Sua dedicação de hoje é o seu sucesso de amanhã!"
]

# --- Mensagens de confiança ---
MENSAGENS_CONFIANCA = [
    """
🛡️ **POR QUE CONFIAR EM NOSSOS SINAIS?** 🛡️

✅ **I.A. Avançada:** Algoritmos que analisam milhares de padrões
✅ **Histórico Comprovado:** Mais de 70% de assertividade
✅ **Transparência Total:** Mostramos wins E losses
✅ **Suporte 24/7:** Estamos sempre aqui para você
✅ **Comunidade Ativa:** Milhares de traders lucrando juntos

🎯 **RESULTADO:** Mais de R$ 2.5 milhões em lucros gerados para nossa comunidade!
    """,
    
    """
📊 **NOSSOS NÚMEROS FALAM POR SI** 📊

📈 **Última semana:** 73% de assertividade
💰 **Lucro médio:** +15% da banca por semana  
👥 **Traders ativos:** +5.000 membros
🏆 **Melhor sequência:** 12 greens consecutivos
⭐ **Satisfação:** 4.8/5 estrelas da comunidade

🚀 **JUNTE-SE AOS VENCEDORES!**
    """
]
async def enviar_prova_social_agendada(context: ContextTypes.DEFAULT_TYPE):
    try:
        prova_social_url = random.choice(PROVAS_SOCIAIS)
        await context.bot.send_photo(chat_id=CANAL_ID, photo=prova_social_url, caption="""
✨ **Nossos membros estão lucrando!** ✨

Veja os resultados reais da nossa comunidade. Junte-se a nós e comece a transformar seus dias!

👉 [**Clique aqui para se cadastrar e lucrar também!**]({URL_CADASTRO})
""", parse_mode='Markdown')
        logger.info(f"Prova social agendada enviada: {prova_social_url}")
    except Exception as e:
        logger.error(f"Erro ao enviar prova social agendada: {e}")

# --- Funções para botões interativos ---
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'resultados':
        win_count = context.application.bot_data.get("diario_win", 0)
        loss_count = context.application.bot_data.get("diario_loss", 0)
        total = win_count + loss_count
        taxa_acerto = (win_count / total * 100) if total > 0 else 0
        
        await query.edit_message_text(
            text=f"📊 **RESULTADOS DE HOJE** 📊\n\n"
                 f"✅ **Greens:** {win_count}\n"
                 f"❌ **Reds:** {loss_count}\n"
                 f"📈 **Taxa de Acerto:** {taxa_acerto:.1f}%\n\n"
                 f"Continue acompanhando para mais sinais!",
            parse_mode='Markdown'
        )
    elif query.data == 'escolher_jogo':
        keyboard = [
            [InlineKeyboardButton("🎲 Bac Bo", callback_data='info_bacbo'),
             InlineKeyboardButton("🎰 Roleta", callback_data='info_roleta')],
            [InlineKeyboardButton("🃏 Blackjack", callback_data='info_blackjack'),
             InlineKeyboardButton("✈️ Aviator", callback_data='info_aviator')],
            [InlineKeyboardButton("⛏️ Mines", callback_data='info_mines'),
             InlineKeyboardButton("💥 Crash", callback_data='info_crash')],
            [InlineKeyboardButton("⚽ Futebol", callback_data='info_futebol'),
             InlineKeyboardButton("🥊 UFC", callback_data='info_ufc')],
            [InlineKeyboardButton("🏀 Basquete", callback_data='info_basquete')],
            [InlineKeyboardButton("↩️ Voltar ao Menu", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🎮 **ESCOLHA SEU JOGO FAVORITO** 🎮\n\nClique para ver informações e estratégias:",
            reply_markup=reply_markup
        )
    elif query.data.startswith('info_'):
        game_type = query.data.replace('info_', '')
        game_info = {
            'bacbo': "🎲 **BAC BO**\n\nJogo de cartas rápido com 3 opções: Banker, Player ou Empate.\n\n🎯 **Estratégia:** Análise de padrões das últimas rodadas\n⏱️ **Duração:** 30-45 segundos\n📊 **Odds:** 1.95x",
            'roleta': "🎰 **ROLETA**\n\nClássico jogo de cassino com múltiplas opções de aposta.\n\n🎯 **Estratégia:** Fibonacci + análise de setores\n⏱️ **Duração:** 60-90 segundos\n📊 **Odds:** 2.0x",
            'blackjack': "🃏 **BLACKJACK**\n\nJogo de cartas onde o objetivo é chegar próximo a 21.\n\n🎯 **Estratégia:** Contagem básica + gestão\n⏱️ **Duração:** 45-60 segundos\n📊 **Odds:** 1.95x",
            'aviator': "✈️ **AVIATOR**\n\nJogo de multiplicador que pode 'crashar' a qualquer momento.\n\n🎯 **Estratégia:** Análise de volatilidade\n⏱️ **Duração:** 8-15 segundos\n📊 **Odds:** Variável",
            'mines': "⛏️ **MINES**\n\nCampo minado com diferentes níveis de risco e recompensa.\n\n🎯 **Estratégia:** Probabilidade matemática\n⏱️ **Duração:** Instantâneo\n📊 **Odds:** 1.2x - 50x",
            'crash': "💥 **CRASH**\n\nMultiplicador que cresce até 'crashar' aleatoriamente.\n\n🎯 **Estratégia:** Análise de tendências\n⏱️ **Duração:** 5-20 segundos\n📊 **Odds:** Variável",
            'futebol': "⚽ **FUTEBOL**\n\nApostas em partidas de futebol ao vivo e pré-jogo.\n\n🎯 **Estratégia:** Análise estatística + forma\n⏱️ **Duração:** 90 minutos\n📊 **Odds:** 1.80x - 2.50x",
            'ufc': "🥊 **UFC**\n\nApostas em lutas de MMA com diversos mercados.\n\n🎯 **Estratégia:** Histórico + estilo de luta\n⏱️ **Duração:** 15-25 minutos\n📊 **Odds:** 1.50x - 4.00x",
            'basquete': "🏀 **BASQUETE**\n\nApostas em jogos da NBA, NBB e outras ligas.\n\n🎯 **Estratégia:** Ritmo + defesas\n⏱️ **Duração:** 48 minutos\n📊 **Odds:** 1.85x - 2.10x"
        }
        
        keyboard = [[InlineKeyboardButton("↩️ Voltar aos Jogos", callback_data='escolher_jogo')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=game_info.get(game_type, "Informações não disponíveis"),
            reply_markup=reply_markup
        )
    elif query.data.startswith('tutorial_'):
        tutorial_type = query.data.replace('tutorial_', '')
        tutorial_map = {
            'gestao': 'gestao_banca',
            'sinais': 'leitura_sinais', 
            'psicologia': 'psicologia_trader'
        }
        
        tutorial_content = TUTORIAIS.get(tutorial_map.get(tutorial_type, ''), "Tutorial não encontrado")
        
        keyboard = [[InlineKeyboardButton("↩️ Voltar aos Tutoriais", callback_data='menu_tutoriais')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=tutorial_content,
            reply_markup=reply_markup
        )
    elif query.data == 'menu_tutoriais':
        keyboard = [
            [InlineKeyboardButton("🎯 Gestão de Banca", callback_data='tutorial_gestao')],
            [InlineKeyboardButton("🔍 Leitura de Sinais", callback_data='tutorial_sinais')],
            [InlineKeyboardButton("🧠 Psicologia do Trader", callback_data='tutorial_psicologia')],
            [InlineKeyboardButton("↩️ Voltar ao Menu", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📚 **TUTORIAIS DISPONÍVEIS** 📚\n\nEscolha o tutorial que deseja acessar:",
            reply_markup=reply_markup
        )
    elif query.data == 'desafio_semanal':
        desafio_atual = random.choice(DESAFIOS_SEMANAIS)
        keyboard = [[InlineKeyboardButton("↩️ Voltar ao Menu", callback_data='menu_principal')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"🏆 **{desafio_atual['titulo']}** 🏆\n\n"
                 f"📋 **DESCRIÇÃO:** {desafio_atual['descricao']}\n\n"
                 f"🎯 **META:** {desafio_atual['meta']}\n\n"
                 f"🏆 **PRÊMIO:** {desafio_atual['premio']}\n\n"
                 f"💪 **Aceite o desafio e prove que você é um trader de elite!**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif query.data == 'motivacao_diaria':
        mensagem = random.choice(MENSAGENS_MOTIVACIONAIS)
        confianca = random.choice(MENSAGENS_CONFIANCA)
        keyboard = [[InlineKeyboardButton("↩️ Voltar ao Menu", callback_data='menu_principal')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"{mensagem}\n\n{confianca}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif query.data == 'menu_principal':
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
        await query.edit_message_text(
            text="🎯 **MENU PRINCIPAL** 🎯\n\n🌈 **ESCOLHA SUA JORNADA PARA O SUCESSO:**",
            reply_markup=reply_markup
        )

# --- 6. FUNÇÃO PRINCIPAL QUE INICIA TUDO ---
def main():
    logger.info("Iniciando o bot...")
    
    application = Application.builder().token(BOT_TOKEN).post_init(inicializar_contadores).build()

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
    
    # Agendamento de sinais com intervalos variados para maior engajamento
    # Manhã: 10-15 minutos (mais ativo)
    job_queue.run_repeating(enviar_sinal, interval=random.randint(600, 900), first=10, name="sinais_manha")
    
    # Tarde: 15-20 minutos  
    job_queue.run_repeating(enviar_sinal, interval=random.randint(900, 1200), first=300, name="sinais_tarde")
    
    # Noite: 12-18 minutos (horário nobre)
    job_queue.run_repeating(enviar_sinal, interval=random.randint(720, 1080), first=600, name="sinais_noite")
    
    # Agendamento do resumo diário
    job_queue.run_daily(resumo_diario, time=time(hour=22, minute=0))

    # Agendamento das provas sociais 4 vezes ao dia
    job_queue.run_daily(enviar_prova_social_agendada, time=time(hour=9, minute=30))
    job_queue.run_daily(enviar_prova_social_agendada, time=time(hour=14, minute=15))
    job_queue.run_daily(enviar_prova_social_agendada, time=time(hour=18, minute=45))
    job_queue.run_daily(enviar_prova_social_agendada, time=time(hour=21, minute=20))

    # Mensagens motivacionais em horários estratégicos
    job_queue.run_daily(lambda context: context.bot.send_message(
        chat_id=CANAL_ID, 
        text=f"🌅 **BOM DIA, TRADERS!** 🌅\n\n{random.choice(MENSAGENS_MOTIVACIONAIS)}\n\n🚀 **Que hoje seja um dia de grandes lucros!**",
        parse_mode='Markdown'
    ), time=time(hour=8, minute=0))
    
    job_queue.run_daily(lambda context: context.bot.send_message(
        chat_id=CANAL_ID,
        text=f"🌆 **BOA TARDE!** 🌆\n\n{random.choice(MENSAGENS_MOTIVACIONAIS)}\n\n💎 **Continue focado nos seus objetivos!**",
        parse_mode='Markdown'
    ), time=time(hour=14, minute=0))
    
    job_queue.run_daily(lambda context: context.bot.send_message(
        chat_id=CANAL_ID,
        text=f"🌙 **BOA NOITE, TRADERS!** 🌙\n\n{random.choice(MENSAGENS_MOTIVACIONAIS)}\n\n⭐ **Descanse bem para amanhã lucrar mais!**",
        parse_mode='Markdown'
    ), time=time(hour=20, minute=30))

    # Lembretes de bônus em horários estratégicos
    job_queue.run_daily(lambda context: context.bot.send_message(chat_id=CANAL_ID, text=f"""
🎉 **BÔNUS MATINAL EXCLUSIVO!** 🎉

☀️ Comece o dia com o pé direito! Seu bônus de boas-vindas está esperando!

✅ **VANTAGENS EXCLUSIVAS:**
💰 Bônus de até 500% no primeiro depósito
🎁 Giros grátis diários
🏆 Participação em sorteios milionários
🎯 Cashback semanal

👉 [**ATIVE SEU BÔNUS AGORA!**]({URL_CADASTRO})

⏰ **Oferta por tempo limitado!**
""", parse_mode='Markdown', disable_web_page_preview=False), time=time(hour=10, minute=30))

    job_queue.run_daily(lambda context: context.bot.send_message(chat_id=CANAL_ID, text=f"""
🔥 **ÚLTIMA CHANCE DO DIA!** 🔥

🌅 Não deixe o sol se pôr sem garantir seu bônus exclusivo!

🚀 **APROVEITE AGORA:**
💎 Bônus premium de boas-vindas
🎰 Acesso a jogos VIP
📈 Sinais exclusivos para novos membros
🏅 Status de trader premium

👉 [**GARANTA JÁ SEU BÔNUS!**]({URL_CADASTRO})

💪 **Amanhã pode ser tarde demais!**
""", parse_mode='Markdown', disable_web_page_preview=False), time=time(hour=19, minute=15))

    # Mensagens de confiança e credibilidade
    job_queue.run_daily(lambda context: context.bot.send_message(
        chat_id=CANAL_ID,
        text=random.choice(MENSAGENS_CONFIANCA),
        parse_mode='Markdown'
    ), time=time(hour=16, minute=30))

    # Desafio semanal (toda segunda-feira)
    job_queue.run_daily(lambda context: context.bot.send_message(
        chat_id=CANAL_ID,
        text=f"🏆 **NOVO DESAFIO SEMANAL!** 🏆\n\n{random.choice(DESAFIOS_SEMANAIS)['titulo']}\n\n💪 **Use /desafio para ver os detalhes completos!**\n\n🎯 **Prove que você é um trader de elite!**",
        parse_mode='Markdown'
    ), time=time(hour=9, minute=0, weekday=0))  # Segunda-feira

    # Tutorial da semana (toda quarta-feira)
    job_queue.run_daily(lambda context: context.bot.send_message(
        chat_id=CANAL_ID,
        text="📚 **TUTORIAL DA SEMANA!** 📚\n\n🧠 **Dica Pro:** Use /tutorial para acessar nossos guias completos!\n\n🎯 **Conhecimento é poder no mundo do trading!**",
        parse_mode='Markdown'
    ), time=time(hour=15, minute=0, weekday=2))  # Quarta-feira

    logger.info("Bot iniciado e tarefas agendadas. O bot está online e operando.")
    
    application.run_polling()

if __name__ == "__main__":
    main()


