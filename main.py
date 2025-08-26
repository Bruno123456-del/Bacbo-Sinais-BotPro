# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO FINAL "EXPERIÊNCIA VIP R$600"
# CRIADO E OTIMIZADO POR MANUS
# Foco em: Prova Social, Oferta Irresistível e Conversão VIP.
# ===================================================================================

# -----------------------------------------------------------------------------------
# 1. IMPORTAÇÕES E CONFIGURAÇÃO GERAL
# -----------------------------------------------------------------------------------
import logging
import os
import random
import asyncio
from datetime import time, datetime
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
ADMIN_ID = 5011424031  # SEU ID DE ADMINISTRADOR

# --- Links Estratégicos ---
URL_CADASTRO = "https://lkwn.cc/f1c1c45a" # SEU LINK DE AFILIADO
URL_VIDEO_DEPOSITO = "https://t.me/ApostasMilionariaVIP/338"
URL_SUPORTE_VIP = "https://t.me/seu_usuario_suporte" # TROQUE PELO SEU CONTATO DE SUPORTE

# --- Validação Crítica ---
if not BOT_TOKEN or CANAL_ID == "0":
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN ou CANAL_ID não foram configurados corretamente no arquivo .env!" )
CANAL_ID = int(CANAL_ID)

# --- Configuração do Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Configurações de Operação ---
HORARIOS_ATIVOS = [(13, 0, 17, 0), (19, 0, 22, 0)]
META_WINS_DIARIA_MIN = 10
META_WINS_DIARIA_MAX = 15
PROBABILIDADE_SINAL_POR_MINUTO = 1 / 18
PROBABILIDADE_MARKETING_POR_MINUTO = 1 / 70
PROBABILIDADE_CONTEUDO_VALOR_POR_MINUTO = 1 / 90

# -----------------------------------------------------------------------------------
# 3. BANCO DE MÍDIAS, JOGOS E CONTEÚDO DE VALOR
# -----------------------------------------------------------------------------------

# --- Mídias Visuais ---
IMG_HEADER_SINAL = "https://i.ibb.co/9g6v3c6/sinal-header.png"
IMG_GREEN = "https://i.ibb.co/M6r5b5x/green.png"
IMG_RED = "https://i.ibb.co/Y0g9g5d/red.png"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_META_BATIDA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3JvZ3g1cWJqY2w4eXJqZzZzZzZzZzZzZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"

# --- Hierarquia de Jogos e Estratégias ---
JOGOS = {
    "Bac Bo 🎲": {"entradas": ["Banker 🔴", "Player 🔵"], "estrategia": "Análise de tendências e quebra de padrão.", "pesos_resultado": [65, 20, 5, 10]},
    "Roleta 🎰": {"entradas": ["1ª Dúzia", "2ª Dúzia", "Vermelho ⚫", "Preto 🔴"], "estrategia": "Monitoramento de colunas e dúzias 'quentes' e 'frias'.", "pesos_resultado": [65, 20, 5, 10]},
    "Fortune Tiger 🐯": {"entradas": ["Buscar 10 rodadas", "Ativar o turbo por 7 rodadas"], "estrategia": "Identificação dos 'minutos pagantes' com RTP elevado.", "pesos_resultado": [60, 15, 10, 15]}
}

# --- Banco de Conteúdo de Valor (Prova Social, Dicas, Motivação ) ---
CONTEUDO_DE_VALOR = {
    "provas_sociais": ["https://i.ibb.co/dG0B2zW/prova1.png", "https://i.ibb.co/jWnB1bQ/prova2.png", "https://i.ibb.co/k1C7z5T/prova3.png"],
    "dicas_gestao": ["🧠 **DICA DE GESTÃO:** Nunca aposte mais de 5% da sua banca em uma única entrada. A consistência vence a ganância.", "🧠 **DICA DE GESTÃO:** Defina metas de ganho e perda DIÁRIAS. Se atingir, pare! O mercado estará aí amanhã.", "🧠 **DICA DE GESTÃO:** Não tente 'recuperar' um red de uma vez. Volte para sua aposta padrão e siga o plano."],
    "frases_motivacionais": ["💸 O sucesso é uma combinação de **paciência, disciplina e informação privilegiada**. Você já tem o terceiro. Os dois primeiros dependem de você.", "🚀 Lembre-se do seu objetivo. Visualize onde você quer chegar. Cada green é um passo nessa direção.", "🔥 A diferença entre quem você é e quem você quer ser é **o que você faz**. Continue seguindo o plano."]
}

