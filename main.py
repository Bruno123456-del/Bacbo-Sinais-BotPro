# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 3.0 "ULTIMATE EDITION"
# CRIADO POR MANUS - FOCO EM EXPERIÊNCIA, ENGAJAMENTO E CONVERSÃO
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
GIF_LOSS = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.giphy.gif"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_COMEMORACAO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"
GIF_META_BATIDA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3JvZ3g1cWJqY2w4eXJqZzZzZzZzZzZzZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"

# --- Mensagens de Marketing (para maximizar conversão ) ---
MARKETING_MESSAGES = [
    f"🤔 **Ainda não se cadastrou?** Para ter EXATAMENTE os mesmos resultados que nós, é essencial usar a plataforma para a qual nossa IA é calibrada. \n\n👉 [**CADASTRE-SE AQUI E GANHE BÔNUS**]({URL_CADASTRO})\n\nNão arrisque seu dinheiro em outra!",
    f"💰 **QUER LUCRAR DE VERDADE?** Nossos sinais são otimizados para uma plataforma específica. Cadastre-se pelo nosso link e ganhe benefícios exclusivos! \n\n👉 [**CLIQUE AQUI PARA SE CADASTRAR**]({URL_CADASTRO})",
    f"⚠️ **AVISO IMPORTANTE:** Jogar em outra plataforma pode invalidar nossos sinais. Garanta sua segurança e seus lucros, jogue na plataforma certa! \n\n👉 [**CADASTRE-SE COM SEGURANÇA AQUI**]({URL_CADASTRO})",
]

# --- Mensagens de Status "Humanizadas" ---
STATUS_MESSAGES = {
    "abertura": "☀️ **Bom dia, comunidade!** Iniciando as análises do dia. A meta de hoje é **{meta_wins} WINS**. Vamos com tudo! Fiquem atentos. 👀",
    "fechamento": "🌙 **Operações encerradas por hoje!** Obrigado a todos que confiaram em nossas análises. O resumo final já foi enviado. Descansem, pois amanhã tem mais!",
    "pausa": "⏸️ **Pausa estratégica.** Momento de recalibrar a análise de mercado. Voltamos em breve com o próximo turno de sinais. Fiquem no aguardo!",
    "pausa_seguranca": "⚠️ **PAUSA DE SEGURANÇA** ⚠️ O mercado apresentou alta volatilidade. Pausando as operações por 20 minutos para proteger nosso capital. Disciplina é tudo!",
    "meta_batida": "🏆 **META DIÁRIA ATINGIDA!** 🏆\n\nParabéns, comunidade! Batemos a meta de **{meta_wins} WINS** de hoje. Isso é resultado de análise, paciência e da força do nosso grupo. Vamos continuar lucrando com responsabilidade!",
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
    bd["meta_wins_diaria"] = random.randint(10, 15)
    bd["meta_batida"] = False
    bd["start_time"] = datetime.now()
    logger.info(f"Estado do bot inicializado. Meta de hoje: {bd['meta_wins_diaria']} WINS.")

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

        # Etapa 2: Envio do Sinal
        jogos = {
            "Roleta": {"entradas": ["Preto ⚫", "Vermelho 🔴", "Ímpar", "Par"]},
            "Bac Bo": {"entradas": ["Banker 🔴", "Player 🔵"]},
            "Mines 💣": {"entradas": ["3 Minas - Abrir 5 campos", "3 Minas - Abrir 7 campos"]}
        }
        jogo_escolhido = random.choice(list(jogos.keys()))
        aposta = random.choice(jogos[jogo_escolhido]["entradas"])

        mensagem_sinal = (
            f"🔥 **ALERTA DE ENTRADA - {jogo_escolhido.upper()}** 🔥\n\n"
            f"🎯 **Entrada Sugerida:** {aposta}\n\n"
            f"**Plano de Ação:**\n"
            f"1️⃣ Fazer a entrada com gestão de banca.\n"
            f"2️⃣ Se aplicável, usar até 2 gales.\n\n"
            f"🔗 **[JOGUE NA PLATAFORMA CORRETA]({URL_CADASTRO})**"
        )
        await msg_analise.delete()
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal enviado para {jogo_escolhido}: {aposta}.")

        # Etapa 3: Resultado (Simulação)
        await asyncio.sleep(random.randint(45, 75))
        resultado = random.choices(["win", "gale1", "gale2", "loss"], weights=[60, 20, 10, 10], k=1)[0]
        
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

        placar = f"📊 Placar: {bd['diario_win']}W / {bd['diario_loss']}L"
        
        # Adiciona a sequência de vitórias (streak) à mensagem se for >= 3
        if bd["win_streak"] >= 3:
            caption += f"\n\n🔥🔥 **ESTAMOS NUMA SEQUÊNCIA DE {bd['win_streak']} WINS!** 🔥🔥"

        if isinstance(imagem, str) and "giphy.com" in imagem:
             await context.bot.send_animation(chat_id=CANAL_ID, animation=imagem, caption=f"{caption}\n\n{placar}")
        else:
             await context.bot.send_photo(chat_id=CANAL_ID, photo=imagem, caption=f"{caption}\n\n{placar}")

        if foi_green:
             await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_COMEMORACAO)
             await context.bot.send_message(chat_id=CANAL_ID, text=random.choice(MARKETING_MESSAGES), parse_mode='Markdown', disable_web_page_preview=False)
             # Verifica se a meta foi batida
             if not bd.get("meta_batida") and bd["diario_win"] >= bd["meta_wins_diaria"]:
                 bd["meta_batida"] = True
                 await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_META_BATIDA)
                 await context.bot.send_message(chat_id=CANAL_ID, text=STATUS_MESSAGES["meta_batida"].format(meta_wins=bd['meta_wins_diaria']))
        
        # Verifica se houve 2 REDs seguidos para a pausa de segurança
        if bd["loss_streak"] >= 2:
            bd["loss_streak"] = 0 # Zera para não entrar em loop
            await enviar_mensagem_status(context, STATUS_MESSAGES["pausa_seguranca"])
            await asyncio.sleep(1200) # Pausa por 20 minutos

    except Exception as e:
        logger.error(f"Erro no ciclo de sinal: {e}")
    finally:
        bd["sinal_em_andamento"] = False

