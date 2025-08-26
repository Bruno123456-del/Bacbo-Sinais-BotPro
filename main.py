# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 4.0 "ULTIMATE EDITION"
# CRIADO E APRIMORADO POR MANUS
# FOCO EM VARIEDADE, ENGAJAMENTO, RETENÇÃO E CONVERSÃO
# ===================================================================================

# -----------------------------------------------------------------------------------
# 1. IMPORTAÇÕES E CONFIGURAÇÃO GERAL
# -----------------------------------------------------------------------------------
import logging
import os
import random
import asyncio
from datetime import time, datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, filters
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# -----------------------------------------------------------------------------------
# 2. CONFIGURAÇÕES ESSENCIAIS E VARIÁVEIS GLOBAIS
# -----------------------------------------------------------------------------------
# --- Credenciais e IDs ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CANAL_ID = os.getenv("CANAL_ID", "0").strip()
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://seu-link-aqui.com" )
ADMIN_ID = 5011424031  # SEU ID DE ADMINISTRADOR

# --- Validação Crítica ---
if not BOT_TOKEN or CANAL_ID == "0" or URL_CADASTRO == "https://seu-link-aqui.com":
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN, CANAL_ID ou URL_CADASTRO não foram configurados corretamente!" )
CANAL_ID = int(CANAL_ID)

# --- Configuração do Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------------
# 3. BANCO DE MENSAGENS, MÍDIAS E ESTRATÉGIAS DE MARKETING
# -----------------------------------------------------------------------------------

# --- Mídias ---
IMG_WIN = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_entrada.png"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
IMG_GALE2 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale2.png"
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_COMEMORACAO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"
GIF_META_BATIDA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3JvZ3g1cWJqY2w4eXJqZzZzZzZzZzZzZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
GIF_GESTAO_BANCA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXNseW5qZ3N2aWJsczZzNmVqN213bHk5a3k0d2w5b3M0cTlncDA5eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/d5wVJ95YvXLEbE4vK/giphy.gif"

# --- Provas Sociais (Adicione os links diretos para suas imagens ) ---
PROVAS_SOCIAIS = [
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova1.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova2.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova3.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova4.png",
    "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova5.png",
    # Adicione quantas provas quiser
]

# --- Mensagens de Marketing (para maximizar conversão ) ---
MARKETING_MESSAGES = [
    f"🤔 **Ainda não se cadastrou?** Para ter EXATAMENTE os mesmos resultados que nós, é essencial usar a plataforma para a qual nossa IA é calibrada. \n\n👉 [**CADASTRE-SE AQUI E GANHE BÔNUS**]({URL_CADASTRO})\n\nNão arrisque seu dinheiro em outra!",
    f"💰 **QUER LUCRAR DE VERDADE?** Nossos sinais são otimizados para uma plataforma específica. Cadastre-se pelo nosso link e ganhe benefícios exclusivos! \n\n👉 [**CLIQUE AQUI PARA SE CADASTRAR**]({URL_CADASTRO})",
    f"⚠️ **AVISO IMPORTANTE:** Jogar em outra plataforma pode invalidar nossos sinais. Garanta sua segurança e seus lucros, jogue na plataforma certa! \n\n👉 [**CADASTRE-SE COM SEGURANÇA AQUI**]({URL_CADASTRO})",
]

# --- Mensagens de Status "Humanizadas" ---
STATUS_MESSAGES = {
    "abertura_madrugada": "🦉 **Turno da Coruja iniciado!** Para quem não dorme no ponto, vamos buscar os greens da madrugada. A meta é **{meta_wins} WINS**. Foco total!",
    "abertura_manha": "☀️ **Bom dia, comunidade!** Iniciando as análises do dia. A meta da manhã é **{meta_wins} WINS**. Vamos com tudo! 👀",
    "abertura_tarde": "☕ **Boa tarde, pessoal!** Café tomado e análises a todo vapor. A meta da tarde é **{meta_wins} WINS**. Vamos buscar!",
    "abertura_noite": "🌙 **Boa noite, apostadores!** Começando o turno nobre. A meta da noite é **{meta_wins} WINS**. Prontos para forrar?",
    "abertura_fds": "🎉 **BOM FIM DE SEMANA!** Os mercados não param, e nós também não! Turno especial de FDS começando com meta de **{meta_wins} WINS**!",
    "fechamento": "⚫ **Operações encerradas por hoje!** Obrigado a todos que confiaram em nossas análises. O resumo final já foi enviado. Descansem, pois amanhã tem mais!",
    "pausa": "⏸️ **Pausa estratégica.** Momento de recalibrar a análise de mercado. Voltamos em breve com o próximo turno de sinais. Fiquem no aguardo!",
    "pausa_seguranca": "⚠️ **PAUSA DE SEGURANÇA** ⚠️ O mercado apresentou alta volatilidade. Pausando as operações por 20 minutos para proteger nosso capital. Disciplina é tudo!",
    "meta_batida": "🏆 **META DO TURNO ATINGIDA!** 🏆\n\nParabéns, comunidade! Batemos a meta de **{meta_wins} WINS**. Isso é resultado de análise, paciência e da força do nosso grupo. Vamos continuar lucrando com responsabilidade!",
    "gestao_banca": "🧠 **LEMBRETE DE GESTÃO DE BANCA** 🧠\n\nNunca entre com mais de 1% a 3% do seu capital total em uma única operação. A consistência é mais importante que um grande ganho isolado. Jogue com responsabilidade!",
}