# -----------------------------------------------------------------------------------
# 4. BANCO DE MENSAGENS PERSUASIVAS (COPYWRITING VIP )
# -----------------------------------------------------------------------------------

def get_welcome_message():
    texto = (
        f"💎 *BEM-VINDO À SALA VIP - BAC BO DE ELITE* 💎\n\n"
        f"Prezado(a) investidor(a), você acaba de entrar no canal de sinais mais completo do mercado.\n\n"
        f"Aqui está tudo o que você precisa para começar a lucrar em menos de 5 minutos:\n\n"
        f"1️⃣ *ATIVE SEU BÔNUS DE R$600*\n"
        f"Para ter os mesmos resultados que nós, use nosso link exclusivo. A plataforma vai te dar um bônus especial no seu primeiro depósito.\n\n"
        f"2️⃣ *APRENDA A DEPOSITAR (VÍDEO)*\n"
        f"Assista ao nosso tutorial rápido e veja como é fácil colocar saldo para operar.\n"
        f"👉 {URL_VIDEO_DEPOSITO}\n\n"
        f"3️⃣ *ENTENDA NOSSA ESTRATÉGIA*\n"
        f"Nós usamos um método de gestão profissional com até 2 gales (proteções). Respeite a gestão para garantir seu lucro a longo prazo.\n\n"
        f"🚀 *Tudo pronto?* Acompanhe os sinais abaixo e comece a operar!"
    )
    botoes = [[InlineKeyboardButton("👉 JOGAR AGORA COM BÔNUS DE R$600 👈", url=URL_CADASTRO)]]
    return texto, botoes

def get_private_start_message():
    texto = (
        f"💎 *BEM-VINDO(A) À NOSSA CENTRAL VIP* 💎\n\n"
        f"Olá! Sou seu assistente de lucros. Para começar a operar e ativar seu **bônus de R$600**, siga os passos abaixo:"
    )
    botoes = [
        [InlineKeyboardButton("1️⃣ ATIVAR BÔNUS DE R$600 AGORA", url=URL_CADASTRO)],
        [InlineKeyboardButton("2️⃣ VÍDEO: COMO DEPOSITAR", url=URL_VIDEO_DEPOSITO)],
        [InlineKeyboardButton("3️⃣ LER SOBRE A ESTRATÉGIA", callback_data="explain_strategy")]
    ]
    return texto, botoes

def get_strategy_explanation():
    return (
        "🧠 *NOSSA ESTRATÉGIA DE GESTÃO PROFISSIONAL*\n\n"
        "Nosso método é simples e eficaz, focado em proteger seu capital e maximizar os lucros a longo prazo.\n\n"
        "1. **ENTRADA INICIAL:** Fazemos a entrada no sinal recomendado com um valor base (sugerimos 1% a 2% da sua banca).\n\n"
        "2. **GALE 1 (Proteção 1):** Se o resultado da primeira entrada for 'RED' (perda), nós dobramos o valor da aposta inicial e entramos novamente para recuperar a perda e ainda sair com lucro.\n\n"
        "3. **GALE 2 (Proteção 2):** Se o GALE 1 também for 'RED', dobramos o valor do GALE 1 para uma última tentativa.\n\n"
        "**REGRA DE OURO:** Se o GALE 2 resultar em 'RED', nós aceitamos a perda (stop loss) e esperamos o próximo sinal. **NUNCA** tente um GALE 3. A disciplina de parar é o que garante o lucro no final do mês."
    )

