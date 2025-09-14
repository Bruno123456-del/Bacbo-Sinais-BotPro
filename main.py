import os
import random
import logging
import json
import datetime
import asyncio
from flask import Flask, request as flask_request # Renomeado para evitar conflito
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    PicklePersistence,
)
from telegram.error import Forbidden

# ==============================
# CONFIGURAÇÕES DO BOT (lidas do ambiente)
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID")) if os.getenv("CANAL_ID") else None
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID")) if os.getenv("VIP_CANAL_ID") else None
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None
# URL para o webhook (ex: https://seu-bot.onrender.com )
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
# Porta que o Render fornece
PORT = int(os.getenv("PORT", 8000))

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
        if record.exc_info:
            log['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# ==============================
# BANCO DE DADOS SIMPLES (usando persistência do bot)
# ==============================
# O PicklePersistence já cuida de salvar os dados do context.bot_data

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
async def safe_send(bot: Bot, chat_id: int, **kwargs):
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
# RESULTADO REALISTA
# ==============================
def escolher_resultado(bot_data: dict, jogo: str) -> str:
    if "ultimos_resultados" not in bot_data:
        bot_data["ultimos_resultados"] = []
    
    ultimos = bot_data["ultimos_resultados"]
    probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])

    if len(ultimos) >= 3 and all(r == "loss" for r in ultimos[-3:]):
        resultado = "win_primeira"
    else:
        resultado = random.choices(
            ["win_primeira", "win_gale", "loss"],
            weights=probabilidades,
            k=1
        )[0]

    ultimos.append(resultado)
    bot_data["ultimos_resultados"] = ultimos[-50:]
    return resultado

# ==============================
# COMANDOS DO BOT
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if "usuarios" not in context.bot_data:
        context.bot_data["usuarios"] = {}
    
    context.bot_data["usuarios"][user.id] = {
        "nome": user.first_name or user.username or "Usuário",
        "id": user.id,
        "joined": str(datetime.datetime.now()),
    }
    
    keyboard = [
        [InlineKeyboardButton("🔥 Entrar no Canal VIP", url="https://t.me/seuCanalVIP" )],
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
    s = context.bot_data.get("stats", {"win": 0, "loss": 0, "gale": 0})
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
        await stats(update, context)
    elif query.data == "painel_sinal":
        await enviar_sinal_especifico(context, jogo="futebol")
        await safe_send(query.bot, query.message.chat.id, text="🎲 Sinal enviado manualmente!")
    elif query.data == "painel_oferta":
        await urgencia(context)
        await safe_send(query.bot, query.message.chat.id, text="💎 Oferta relâmpago ativada!")

# ==============================
# ENVIO DE SINAIS
# ==============================
async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo="futebol"):
    bot_data = context.bot_data
    if "stats" not in bot_data:
        bot_data["stats"] = {"win": 0, "loss": 0, "gale": 0}

    resultado = escolher_resultado(bot_data, jogo)

    if resultado == "win_primeira":
        msg = f"⚽ {jogo.upper()} | ✅ WIN NA PRIMEIRA!"
        bot_data["stats"]["win"] += 1
    elif resultado == "win_gale":
        msg = f"🏀 {jogo.upper()} | ⚠️ WIN NO GALE!"
        bot_data["stats"]["gale"] += 1
    else:
        msg = f"🥊 {jogo.upper()} | ❌ RED!"
        bot_data["stats"]["loss"] += 1

    await safe_send(context.bot, CANAL_ID, text=msg)
    await safe_send(context.bot, VIP_CANAL_ID, text=msg + "\n🔥 Exclusivo para VIPs!")
    logger.info(f"Sinal enviado: {msg}")

# ==============================
# ROTINAS AGENDADAS
# ==============================
async def rotina_diaria(context: ContextTypes.DEFAULT_TYPE):
    jogos = ["futebol", "basquete", "mma"]
    jogo = random.choice(jogos)
    await enviar_sinal_especifico(context, jogo=jogo)
    logger.info(f"rotina_diaria: sinal enviado ({jogo})")

async def reset_diario(context: ContextTypes.DEFAULT_TYPE):
    context.bot_data["stats"] = {"win": 0, "loss": 0, "gale": 0}
    await safe_send(context.bot, CANAL_ID, text="📊 As estatísticas foram resetadas para um novo dia de lucros!")
    logger.info("reset_diario: estatísticas resetadas.")

async def provas_sociais(context: ContextTypes.DEFAULT_TYPE):
    mensagens = [
        "🔥 Aluno transformou R$200 em R$2.000 em 1 semana!",
        "🚀 Lucro de 300% só hoje com nossos sinais!",
        "💎 Grupo VIP explodindo de green!"
    ]
    msg = random.choice(mensagens)
    await safe_send(context.bot, CANAL_ID, text=msg)
    logger.info("provas_sociais: mensagem enviada.")

async def urgencia(context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⚡ Oferta Relâmpago! ⚡\n\n"
        "Somente HOJE o acesso ao **VIP** está com 50% OFF.\n"
        "⏳ Vagas limitadas!\n\n"
        "👉 Garanta já: https://t.me/seuCanalVIP"
     )
    await safe_send(context.bot, CANAL_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
    logger.info("urgencia: oferta relâmpago enviada.")

# ==============================
# INICIALIZAÇÃO DO BOT E WEBHOOK
# ==============================
# Persistência de dados
persistence = PicklePersistence(filepath="bot_data.pkl")

# Cria a aplicação do telegram
application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

# Handlers de comando
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("painel", painel_command))
application.add_handler(CallbackQueryHandler(callback_handler))

# JobQueue para rotinas automáticas
job_queue = application.job_queue
job_queue.run_repeating(rotina_diaria, interval=3600, first=10)
job_queue.run_daily(reset_diario, time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
job_queue.run_repeating(provas_sociais, interval=7200, first=60)
# Envia urgência em horários específicos (10h, 15h, 20h UTC)
job_queue.run_daily(urgencia, time=datetime.time(hour=10, tzinfo=datetime.timezone.utc))
job_queue.run_daily(urgencia, time=datetime.time(hour=15, tzinfo=datetime.timezone.utc))
job_queue.run_daily(urgencia, time=datetime.time(hour=20, tzinfo=datetime.timezone.utc))

# ==============================
# FLASK (para receber o webhook do Telegram)
# ==============================
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Servidor do Bot está no ar!"

@app_flask.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(flask_request.get_json(force=True), application.bot)
    await application.process_update(update)
    return 'ok'

# ==============================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO (main)
# ==============================
async def main():
    # Inicializa o bot e os jobs
    await application.initialize()
    
    # Configura o webhook
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    
    # Configuração para rodar o Flask com Hypercorn
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config()
    config.bind = [f"0.0.0.0:{PORT}"]
    config.use_reloader = False # Importante para produção
    
    logger.info(f"🤖 Iniciando servidor web na porta {PORT}...")
    
    # Roda o servidor web (que por sua vez recebe os updates do webhook)
    await serve(app_flask, config)

if __name__ == "__main__":
    # Verifica se as variáveis essenciais estão configuradas
    if not BOT_TOKEN or not WEBHOOK_URL:
        logger.error("ERRO: BOT_TOKEN e WEBHOOK_URL devem ser definidos nas variáveis de ambiente!")
    else:
        try:
            # Instala uvloop para melhor performance se disponível
            import uvloop
            uvloop.install()
        except ImportError:
            logger.info("uvloop não encontrado, usando asyncio padrão.")
        
        # Roda a função principal assíncrona
        asyncio.run(main())