# -----------------------------------------------------------------------------------
# 4. LÓGICA PRINCIPAL DO BOT
# -----------------------------------------------------------------------------------

async def inicializar_estado(app: Application):
    """Prepara o estado inicial do bot ao ser iniciado."""
    bd = app.bot_data
    bd["diario_win"] = 0
    bd["diario_loss"] = 0
    bd["win_streak"] = 0
    bd["loss_streak"] = 0
    bd["sinal_em_andamento"] = False
    bd["manutencao"] = False
    bd["meta_wins_turno"] = random.randint(5, 8)
    bd["meta_batida_turno"] = False
    bd["start_time"] = datetime.now()
    logger.info(f"Estado do bot inicializado. Meta do turno: {bd['meta_wins_turno']} WINS.")

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE, forcado_por_admin: bool = False):
    """Função completa para gerar e enviar um ciclo de sinal."""
    bd = context.bot_data
    if bd.get("sinal_em_andamento"):
        if forcado_por_admin:
            await context.bot.send_message(chat_id=ADMIN_ID, text="❌ Erro: Um sinal já está em andamento.")
        return
        
    bd["sinal_em_andamento"] = True
    
    try:
        # Etapa 1: Análise (com mensagens de pré-análise)
        analises_ficticias = [
            "📈 *Análise: Detectei uma forte tendência de quebra de padrão. Preparando uma entrada...*",
            "📊 *Análise: Padrão de velas indica uma oportunidade iminente. Fiquem a postos...*",
            "🤖 *IA BEEP BOOP: Calculando probabilidades... Oportunidade encontrada.*",
        ]
        if random.random() < 0.4: # 40% de chance de enviar uma pré-análise
            await context.bot.send_message(chat_id=CANAL_ID, text=random.choice(analises_ficticias), parse_mode='Markdown')
            await asyncio.sleep(random.randint(5, 10))

        caption_analise = "📡 Analisando o mercado... Buscando a melhor entrada para vocês!"
        if forcado_por_admin:
            caption_analise = "⚡ **SINAL MANUAL INICIADO PELO ADMIN** ⚡\n\n" + caption_analise
        msg_analise = await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_ANALISANDO, caption=caption_analise)
        await asyncio.sleep(random.randint(10, 15))

        # Etapa 2: Envio do Sinal (com novos jogos)
        jogos = {
            "Roleta 룰렛": {"entradas": ["Preto ⚫", "Vermelho 🔴", "Ímpar", "Par", "1ª Dúzia", "3ª Dúzia"]},
            "Bac Bo 🎲": {"entradas": ["Banker 🔴", "Player 🔵"]},
            "Mines 💣": {"entradas": ["3 Minas - Abrir 5 campos", "3 Minas - Abrir 7 campos", "5 Minas - Abrir 4 campos"]},
            "Aviator ✈️": {"entradas": ["Buscar vela de 1.50x", "Buscar vela de 2.00x"]},
            "Trade Esportivo ⚽": {"entradas": ["Over 0.5 HT (Gol no 1º Tempo)", "Ambas Marcam - Sim"]},
            "Futebol (Gols) 🥅": {"entradas": ["Mais de 1.5 Gols na Partida", "Menos de 3.5 Gols na Partida"]}
        }
        jogo_escolhido = random.choice(list(jogos.keys()))
        aposta = random.choice(jogos[jogo_escolhido]["entradas"])

        mensagem_sinal = (
            f"🔥 **ALERTA DE ENTRADA - {jogo_escolhido.upper()}** 🔥\n\n"
            f"🎯 **Entrada Sugerida:** {aposta}\n\n"
            f"**Plano de Ação:**\n"
            f"1️⃣ Fazer a entrada com gestão de banca.\n"
            f"2️⃣ Se aplicável, usar até 2 gales (não se aplica a Aviator/Futebol).\n\n"
            f"🔗 **[JOGUE NA PLATAFORMA CORRETA]({URL_CADASTRO})**"
        )
        await msg_analise.delete()
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal enviado para {jogo_escolhido}: {aposta}.")

        # Etapa 3: Resultado (Simulação)
        await asyncio.sleep(random.randint(45, 75))
        resultado = random.choices(["win", "gale1", "gale2", "loss"], weights=[65, 20, 5, 10], k=1)[0]
        
        caption, imagem = "", ""
        foi_green = False

        if resultado in ["win", "gale1", "gale2"]:
            foi_green = True
            bd["diario_win"] += 1
            bd["win_streak"] += 1
            bd["loss_streak"] = 0
            if resultado == "win":
                caption, imagem = "✅ GREEN DE PRIMEIRA! ✅", IMG_WIN
            elif resultado == "gale1":
                caption, imagem = "✅ GREEN NO GALE 1! ✅", IMG_GALE1
            else:
                caption, imagem = "✅ GREEN NO GALE 2! ✅", IMG_GALE2
        else: # Loss
            bd["diario_loss"] += 1
            bd["loss_streak"] += 1
            bd["win_streak"] = 0
            caption = "❌ RED! ❌\n\nInfelizmente não bateu. Disciplina e gestão sempre! Voltaremos mais fortes."
            imagem = GIF_LOSS

        placar = f"📊 Placar do Dia: {bd['diario_win']}W / {bd['diario_loss']}L"
        
        if bd["win_streak"] >= 3:
            caption += f"\n\n🔥🔥 **ESTAMOS NUMA SEQUÊNCIA DE {bd['win_streak']} WINS!** 🔥🔥"

        if isinstance(imagem, str) and "giphy.com" in imagem:
             await context.bot.send_animation(chat_id=CANAL_ID, animation=imagem, caption=f"{caption}\n\n{placar}")
        else:
             await context.bot.send_photo(chat_id=CANAL_ID, photo=imagem, caption=f"{caption}\n\n{placar}")

        if foi_green:
             await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_COMEMORACAO)
             await context.bot.send_message(chat_id=CANAL_ID, text=random.choice(MARKETING_MESSAGES), parse_mode='Markdown', disable_web_page_preview=False)
             
             if not bd.get("meta_batida_turno") and (bd["diario_win"] % bd["meta_wins_turno"] == 0):
                 bd["meta_batida_turno"] = True
                 await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_META_BATIDA)
                 await context.bot.send_message(chat_id=CANAL_ID, text=STATUS_MESSAGES["meta_batida"].format(meta_wins=bd['meta_wins_turno']))
        
        if bd["loss_streak"] >= 2:
            bd["loss_streak"] = 0
            await enviar_mensagem_status(context, STATUS_MESSAGES["pausa_seguranca"])
            await asyncio.sleep(1200)

    except Exception as e:
        logger.error(f"Erro no ciclo de sinal: {e}")
    finally:
        bd["sinal_em_andamento"] = False

