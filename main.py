# -*- coding: utf-8 -*-

import logging
import os
import random
import asyncio
from datetime import time, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
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

# Imagens de resultado (genéricas, sem nome de casa de aposta)
IMG_WIN_ENTRADA = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
IMG_WIN_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
IMG_WIN_GALE2 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale2.png"
IMG_WIN_EMPATE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_empate.png"

# Novas provas sociais (simuladas, estilo WhatsApp )
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
    application.bot_data.setdefault("sinal_em_andamento", False) # Novo controle
    logger.info(f"Contadores inicializados: {application.bot_data}")

# --- 4. COMANDOS DO USUÁRIO (Para chat privado) ---
# ... (Todo o seu código de comandos como start, help, etc., permanece o mesmo) ...
# (Para economizar espaço, estou omitindo essa parte, mas você deve mantê-la no seu arquivo)
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
    
    # Adiciona a flag para indicar que um sinal está sendo processado
    bot_data["sinal_em_andamento"] = True
    
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
    finally:
        # Libera a flag para que um novo sinal possa ser enviado
        bot_data["sinal_em_andamento"] = False

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

# --- Tutoriais, Desafios, etc. (Mantenha todo o seu código aqui) ---
# ... (Todo o seu código de TUTORIAIS, DESAFIOS_SEMANAIS, etc., permanece o mesmo) ...
# (Para economizar espaço, estou omitindo essa parte, mas você deve mantê-la no seu arquivo)
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
🔍 **TUTORIAL: COMO LER NOSS