def get_marketing_message():
    return (
        f"💰 **OFERTA EXCLUSIVA AINDA ATIVA!** 💰\n\n"
        f"Lembre-se: nosso link de parceiro te garante um **bônus de R$600** no seu primeiro depósito.\n\n"
        f"Não deixe esse dinheiro na mesa. Ative sua oferta e aumente sua banca para lucrar ainda mais com nossos sinais.\n\n"
        f"👉 [**ATIVAR MEU BÔNUS DE R$600 AGORA**]({URL_CADASTRO})"
    )

def get_placar_message(bd):
    wins, losses = bd.get('diario_win', 0), bd.get('diario_loss', 0)
    total = wins + losses
    assertividade = (wins / total * 100) if total > 0 else 0
    return (
        f"📊 **PAINEL DE ESTATÍSTICAS DO DIA** 📊\n\n"
        f"✅ Greens: {wins} | ❌ Reds: {losses}\n"
        f"📈 Assertividade: {assertividade:.2f}%\n"
        f"🔥 Sequência de Vitórias: {bd.get('win_streak', 0)}\n"
        f"🎯 Meta Diária: {bd.get('meta_wins_diaria', 0)} Wins"
    )

# -----------------------------------------------------------------------------------
# 5. LÓGICA PRINCIPAL E TAREFAS AGENDADAS
# -----------------------------------------------------------------------------------

async def post_init(app: Application):
    bd = app.bot_data
    bd.update({"diario_win": 0, "diario_loss": 0, "win_streak": 0, "loss_streak": 0, "sinal_em_andamento": False, "manutencao": False, "meta_batida": False, "meta_wins_diaria": random.randint(META_WINS_DIARIA_MIN, META_WINS_DIARIA_MAX)})
    logger.info(f"Estado do bot inicializado. Meta de hoje: {bd['meta_wins_diaria']} WINS.")

async def enviar_sinal(context: ContextTypes.DEFAULT_TYPE):
    bd = context.bot_data
    if bd.get("sinal_em_andamento") or bd.get("meta_batida"): return
    bd["sinal_em_andamento"] = True
    try:
        await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_ANALISANDO, caption="```ansi\n[2;34m// IA EM ANÁLISE... BUSCANDO PADRÃO LUCRATIVO //[0m\n```")
        await asyncio.sleep(random.randint(10, 20))
        
        jogo_escolhido = random.choice(list(JOGOS.keys()))
        jogo_info = JOGOS[jogo_escolhido]
        aposta = random.choice(jogo_info["entradas"])
        
        keyboard = [[InlineKeyboardButton("🎮 JOGAR COM BÔNUS VIP 🎮", url=URL_CADASTRO)], [InlineKeyboardButton("📊 Estratégia", callback_data=f'strat_{jogo_escolhido}'), InlineKeyboardButton("💎 Suporte VIP", url=URL_SUPORTE_VIP)]]
        
        await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_HEADER_SINAL, caption=f"🔥 **SINAL CONFIRMADO | {jogo_escolhido.upper()}** 🔥\n\n**ENTRADA:**\n```{aposta}```\n**ESTRATÉGIA:**\nProteger com até 2 gales. Seguir a gestão.", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        logger.info(f"Sinal enviado para {jogo_escolhido}: {aposta}.")

        await asyncio.sleep(random.randint(60, 90))
        resultado = random.choices(["win", "gale1", "gale2", "loss"], weights=jogo_info["pesos_resultado"], k=1)[0]
        
        imagem_resultado, caption_resultado = IMG_RED, ""
        if resultado != "loss":
            bd["diario_win"] += 1; bd["win_streak"] += 1; bd["loss_streak"] = 0; imagem_resultado = IMG_GREEN
            if resultado == "win": caption_resultado = "✅ **GREEN!** ✅\n\nSimples assim."
            elif resultado == "gale1": caption_resultado = "✅ **GREEN NO GALE 1!** ✅\n\nA análise foi mais forte."
            else: caption_resultado = "✅ **GREEN NO GALE 2!** ✅\n\nNo limite, mas dentro do plano!"
        else:
            bd["diario_loss"] += 1; bd["loss_streak"] += 1; bd["win_streak"] = 0
            caption_resultado = "❌ **RED.** ❌\n\nStop loss. A gestão nos protege."

        if bd["win_streak"] >= 3: caption_resultado += f"\n\n🔥🔥 **SEQUÊNCIA DE {bd['win_streak']} GREENS!** 🔥🔥"
        
        await context.bot.send_photo(chat_id=CANAL_ID, photo=imagem_resultado, caption=f"{caption_resultado}\n\n📊 Placar: {bd['diario_win']}W / {bd['diario_loss']}L", parse_mode='Markdown')

        if not bd.get("meta_batida") and bd["diario_win"] >= bd["meta_wins_diaria"]:
            bd["meta_batida"] = True
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_META_BATIDA)
            await context.bot.send_message(chat_id=CANAL_ID, text=f"🏆 **META BATIDA!** 🏆\n\nBatemos a meta de **{bd['meta_wins_diaria']} WINS**! Isso não é sorte, é método.\n\n👇 **Ainda não ativou seu bônus de R$600? A hora é AGORA:**\n[**QUERO MEU BÔNUS E LUCRAR JUNTO!**]({URL_CADASTRO})", parse_mode='Markdown')
        
        if bd["loss_streak"] >= 2:
            bd["loss_streak"] = 0
            await context.bot.send_message(chat_id=CANAL_ID, text="```ansi\n[2;33m// ALERTA: PROTOCOLO DE CONTENÇÃO ATIVADO //[0m\n```\n⚠️ **PAUSA DE SEGURANÇA.** Mercado instável. Pausando por 20 minutos.", parse_mode='Markdown')
            await asyncio.sleep(1200)
    except Exception as e:
        logger.error(f"Erro no ciclo de sinal: {e}")
    finally:
        bd["sinal_em_andamento"] = False