# -----------------------------------------------------------------------------------
# 5. AGENDAMENTO E TAREFAS RECORRENTES
# -----------------------------------------------------------------------------------

async def agendador_principal(context: ContextTypes.DEFAULT_TYPE):
    """Verifica o horário e a probabilidade para enviar um sinal ou mensagem."""
    agora = datetime.now()
    bd = context.bot_data
    
    if bd.get("manutencao", False) or bd.get("sinal_em_andamento", False):
        return

    # Horários 24/7
    is_active_time = True 
    
    # Probabilidades variam com o horário para simular volume
    hora = agora.hour
    if 2 <= hora < 7: # Madrugada (menor frequência)
        prob_sinal = 1/25
        prob_extra = 1/90
    elif 12 <= hora < 14 or 18 <= hora < 20: # Pausas (menor frequência)
        prob_sinal = 1/30
        prob_extra = 1/120
    else: # Horários de pico
        prob_sinal = 1/15
        prob_extra = 1/60

    # Sorteio da Ação
    rand = random.random()
    if rand < prob_sinal:
        logger.info(f"Sorteado para enviar SINAL no horário {agora.time()}.")
        await enviar_sinal(context)
    elif rand < prob_sinal + prob_extra:
        # Sorteia entre marketing, gestão ou prova social
        extra_choice = random.choice(["marketing", "gestao", "prova"])
        if extra_choice == "marketing":
            logger.info(f"Sorteado para enviar MENSAGEM DE MARKETING no horário {agora.time()}.")
            await context.bot.send_message(chat_id=CANAL_ID, text=random.choice(MARKETING_MESSAGES), parse_mode='Markdown', disable_web_page_preview=False)
        elif extra_choice == "gestao":
            logger.info(f"Sorteado para enviar DICA DE GESTÃO no horário {agora.time()}.")
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_GESTAO_BANCA, caption=STATUS_MESSAGES["gestao_banca"], parse_mode='Markdown')
        elif extra_choice == "prova" and PROVAS_SOCIAIS:
            logger.info(f"Sorteado para enviar PROVA SOCIAL no horário {agora.time()}.")
            await context.bot.send_photo(chat_id=CANAL_ID, photo=random.choice(PROVAS_SOCIAIS), caption="🚀 Nossos membros também estão lucrando! Faça parte do time vencedor!")


