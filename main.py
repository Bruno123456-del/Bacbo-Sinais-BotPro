import os
import random
import logging
import json
import threading
import datetime
import asyncio
from flask import Flask
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    PicklePersistence,
)
from telegram.error import Forbidden

# ==============================
# CONFIGURAÇÕES DO BOT (env vars)
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID")) if os.getenv("CANAL_ID") else None
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID")) if os.getenv("VIP_CANAL_ID") else None
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None
PORT = int(os.getenv("PORT", 5000))

# ==============================
# LOG PROFISSIONAL EM JSON
# ==============================
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "msg": record.getMessage(),
            "name": record.name,
        }
        return json.dumps(log)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# ==============================
# BANCO DE DADOS SIMPLES (memória)
# ==============================
BANCO = {
    "ultimos_resultados": [],
    "usuarios": {},
    "stats": {"win": 0, "loss": 0, "gale": 0},
}

# ==============================
# ASSERTIVIDADE POR JOGO
# ==============================
ASSERTIVIDADE_JOGOS = {
    "futebol": [70, 20, 10],
    "basquete": [65, 25, 10],
    "mma": [60, 30, 10],
    "default": [65, 25, 10],
}

# ==============================
# FUNÇÃO DE ENVIO SEGURO (tratamento de exceções)
# ==============================
async def safe_send(bot, chat_id, **kwargs):
    if chat_id is None:
        logger.warning("chat_id é None, mensagem não enviada.")
        return None
    try:
        return await bot.send_message(chat_id=chat_id, **kwargs)
    except Forbidden:
        logger.info(f"Usuário/chat {chat_id} bloqueou o bot ou bot não tem acesso.")
    except Exception as e:
        logger.warning(f"Falha ao enviar mensagem para {chat_id}: {e}")

# ==============================
# RESULTADO REALISTA (MEMÓRIA CURTA)
# ==============================
def escolher_resultado(bd, jogo):
    ultimos = bd.get("ultimos_resultados", [])
    probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])

    # Evita 3 reds seguidos
    if ultimos[-3:] == ["loss", "loss", "loss"]:
        resultado = "win_primeira"
    else:
        resultado = random.choices(
            ["win_primeira", "win_gale", "loss"],
            weights=probabilidades,
            k=1
        )[0]

    ultimos.append(resultado)
    bd["ultimos_resultados"] = ultimos[-50:]  # mantém histórico curto (até 50)
    return resultado