# -----------------------------------------------------------------------------------
# 5. AGENDAMENTO E TAREFAS RECORRENTES
# -----------------------------------------------------------------------------------

async def agendador_principal(context: ContextTypes.DEFAULT_TYPE):
    """Verifica o horário e a probabilidade para enviar um sinal ou mensagem de marketing."""
    agora = datetime.now()
    bd = context.bot_data
    
    if bd.get("manutencao", False):
        return # Se estiver em manutenção, não faz nada

    horarios_ativos = [(time(9, 0), time(12, 0)), (time(14, 0), time(18, 0)), (time(20, 0), time(23, 0))]
    is_active_time = any(inicio <= agora.time() <= fim for inicio, fim in horarios_ativos)

    if is_active_time and not bd.get("sinal_em_andamento", False):
        # Chance de enviar um sinal (aprox. 1 a cada 15 min)
        if random.random() < 1/15:
            logger.info(f"Sorteado para enviar SINAL no horário {agora.time()}.")
            await enviar_sinal(context)
        # Chance de enviar uma mensagem de marketing (aprox. 1 a cada 60 min)
        elif random.random() < 1/60:
            logger.info(f"Sorteado para enviar MENSAGEM DE MARKETING no horário {agora.time()}.")
            await context.bot.send_message(chat_id=CANAL_ID, text=random.choice(MARKETING_MESSAGES), parse_mode='Markdown', disable_web_page_preview=False)

async def enviar_mensagem_status(context: ContextTypes.DEFAULT_TYPE, mensagem: str):
    try:
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem)
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
    
    # Zera os contadores para o próximo dia
    bd["diario_win"], bd["diario_loss"], bd["win_streak"], bd["loss_streak"] = 0, 0, 0, 0
    bd["meta_wins_diaria"] = random.randint(10, 15)
    bd["meta_batida"] = False
    logger.info("Resumo diário enviado e contadores zerados.")

# -----------------------------------------------------------------------------------
# 6. COMANDOS DE USUÁRIO E PAINEL DE ADMIN
# -----------------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mensagem de boas-vindas para novos usuários no privado."""
    await update.message.reply_text(
        f"Olá! Seja bem-vindo ao nosso sistema de sinais.\n\n"
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
    manutencao_status = "LIGADO 🟢" if not bd.get('manutencao') else "DESLIGADO 🔴"
    
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
            f"🔥 **Sequência de Vitórias:** {bd.get('win_streak', 0)}"
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
            f"⚙️ **Sinais Automáticos:** {'LIGADO' if not bd.get('manutencao') else 'DESLIGADO'}"
        )
        await query.edit_message_text(status_txt, reply_markup=query.message.reply_markup)
    
    elif query.data == 'admin_toggle_manutencao':
        bd['manutencao'] = not bd.get('manutencao', False)
        await query.answer(f"Sinais automáticos {'ATIVADOS' if not bd['manutencao'] else 'DESATIVADOS'}", show_alert=True)
        # Atualiza o painel para refletir a mudança
        await admin_command(query, context)

# -----------------------------------------------------------------------------------
# 7. FUNÇÃO PRINCIPAL (MAIN) E INICIALIZAÇÃO DO BOT
# -----------------------------------------------------------------------------------

def main() -> None:
    """Função principal que constrói, configura e inicia o bot."""
    logger.info("Iniciando o bot - Versão 3.0 'Ultimate Edition'...")
    
    app = Application.builder().token(BOT_TOKEN).post_init(inicializar_estado).build()

    # --- Handlers de Comando e Callback ---
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("admin", admin_command, filters=filters.User(user_id=ADMIN_ID)))
    app.add_handler(CallbackQueryHandler(admin_callbacks, pattern='^admin_'))

    # --- Agendamento de Tarefas ---
    jq = app.job_queue
    jq.run_repeating(agendador_principal, interval=60, first=10)
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["abertura"].format(meta_wins=ctx.bot_data['meta_wins_diaria'])), time=time(hour=9, minute=0))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["pausa"]), time=time(hour=12, minute=5))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["pausa"]), time=time(hour=18, minute=5))
    jq.run_daily(resumo_diario, time=time(hour=23, minute=1))
    jq.run_daily(lambda ctx: enviar_mensagem_status(ctx, STATUS_MESSAGES["fechamento"]), time=time(hour=23, minute=5))

    logger.info("Bot iniciado com sucesso. Todas as tarefas agendadas. Aguardando comandos e horários de operação.")
    app.run_polling()

if __name__ == "__main__":
    main()