async def enviar_conteudo_de_valor(context: ContextTypes.DEFAULT_TYPE):
    tipo_conteudo = random.choice(list(CONTEUDO_DE_VALOR.keys()))
    if tipo_conteudo == "provas_sociais":
        imagem = random.choice(CONTEUDO_DE_VALOR[tipo_conteudo])
        await context.bot.send_photo(chat_id=CANAL_ID, photo=imagem, caption="🔥 **Acontece todos os dias na nossa comunidade VIP.** 🔥\n\nIsso é resultado de seguir o método. E você, vai ficar de fora?")
    else:
        mensagem = random.choice(CONTEUDO_DE_VALOR[tipo_conteudo])
        await context.bot.send_message(chat_id=CANAL_ID, text=mensagem, parse_mode='Markdown')
    logger.info(f"Enviado conteúdo de valor do tipo: {tipo_conteudo}")

async def agendador_principal(context: ContextTypes.DEFAULT_TYPE):
    agora = datetime.now().time()
    bd = context.bot_data
    if bd.get("manutencao", False): return
    is_active_time = any(time(h_i, m_i) <= agora <= time(h_f, m_f) for h_i, m_i, h_f, m_f in HORARIOS_ATIVOS)
    if is_active_time and not bd.get("sinal_em_andamento", False):
        rand_num = random.random()
        if rand_num < PROBABILIDADE_SINAL_POR_MINUTO: await enviar_sinal(context)
        elif rand_num < PROBABILIDADE_SINAL_POR_MINUTO + PROBABILIDADE_MARKETING_POR_MINUTO: await context.bot.send_message(chat_id=CANAL_ID, text=get_marketing_message(), parse_mode='Markdown', disable_web_page_preview=True)
        elif rand_num < PROBABILIDADE_SINAL_POR_MINUTO + PROBABILIDADE_MARKETING_POR_MINUTO + PROBABILIDADE_CONTEUDO_VALOR_POR_MINUTO: await enviar_conteudo_de_valor(context)

# -----------------------------------------------------------------------------------
# 6. COMANDOS DE USUÁRIO E PAINEL DE ADMIN
# -----------------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto, botoes = get_private_start_message()
    await update.message.reply_text(texto, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(botoes))