async def enviar_mensagem_status(context: ContextTypes.DEFAULT_TYPE, mensagem: str):
    try:
        # Reseta a meta do turno a cada nova abertura
        context.bot_data["meta_wins_turno"] = random.randint(5, 8)
        context.bot_data["meta_batida_turno"] = False
        msg_formatada = mensagem.format(meta_wins=context.bot_data['meta_wins_turno'])
        await context.bot.send_message(chat_id=CANAL_ID, text=msg_formatada)
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem de status: {e}")

async def resumo_diario(context: ContextTypes.DEFAULT_TYPE):
    bd = context.bot_data
    wins = bd.get('diario_win', 0)
    losses = bd.get('diario_loss', 0)
    total = wins + losses
    assertividade = (wins / total * 100) if total > 0 else 0
    
    resumo = (
        f"📊 **RESUMO DO DIA** 📊\n\n"
        f"✅ **Greens:** {wins}\n"
        f"❌ **Reds:** {losses}\n"
        f"📈 **Assertividade:** {assertividade:.2f}%\n\n"
        f"Lembre-se: a consistência é a chave do sucesso. Para garantir os melhores resultados, opere na plataforma que recomendamos!\n"
        f"👉 [**CADASTRE-SE AQUI**]({URL_CADASTRO})"
    )
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo, parse_mode='Markdown')
    
    bd["diario_win"], bd["diario_loss"], bd["win_streak"], bd["loss_streak"] = 0, 0, 0, 0
    logger.info("Resumo diário enviado e contadores zerados.")

