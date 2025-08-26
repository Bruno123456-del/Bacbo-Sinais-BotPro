# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 5.0 "BILLIONAIRE'S STRATEGY"
# CRIADO E APRIMORADO POR MANUS
# FOCO EM FUNIL DE CONVERSÃO, ESCASSEZ, URGÊNCIA E VALOR PERCEBIDO
# ===================================================================================

# ... (Importações e configurações básicas permanecem as mesmas) ...
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
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://seu-link-aqui.com" )
ADMIN_ID = 5011424031
### NOVO: Link para o seu Grupo VIP (pode ser um link de convite) ###
LINK_GRUPO_VIP = os.getenv("LINK_GRUPO_VIP", "https://t.me/seu_grupo_vip_privado" )

if not BOT_TOKEN or CANAL_ID == "0" or URL_CADASTRO == "https://seu-link-aqui.com":
    raise ValueError("ERRO CRÍTICO: Variáveis de ambiente não configuradas!" )
CANAL_ID = int(CANAL_ID)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ... (Mídias e outras mensagens permanecem as mesmas) ...
IMG_WIN = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_COMEMORACAO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"


# -----------------------------------------------------------------------------------
# 3. BANCO DE MENSAGENS E ESTRATÉGIAS DE MARKETING (ATUALIZADO )
# -----------------------------------------------------------------------------------

### NOVO: Mensagens focadas na conversão para o VIP ###
MARKETING_MESSAGES = {
    "oferta_vip": (
        f"💎 **QUER ACESSO AO NOSSO GRUPO VIP 100% DE GRAÇA?** 💎\n\n"
        f"Chega de pegar poucos sinais! No nosso Grupo VIP, as operações são **24 horas por dia**, com análises exclusivas e estratégias que não postamos aqui.\n\n"
        f"**Para entrar é simples:**\n"
        f"1️⃣ **Cadastre-se** na plataforma através do nosso link oficial: [CLIQUE AQUI]({URL_CADASTRO})\n"
        f"2️⃣ Faça seu **primeiro depósito** (de qualquer valor).\n"
        f"3️⃣ **Envie o comprovante** para o nosso suporte (@seu_usuario_de_suporte) e receba seu acesso vitalício!\n\n"
        f"Você não paga NADA a mais por isso. Apenas usa a plataforma correta e ganha acesso a um mundo de oportunidades. Vagas limitadas!"
    ),
    "estrategia_secreta": (
        f"🤫 **A ESTRATÉGIA DOS GIGANTES...**\n\n"
        f"Você sabia que os maiores players não contam apenas com sinais? Eles usam uma **estratégia de alavancagem com Martingale Inteligente** para otimizar os lucros e proteger a banca.\n\n"
        f"Essa e outras estratégias avançadas são reveladas **apenas no nosso Grupo VIP**. Enquanto você pega 10 sinais aqui, lá dentro eles já fizeram 50 operações.\n\n"
        f"Não fique para trás. [**GARANTA SEU ACESSO VIP AGORA!**]({URL_CADASTRO})"
    ),
    "escassez": (
        f"🏃‍♂️💨 **ÚLTIMAS VAGAS PARA O VIP!**\n\n"
        f"Devido à alta demanda, estamos prestes a **encerrar o acesso gratuito** ao Grupo VIP através do cadastro e depósito. Esta pode ser sua última chance de entrar sem custos!\n\n"
        f"✅ Sinais 24/7\n"
        f"✅ Estratégias Exclusivas\n"
        f"✅ Suporte Prioritário\n\n"
        f"Não perca tempo! [**CLIQUE AQUI, CADASTRE-SE E GARANTA SUA VAGA!**]({URL_CADASTRO})"
    )
}

# -----------------------------------------------------------------------------------
# 4. LÓGICA PRINCIPAL DO BOT (COM AGENDAMENTO PRECISO)
# -----------------------------------------------------------------------------------

async def inicializar_estado(app: Application):
    """Prepara o estado inicial do bot."""
    bd = app.bot_data
    bd["sinal_em_andamento"] = False
    bd["manutencao"] = False
    logger.info("Estado do bot inicializado para a Estratégia Bilionária.")

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str):
    """Função otimizada para enviar um sinal específico agendado."""
    bd = context.bot_data
    if bd.get("sinal_em_andamento"):
        logger.warning(f"Pulei o sinal de {jogo} pois outro já estava em andamento.")
        return
        
    bd["sinal_em_andamento"] = True
    
    try:
        # Etapa 1: Análise Rápida
        await context.bot.send_animation(
            chat_id=CANAL_ID,
            animation=GIF_ANALISANDO,
            caption=f"🔎 Analisando padrões para a entrada em **{jogo.upper()}**... Fiquem atentos!"
        )
        await asyncio.sleep(random.randint(10, 20))

        # Etapa 2: Envio do Sinal
        mensagem_sinal = (
            f"🔥 **ENTRADA CONFIRMADA - {jogo.upper()}** 🔥\n\n"
            f"🎯 **Aposta:** {aposta}\n"
            f"🛡️ **Proteção:** Usar até 2 gales, se necessário.\n\n"
            f"🔗 **[ENTRAR NA PLATAFORMA CORRETA]({URL_CADASTRO})**\n\n"
            f"✨ *No Grupo VIP, as análises como esta são 24h!*"
        )
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal agendado enviado para {jogo}: {aposta}.")

        # Etapa 3: Resultado (Simulação)
        await asyncio.sleep(random.randint(60, 90))
        resultado = random.choices(["win", "loss"], weights=[85, 15], k=1)[0] # Alta assertividade para a isca

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
    """Envia uma mensagem de marketing específica."""
    mensagem = MARKETING_MESSAGES.get(tipo_mensagem)
    if mensagem:
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem, parse_mode='Markdown', disable_web_page_preview=False)
        logger.info(f"Mensagem de marketing '{tipo_mensagem}' enviada.")