async def comecar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    texto, botoes = get_welcome_message()
    mensagem_enviada = await context.bot.send_message(chat_id=update.effective_chat.id, text=texto, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(botoes), disable_web_page_preview=True)
    try:
        await context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=mensagem_enviada.message_id, disable_notification=True)
        await update.message.delete()
    except Exception as e:
        logger.error(f"Erro ao fixar mensagem: {e}. O bot tem permissão de admin?")

async def placar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_placar_message(context.bot_data), parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    status_auto = "ATIVADOS ✅" if not context.bot_data.get('manutencao') else "DESATIVADOS ❌"
    keyboard = [[InlineKeyboardButton("📊 Ver Placar", callback_data='admin_placar')], [InlineKeyboardButton("⚡ Forçar Sinal", callback_data='admin_forcar_sinal')], [InlineKeyboardButton(f"Sinais Automáticos: {status_auto}", callback_data='admin_toggle_auto')]]
    await update.message.reply_text("🔑 **PAINEL DE CONTROLE VIP** 🔑", reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'admin_placar': await query.edit_message_text(get_placar_message(context.bot_data), parse_mode='Markdown', reply_markup=query.message.reply_markup)
    elif query.data == 'admin_forcar_sinal':
        await query.edit_message_text("✅ Comando recebido. Forçando o envio de um sinal...", reply_markup=query.message.reply_markup)
        await enviar_sinal(context)
    elif query.data == 'admin_toggle_auto':
        bd = context.bot_data
        bd['manutencao'] = not bd.get('manutencao', False)
        await query.answer(f"Sinais automáticos {'ATIVADOS' if not bd['manutencao'] else 'DESATIVADOS'}", show_alert=True)
        await admin_command(query, context)

async def strategy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(text=get_strategy_explanation(), parse_mode='Markdown')

async def game_strategy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    jogo_key = query.data.split('_')[1]
    if jogo_key in JOGOS: await query.answer(text=f"Estratégia para {jogo_key}:\n\n{JOGOS[jogo_key]['estrategia']}", show_alert=True)

# -----------------------------------------------------------------------------------
# 7. FUNÇÃO PRINCIPAL (MAIN)
# -----------------------------------------------------------------------------------

def main() -> None:
    logger.info("Iniciando o bot - Edição Experiência VIP R$600...")
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("placar", placar_command))
    app.add_handler(CommandHandler("comecar", comecar_command, filters=filters.User(user_id=ADMIN_ID)))
    app.add_handler(CommandHandler("admin", admin_command, filters=filters.User(user_id=ADMIN_ID)))
    
    app.add_handler(CallbackQueryHandler(admin_callbacks, pattern='^admin_'))
    app.add_handler(CallbackQueryHandler(strategy_callback, pattern='^explain_strategy$'))
    app.add_handler(CallbackQueryHandler(game_strategy_callback, pattern='^strat_'))

    jq = app.job_queue
    jq.run_repeating(agendador_principal, interval=60, first=10)
    jq.run_daily(lambda ctx: ctx.bot.send_message(chat_id=CANAL_ID, text=f"```ansi\n[2;32m// STATUS: ONLINE //[0m\n```\nBom dia, time VIP. A meta de hoje é **{ctx.bot_data['meta_wins_diaria']} WINS**.", parse_mode='Markdown'), time=time(hour=12, minute=55))
    jq.run_daily(lambda ctx: ctx.bot.send_message(chat_id=CANAL_ID, text="```ansi\n[2;31m// STATUS: OFFLINE //[0m\n```\nOperações finalizadas. Descansem, amanhã tem mais.", parse_mode='Markdown'), time=time(hour=22, minute=5))
    jq.run_daily(lambda ctx: post_init(ctx.application), time=time(hour=0, minute=1))

    logger.info("Bot iniciado com sucesso. Estratégia VIP R$600 ativa.")
    app.run_polling()

if __name__ == "__main__":
    main()