# -----------------------------------------------------------------------------------
# 6. COMANDOS DE USUÁRIO E PAINEL DE ADMIN
# -----------------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mensagem de boas-vindas para novos usuários no privado."""
    await update.message.reply_text(
        f"Olá! Seja bem-vindo ao nosso sistema de sinais 24 horas.\n\n"
        f"Para garantir que você tenha os mesmos resultados que postamos no canal, é **essencial** que você se cadastre na plataforma correta através do nosso link de parceiro.\n\n"
        f"👇 **CLIQUE ABAIXO PARA SE CADASTRAR E GANHAR BÔNUS** 👇\n"
        f"🔗 {URL_CADASTRO}\n\n"
        f"Após o cadastro, fique atento ao canal principal para os sinais. Boa sorte!"
    )

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o painel de controle para o administrador."""
    if update.effective_user.id != ADMIN_ID:
        return

    bd = context.bot_data
    manutencao_status = "ATIVOS ✅" if not bd.get('manutencao') else "PAUSADOS ⏸️"
    
    keyboard = [
        [InlineKeyboardButton("📊 Ver Placar", callback_data='admin_placar')],
        [InlineKeyboardButton("⚡ Forçar Sinal", callback_data='admin_forcar_sinal')],
        [InlineKeyboardButton("⚙️ Status do Bot", callback_data='admin_status')],
        [InlineKeyboardButton(f"Sinais Automáticos: {manutencao_status}", callback_data='admin_toggle_manutencao')],
    ]
    await update.message.reply_text("🔑 **Painel de Administrador** 🔑", reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processa os cliques nos botões do painel de admin."""
    query = update.callback_query
    await query.answer()
    bd = context.bot_data
    
    if query.data == 'admin_placar':
        placar_txt = (
            f"📊 **Placar Atual:** {bd.get('diario_win', 0)}W / {bd.get('diario_loss', 0)}L\n"
            f"🔥 **Sequência de Vitórias:** {bd.get('win_streak', 0)}\n"
            f"🎯 **Meta do Turno:** {bd.get('meta_wins_turno', 0)} WINS"
        )
        await query.edit_message_text(placar_txt, reply_markup=query.message.reply_markup)
    
    elif query.data == 'admin_forcar_sinal':
        await query.edit_message_text("✅ Comando recebido. Forçando o envio de um sinal agora...", reply_markup=query.message.reply_markup)
        await enviar_sinal(context, forcado_por_admin=True)

    elif query.data == 'admin_status':
        uptime = datetime.now() - bd.get("start_time", datetime.now())
        status_txt = (
            f"🤖 **Status do Bot** 🤖\n\n"
            f"✅ **Online e operando.**\n"
            f"⏱️ **Tempo no ar:** {str(uptime).split('.')[0]}\n"
            f"▶️ **Sinal em andamento?** {'Sim' if bd.get('sinal_em_andamento') else 'Não'}\n"
            f"⚙️ **Sinais Automáticos:** {'ATIVOS' if not bd.get('manutencao') else 'PAUSADOS'}"
        )
        await query.edit_message_text(status_txt, reply_markup=query.message.reply_markup)
    
    elif query.data == 'admin_toggle_manutencao':
        bd['manutencao'] = not bd.get('manutencao', False)
        status_text = 'PAUSADOS' if bd['manutencao'] else 'ATIVOS'
        await query.answer(f"Sinais automáticos agora estão {status_text}", show_alert=True)
        
        # Recria o painel para atualizar o texto do botão
        manutencao_status = "ATIVOS ✅" if not bd.get('manutencao') else "PAUSADOS ⏸️"
        keyboard = [
            [InlineKeyboardButton("📊 Ver Placar", callback_data='admin_placar')],
            [InlineKeyboardButton("⚡ Forçar Sinal", callback_data='admin_forcar_sinal')],
            [InlineKeyboardButton("⚙️ Status do Bot", callback_data='admin_status')],
            [InlineKeyboardButton(f"Sinais Automáticos: {manutencao_status}", callback_data='admin_toggle_manutencao')],
        ]
        await query.edit_message_text("🔑 **Painel de Administrador** 🔑", reply_markup=InlineKeyboardMarkup(keyboard))


# -----------------------------------------------------------------------------------
# 7. FUNÇÃO PRINCIPAL (MAIN) E INICIALIZAÇÃO DO BOT
# -----------------------------------------------------------------------------------

def main() -> None:
    """Função principal que constrói, configura e inicia o bot."""
    logger.info("Iniciando o bot - Versão 4.0 'Ultimate Edition'...")
    
    app = Application.builder().token(BOT_TOKEN).post_init(inicializar_estado).build()

    # --- Handlers de Comando e Callback ---
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("admin", admin_command, filters=filters.User(user_id=ADMIN_ID)))
    app.add_handler(CallbackQueryHandler(admin_callbacks, pattern='^admin_'))

    # --- Agendamento de Tarefas ---
    jq = app.job_queue
    # Agendador principal roda a cada minuto para decidir o que fazer
    jq.run_repeating(agendador_principal, interval=60, first=10)
    
    # Mensagens de abertura e fechamento dos turnos
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["abertura_madrugada"]), time=time(hour=2, minute=0))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["abertura_manha"]), time=time(hour=9, minute=0))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["abertura_tarde"]), time=time(hour=14, minute=0))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["abertura_noite"]), time=time(hour=20, minute=0))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["abertura_fds"]), time=time(hour=10, minute=0), days=(5, 6)) # Sábado e Domingo

    # Pausas e Resumo
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["pausa"]), time=time(hour=12, minute=5))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["pausa"]), time=time(hour=18, minute=5))
    jq.run_daily(resumo_diario, time=time(hour=23, minute=55))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["fechamento"]), time=time(hour=23, minute=59))

    logger.info("Bot iniciado com sucesso. Todas as tarefas agendadas. Operando 24/7.")
    app.run_polling()

if __name__ == "__main__":
    main()