# -----------------------------------------------------------------------------------
# 5. AGENDAMENTO E TAREFAS RECORRENTES (O CORAÇÃO DO FUNIL)
# -----------------------------------------------------------------------------------

def agendar_tarefas(app: Application):
    """Agenda todos os sinais e mensagens de marketing."""
    jq = app.job_queue

    # --- Bloco da Manhã (09:00 - 10:00) ---
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Vermelho ⚫"), time=time(hour=9, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "3 Minas - Abrir 7 campos"), time=time(hour=9, minute=35))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Aviator ✈️", "Buscar vela de 1.80x"), time=time(hour=10, minute=5))
    jq.run_daily(lambda ctx: enviar_mensagem_marketing(ctx, "oferta_vip"), time=time(hour=10, minute=30))

    # --- Bloco da Tarde (14:00 - 15:00) ---
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Bac Bo 🎲", "Player 🔵"), time=time(hour=14, minute=10))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Futebol (Gols) 🥅", "Mais de 1.5 Gols"), time=time(hour=14, minute=40))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Ímpar"), time=time(hour=15, minute=15))
    jq.run_daily(lambda ctx: enviar_mensagem_marketing(ctx, "estrategia_secreta"), time=time(hour=15, minute=45))

    # --- Bloco da Noite (20:00 - 21:00) ---
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Aviator ✈️", "Buscar vela de 2.10x"), time=time(hour=20, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "5 Minas - Abrir 4 campos"), time=time(hour=20, minute=35))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Bac Bo 🎲", "Banker 🔴"), time=time(hour=21, minute=5))
    jq.run_daily(lambda ctx: enviar_mensagem_marketing(ctx, "escassez"), time=time(hour=21, minute=30))

    # --- Bloco do Fim da Noite (23:00 - 00:00) ---
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Roleta", "Preto ⚫"), time=time(hour=23, minute=5))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Futebol (Gols) 🥅", "Menos de 3.5 Gols"), time=time(hour=23, minute=30))
    jq.run_daily(lambda ctx: enviar_sinal_especifico(ctx, "Mines 💣", "3 Minas - Abrir 5 campos"), time=time(hour=23, minute=55))
    
    logger.info("Todos os sinais e mensagens de marketing foram agendados com sucesso.")

# -----------------------------------------------------------------------------------
# 6. COMANDOS DE USUÁRIO E PAINEL DE ADMIN
# -----------------------------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mensagem de boas-vindas focada na conversão."""
    await update.message.reply_text(
        text=MARKETING_MESSAGES["oferta_vip"],
        parse_mode='Markdown'
    )

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Painel de admin simplificado para a nova estratégia."""
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
    """Processa os cliques do painel de admin."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'admin_forcar_sinal':
        await query.edit_message_text("✅ Forçando um sinal de Roleta agora...")
        await enviar_sinal_especifico(context, "Roleta (Teste)", "Cor Aleatória")
    elif query.data == 'admin_enviar_oferta_vip':
        await query.edit_message_text("✅ Enviando a oferta VIP para o canal...")
        await enviar_mensagem_marketing(context, "oferta_vip")
    # ... (outros callbacks se necessário)

# -----------------------------------------------------------------------------------
# 7. FUNÇÃO PRINCIPAL (MAIN)
# -----------------------------------------------------------------------------------
def main() -> None:
    """Função principal que constrói, configura e inicia o bot."""
    logger.info("Iniciando o bot - Versão 5.0 'Billionaire's Strategy'...")
    
    app = Application.builder().token(BOT_TOKEN).post_init(inicializar_estado).build()

    # --- Handlers ---
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("admin", admin_command, filters=filters.User(user_id=ADMIN_ID)))
    app.add_handler(CallbackQueryHandler(admin_callbacks, pattern='^admin_'))

    # --- Agendamento ---
    agendar_tarefas(app)

    logger.info("Bot iniciado. O funil de conversão está ativo.")
    app.run_polling()

if __name__ == "__main__":
    main()