# ==============================
# COMANDOS DO BOT
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        BANCO["usuarios"][user.id] = {
            "nome": user.first_name or user.username or "Usuário",
            "id": user.id,
            "joined": str(datetime.datetime.now()),
        }
    except Exception:
        logger.exception("Erro ao salvar usuário no BANCO.")
    keyboard = [
        [InlineKeyboardButton("🔥 Entrar no Canal VIP", url="https://t.me/seuCanalVIP")],
        [InlineKeyboardButton("📊 Ver Estatísticas", callback_data="painel_stats")]
    ]
    await safe_send(
        context.bot,
        chat_id=update.effective_chat.id,
        text=(
            "👋 Olá, bem-vindo(a)!\n\n"
            "Você está prestes a entrar no mundo dos sinais **milionários**. "
            "Aqui você terá acesso a estratégias usadas pelos **bilionários das apostas**.\n\n"
            "Escolha abaixo 👇"
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = BANCO["stats"]
    text = (
        f"📊 Estatísticas até agora:\n\n"
        f"✅ Wins: {s['win']}\n"
        f"⚠️ Wins no Gale: {s['gale']}\n"
        f"❌ Reds: {s['loss']}\n"
    )
    await safe_send(context.bot, update.effective_chat.id, text=text)

# ==============================
# PAINEL ADMINISTRATIVO
# ==============================
async def painel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID is None:
        await update.message.reply_text("ADMIN_ID não configurado.")
        return

    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Acesso negado!")
    
    keyboard = [
        [InlineKeyboardButton("📊 Estatísticas", callback_data="painel_stats")],
        [InlineKeyboardButton("🎲 Enviar sinal agora", callback_data="painel_sinal")],
        [InlineKeyboardButton("💎 Oferta Relâmpago", callback_data="painel_oferta")],
    ]
    await update.message.reply_text(
        "📌 *PAINEL DO ADMIN*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    if query.data == "painel_stats":
        # Reutiliza função stats: cria um falso objeto update com chat para enviar
        await stats(update, context)
    elif query.data == "painel_sinal":
        await safe_send(query.bot, query.message.chat.id, text="🎲 Sinal enviado manualmente!")
    elif query.data == "painel_oferta":
        await safe_send(query.bot, query.message.chat.id, text="💎 Oferta relâmpago ativada!")

# ==============================
# ENVIO DE SINAIS (single send)
# ==============================
async def enviar_sinal_especifico(bot, jogo="futebol"):
    resultado = escolher_resultado(BANCO, jogo)

    if resultado == "win_primeira":
        msg = f"⚽ {jogo.upper()} | ✅ WIN NA PRIMEIRA!"
        BANCO["stats"]["win"] += 1
    elif resultado == "win_gale":
        msg = f"🏀 {jogo.upper()} | ⚠️ WIN NO GALE!"
        BANCO["stats"]["gale"] += 1
    else:
        msg = f"🥊 {jogo.upper()} | ❌ RED!"
        BANCO["stats"]["loss"] += 1

    # Envia para canais configurados (ignora se None)
    await safe_send(bot, CANAL_ID, text=msg)
    await safe_send(bot, VIP_CANAL_ID, text=msg + "\n🔥 Exclusivo para VIPs!")

# ==============================
# ROTINAS AGENDADAS (cada uma executa UMA vez quando o Job chama)
# Usamos JobQueue para agendamento - NÃO colocamos while True aqui.
# ==============================
async def rotina_diaria(context: ContextTypes.DEFAULT_TYPE):
    """Envia um sinal aleatório — agendado a cada X minutos/hora via JobQueue."""
    jogos = ["futebol", "basquete", "mma"]
    jogo = random.choice(jogos)
    await enviar_sinal_especifico(context.bot, jogo=jogo)
    logger.info(f"rotina_diaria: sinal enviado ({jogo})")

async def reset_diario(context: ContextTypes.DEFAULT_TYPE):
    """Reseta estatísticas diárias — agendado com run_daily."""
    BANCO["stats"] = {"win": 0, "loss": 0, "gale": 0}
    logger.info("reset_diario: estatísticas resetadas para o novo dia.")

async def provas_sociais(context: ContextTypes.DEFAULT_TYPE):
    """Envia uma prova social curta — agendado a cada X horas."""
    mensagens = [
        "🔥 Aluno transformou R$200 em R$2.000 em 1 semana!",
        "🚀 Lucro de 300% só hoje com nossos sinais!",
        "💎 Grupo VIP explodindo de green!"
    ]
    msg = random.choice(mensagens)
    await safe_send(context.bot, CANAL_ID, text=msg)
    logger.info("provas_sociais: mensagem enviada.")

async def urgencia(context: ContextTypes.DEFAULT_TYPE):
    """Envia mensagens de urgência em horários estratégicos."""
    agora = datetime.datetime.now()
    # Se quiser horários diferentes, altere a lista abaixo
    if agora.hour in [10, 15, 20]:
        msg = (
            "⚡ Oferta Relâmpago! ⚡\n\n"
            "Somente HOJE o acesso ao **VIP** está com 50% OFF.\n"
            "⏳ Expira em 15 minutos!\n\n"
            "👉 Garanta já: https://t.me/seuCanalVIP"
        )
        await safe_send(context.bot, CANAL_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
        logger.info("urgencia: oferta relâmpago enviada.")
    else:
        logger.debug("urgencia: hora atual fora do range configurado.")

# ==============================
# FLASK (PING DO RENDER/HEROKU)
# ==============================
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot rodando com sucesso!"

# ==============================
# INICIALIZAÇÃO DO BOT (main)
# ==============================
async def main():
    # Persistência de dados (opcional)
    persistence = PicklePersistence(filepath="bot_data.pkl")

    # Cria a aplicação do telegram
    app = ApplicationBuilder()\
        .token(BOT_TOKEN)\
        .persistence(persistence)\
        .concurrent_updates(True)\
        .build()

    # Handlers de comando
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("painel", painel_command))

    # CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(callback_handler))

    # JobQueue para rotinas automáticas
    job_queue = app.job_queue

    # rotina_diaria: envia sinal a cada 1 hora (3600s) - primeiro em 5s
    job_queue.run_repeating(rotina_diaria, interval=3600, first=5)

    # reset_diario: agendado diariamente à meia-noite
    job_queue.run_daily(reset_diario, time=datetime.time(hour=0, minute=0))

    # provas_sociais: a cada 2 horas (7200s)
    job_queue.run_repeating(provas_sociais, interval=7200, first=15)

    # urgencia: verificação a cada 1 hora
    job_queue.run_repeating(urgencia, interval=3600, first=20)

    # Log e start do bot (modo async)
    logger.info("🤖 Iniciando bot...")
    # run_polling cuida de initialize/start/idle internamente
    await app.run_polling()

# ==============================
# EXECUÇÃO MULTITHREAD (FLASK + TELEGRAM)
# ==============================
def run_flask():
    # Flask roda em thread separada
    app_flask.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    # Inicia Flask em thread separada (não bloqueante)
    threading.Thread(target=run_flask, daemon=True).start()
    # Roda o bot (async)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot finalizado manualmente.")
    except Exception:
        logger.exception("Erro não tratado ao iniciar o bot.")
