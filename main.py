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
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, PicklePersistence, JobQueue
)
from telegram.error import Forbidden

# ==============================
# CONFIGURAÇÕES DO BOT
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

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
# BANCO DE DADOS SIMPLES
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
# FUNÇÃO DE ENVIO SEGURO
# ==============================
async def safe_send(bot, chat_id, **kwargs):
    try:
        return await bot.send_message(chat_id=chat_id, **kwargs)
    except Forbidden:
        logger.info(f"Usuário {chat_id} bloqueou o bot.")
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
    bd["ultimos_resultados"] = ultimos[-10:]  # mantém histórico curto
    return resultado

# ==============================
# COMANDOS DO BOT
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    BANCO["usuarios"][user.id] = {
        "nome": user.first_name,
        "id": user.id,
        "joined": str(datetime.datetime.now()),
    }
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
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Acesso negado!")
    
    keyboard = [
        [InlineKeyboardButton("📊 Estatísticas", callback_data="painel_stats")],
        [InlineKeyboardButton("🎲 Enviar sinal agora", callback_data="painel_sinal")],
        [InlineKeyboardButton("💎 Oferta Relâmpago", callback_data="painel_oferta")],
    ]
    await update.message.reply_text(
        "📌 **PAINEL DO ADMIN**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "painel_stats":
        await stats(update, context)
    elif query.data == "painel_sinal":
        await safe_send(query.bot, query.message.chat.id, text="🎲 Sinal enviado manualmente!")
    elif query.data == "painel_oferta":
        await safe_send(query.bot, query.message.chat.id, text="💎 Oferta relâmpago ativada!")

# ==============================
# ENVIO DE SINAIS
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

    await safe_send(bot, CANAL_ID, text=msg)
    await safe_send(bot, VIP_CANAL_ID, text=msg + "\n🔥 Exclusivo para VIPs!")

# ==============================
# ROTINA AUTOMÁTICA DE SINAIS
# ==============================
async def rotina_diaria(context: ContextTypes.DEFAULT_TYPE):
    jogos = ["futebol", "basquete", "mma"]
    while True:
        jogo = random.choice(jogos)
        await enviar_sinal_especifico(context.bot, jogo=jogo)
        await asyncio.sleep(3600)  # envia a cada 1 hora

# ==============================
# RESET DIÁRIO DE ESTATÍSTICAS
# ==============================
async def reset_diario(context: ContextTypes.DEFAULT_TYPE):
    while True:
        agora = datetime.datetime.now()
        proximo_reset = (agora + datetime.timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        segundos = (proximo_reset - agora).total_seconds()
        await asyncio.sleep(segundos)
        BANCO["stats"] = {"win": 0, "loss": 0, "gale": 0}
        logger.info("📊 Estatísticas resetadas para o novo dia.")

# ==============================
# PROVAS SOCIAIS AUTOMÁTICAS
# ==============================
async def provas_sociais(context: ContextTypes.DEFAULT_TYPE):
    mensagens = [
        "🔥 Aluno transformou R$200 em R$2.000 em 1 semana!",
        "🚀 Lucro de 300% só hoje com nossos sinais!",
        "💎 Grupo VIP explodindo de green!"
    ]
    while True:
        msg = random.choice(mensagens)
        await safe_send(context.bot, CANAL_ID, text=msg)
        await asyncio.sleep(7200)  # a cada 2 horas

# ==============================
# URGÊNCIA AUTOMÁTICA
# ==============================
async def urgencia(context: ContextTypes.DEFAULT_TYPE):
    while True:
        agora = datetime.datetime.now()
        if agora.hour in [10, 15, 20]:  # horários estratégicos
            msg = (
                "⚡ Oferta Relâmpago! ⚡\n\n"
                "Somente HOJE o acesso ao **VIP** está com 50% OFF.\n"
                "⏳ Expira em 15 minutos!\n\n"
                "👉 Garanta já: https://t.me/seuCanalVIP"
            )
            await safe_send(context.bot, CANAL_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(3600)

# ==============================
# FLASK (PING DO RENDER/HEROKU)
# ==============================
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot rod
# ==============================
# INICIALIZAÇÃO DO BOT
# ==============================
async def main():
    # Persistência de dados (opcional)
    persistence = PicklePersistence(filepath="bot_data.pkl")

    # Criação da aplicação
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
    job_queue.run_repeating(rotina_diaria, interval=3600, first=5)
    job_queue.run_repeating(reset_diario, interval=86400, first=10)
    job_queue.run_repeating(provas_sociais, interval=7200, first=15)
    job_queue.run_repeating(urgencia, interval=3600, first=20)

    # Start do bot
    logger.info("🤖 Bot iniciado com sucesso!")
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# ==============================
# EXECUÇÃO MULTITHREAD (FLASK + TELEGRAM)
# ==============================
def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    # Thread para o Flask
    threading.Thread(target=run_flask).start()
    # Thread principal para o Bot
    asyncio.run(main())
