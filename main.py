# -*- coding: utf-8 -*-
"""
Main bot para BacBo/Sinais - Fluxo:
- posts automáticos em canais FREE e VIP
- testes de envio
- comando /submitdeposit para o usuário enviar print do depósito
- aprovar/reprovar por ADMIN (gera VIP vitalício)
- comandos manuais para enviar sinais por jogo
Configurar variáveis de ambiente no Render:
BOT_TOKEN, FREE_CHAT_ID, VIP_CHAT_ID, ADMIN_ID, AFFILIATE_LINK
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from random import choice, randint
from pathlib import Path

from telegram import (
    Bot,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    ChatAction,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# ----------------------------
# Configuração / Ambiente
# ----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
FREE_CHAT_ID = int(os.getenv("FREE_CHAT_ID", "-1002808626127"))
VIP_CHAT_ID = int(os.getenv("VIP_CHAT_ID", "-1003053055680"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "5011424031"))
AFFILIATE_LINK = os.getenv("AFFILIATE_LINK", "https://lkwn.cc/f1c1c45a")

ROOT = Path(__file__).parent
IMAGES_DIR = ROOT / "imagens"
VIP_DB = ROOT / "vip_users.json"
DEPOSITS_DIR = ROOT / "deposits"

# Cria pastas / db caso não existam
DEPOSITS_DIR.mkdir(parents=True, exist_ok=True)
if not VIP_DB.exists():
    VIP_DB.write_text(json.dumps({"vip_users": []}, indent=2, ensure_ascii=False))

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

# ----------------------------
# Utilitários
# ----------------------------
def load_vips():
    try:
        data = json.loads(VIP_DB.read_text(encoding="utf-8"))
        return set(data.get("vip_users", []))
    except Exception as e:
        logger.error("Erro ao ler vip_users.json: %s", e)
        return set()

def save_vips(vips_set):
    VIP_DB.write_text(json.dumps({"vip_users": list(vips_set)}, indent=2, ensure_ascii=False), encoding="utf-8")

def is_vip(user_id: int) -> bool:
    return str(user_id) in load_vips()

def add_vip(user_id: int):
    vips = load_vips()
    vips.add(str(user_id))
    save_vips(vips)

def remove_vip(user_id: int):
    vips = load_vips()
    vips.discard(str(user_id))
    save_vips(vips)

def random_proof_image():
    files = [p for p in IMAGES_DIR.iterdir() if p.is_file() and p.name.lower().startswith("prova")]
    return choice(files) if files else None

def random_win_image(kind="entrada"):
    # kind: entrada, gale1, gale2, empate
    mapping = {
        "entrada": "win_entrada.png",
        "gale1": "win_gale1.png",
        "gale2": "win_gale2.png",
        "empate": "win_empate.png",
    }
    p = IMAGES_DIR / mapping.get(kind, "win_entrada.png")
    return p if p.exists() else None

def scarcity_message_template():
    return (
        "🔥 *ACESSO VIP LIBERADO (vitalício)* 🔥\n\n"
        "Parabéns! Sua prova foi aprovada — ✅ você acaba de garantir *ACESSO VITALÍCIO* ao clube VIP.\n\n"
        "🔒 Vagas limitadas liberadas pelo CEO. Só alguns usuários selecionados ganharam acesso — "
        "essa oferta é exclusiva e pode ser encerrada a qualquer momento.\n\n"
        f"👉 Use o bônus e entre agora: {AFFILIATE_LINK}\n\n"
        "📌 Lembre-se: dentro do VIP você terá sinais exclusivos, sorteios e bônus (verifique o canal VIP)."
    )

# ----------------------------
# Handlers
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"Olá, {user.first_name} 👋\n\n"
        "Bem-vindo(a)! Aqui você pode receber sinais gratuitos e se qualificar para *VIP vitalício*.\n\n"
        "➡️ Envie seu print de depósito usando /submitdeposit para solicitar acesso VIP.\n"
        "➡️ Receba 1 sinal por jogo (Bac Bo, Slots, Roleta, Aviator...) via nosso canal FREE.\n\n"
        "Se precisar, fale com o administrador."
    )
    await update.message.reply_markdown_v2(text)

# Comando para enviar um sinal manual (apenas admin)
async def signal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Apenas admin pode enviar sinais manuais.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Uso: /signal <jogo> <mensagem curta>\nEx: /signal bacbo Entrada 1: BANCO")
        return

    jogo = context.args[0].lower()
    texto = " ".join(context.args[1:])
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar (Afiliado)", url=AFFILIATE_LINK)]])
    # Defina imagens por jogo se quiser
    image = None
    if jogo in ("bacbo", "baccarat", "bac"):
        image = random_win_image("entrada")
    elif jogo in ("gale1",):
        image = random_win_image("gale1")
    elif jogo in ("gale2",):
        image = random_win_image("gale2")
    elif jogo in ("aviator", "slot", "slots", "roleta"):
        image = random_proof_image()

    # Envia para FREE e VIP (se apropriado)
    caption = f"*{jogo.upper()}*\n{texto}\n\n{AFFILIATE_LINK}"
    try:
        if image:
            await bot.send_chat_action(chat_id=FREE_CHAT_ID, action=ChatAction.UPLOAD_PHOTO)
            await bot.send_photo(chat_id=FREE_CHAT_ID, photo=InputFile(image), caption=caption, reply_markup=keyboard)
            await bot.send_photo(chat_id=VIP_CHAT_ID, photo=InputFile(image), caption=caption, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=FREE_CHAT_ID, text=caption, reply_markup=keyboard)
            await bot.send_message(chat_id=VIP_CHAT_ID, text=caption, reply_markup=keyboard)
        await update.message.reply_text("Sinal enviado nos canais FREE e VIP.")
    except Exception as e:
        await update.message.reply_text(f"Erro ao enviar sinal: {e}")

# Comando para o usuário submeter print do depósito
async def submit_deposit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Envie aqui o *print* do depósito (foto) feito com o link da oferta. "
        "Após o envio, nossa equipe irá analisar e você receberá resposta em até algumas horas.",
        parse_mode="Markdown"
    )

# Receber a foto (ou mensagem encaminhada) com o print do depósito
async def handle_deposit_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # Só aceitaremos em chat privado (segurança). Se for em grupo, ignore.
    if chat.type != "private":
        return

    # Se for foto
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{user.id}_{timestamp}.jpg"
        save_path = DEPOSITS_DIR / filename
        await file.download_to_drive(custom_path=str(save_path))
        logger.info("Deposit saved: %s", save_path)

    # Se for documento (imagem enviada como arquivo)
    elif update.message.document:
        doc = update.message.document
        file = await doc.get_file()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{user.id}_{timestamp}_{doc.file_name}"
        save_path = DEPOSITS_DIR / filename
        await file.download_to_drive(custom_path=str(save_path))
        logger.info("Deposit saved (doc): %s", save_path)

    # Se for encaminhado mensagem do canal com print
    elif update.message.forward_from_chat or update.message.forward_from:
        # tenta pegar foto dentro da mensagem encaminhada
        if update.message.photo:
            # same as above; handled already
            pass
        # salvar mensagem como .txt com conteúdo
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        textfile = DEPOSITS_DIR / f"{user.id}_{timestamp}_forward.txt"
        textfile.write_text(update.message.text or "<sem texto>", encoding="utf-8")
        save_path = textfile
    else:
        await update.message.reply_text("Envie uma foto (print) do depósito, por favor.")
        return

    # Notifica o usuário e envia para admin revisar
    await update.message.reply_text(
        "✅ Recebi seu print. Vou enviar para análise. Aguarde o retorno do admin."
    )

    # Envia para o admin com buttons Aprovar/Reprovar
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Aprovar (VIP vitalício)", callback_data=f"approve::{user.id}::{save_path.name}")],
        [InlineKeyboardButton("❌ Reprovar", callback_data=f"reject::{user.id}::{save_path.name}")]
    ])

    caption = (
        f"Nova solicitação de VIP por depósito.\n\nUsuário: {user.full_name} (@{user.username})\nID: {user.id}\nHora(UTC): {datetime.utcnow()}\n\n"
        f"Arquivo: {save_path.name}"
    )

    try:
        # envia arquivo para admin com botões
        await bot.send_chat_action(chat_id=ADMIN_ID, action=ChatAction.UPLOAD_PHOTO)
        if save_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            await bot.send_photo(chat_id=ADMIN_ID, photo=InputFile(save_path), caption=caption, reply_markup=keyboard)
        else:
            await bot.send_document(chat_id=ADMIN_ID, document=InputFile(save_path), caption=caption, reply_markup=keyboard)
    except Exception as e:
        logger.error("Erro ao enviar deposit para admin: %s", e)
        await update.message.reply_text("Erro ao notificar admin. Tente novamente mais tarde.")

# Callback Query do admin aprovar/reprovar
async def callback_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data  # formato: "approve::USERID::FILENAME" ou "reject::USERID::FILENAME"
    parts = data.split("::")
    if len(parts) < 3:
        await query.edit_message_text("Payload inválido.")
        return

    action, user_id_str, filename = parts[0], parts[1], parts[2]
    admin_id = update.effective_user.id
    if admin_id != ADMIN_ID:
        await query.edit_message_text("Apenas o ADMIN pode aprovar ou reprovar.")
        return

    user_id = int(user_id_str)
    saved_path = DEPOSITS_DIR / filename

    if action == "approve":
        # adiciona VIP
        add_vip(user_id)
        # notifica o usuário que foi aprovado
        try:
            await bot.send_message(chat_id=user_id,
                                   text="🎉 *Seu depósito foi aprovado!* Você recebeu *ACESSO VIP VITALÍCIO*.\n\n"
                                        "Use o link e aproveite os bônus agora:\n" + AFFILIATE_LINK,
                                   parse_mode="Markdown")
        except Exception as e:
            logger.warning("Não foi possível enviar mensagem ao usuário aprovado: %s", e)

        # Mensagem de escassez no VIP canal
        try:
            await bot.send_message(chat_id=VIP_CHAT_ID, text=scarcity_message_template(), parse_mode="Markdown")
        except Exception as e:
            logger.warning("Erro ao anunciar no VIP: %s", e)

        await query.edit_message_caption(caption=(query.message.caption or "") + "\n\n✅ APROVADO (VIP concedido)")
        await query.message.reply_text(f"Usuário {user_id} aprovado e VIP concedido.")
    else:
        # reject
        try:
            await bot.send_message(chat_id=user_id,
                                   text="❌ Sua solicitação de VIP foi *reprovada*.\nVerifique se o print contém o depósito feito via nosso link e tente novamente.",
                                   parse_mode="Markdown")
        except Exception as e:
            logger.warning("Não foi possível notificar usuário de reprovação: %s", e)
        await query.edit_message_caption(caption=(query.message.caption or "") + "\n\n❌ REPROVADO")
        await query.message.reply_text(f"Usuário {user_id} reprovado.")

# Comando para checar VIP
async def me_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_vip(uid):
        await update.message.reply_text("✔️ Você é VIP vitalício. Bem-vindo ao clube!")
    else:
        await update.message.reply_text("ℹ️ Você ainda não é VIP. Use /submitdeposit para enviar seu print.")

# Teste que posta prova social aleatória no FREE
async def post_random_proof(context: ContextTypes.DEFAULT_TYPE):
    img = random_proof_image()
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar e Ganhar (Afiliado)", url=AFFILIATE_LINK)]])
    caption = (
        "💬 *Prova Social*\n\nVeja mais um depoimento dos nossos membros que transformaram sua banca. "
        "Quer resultados? Acesse e confira: " + AFFILIATE_LINK
    )
    try:
        if img:
            await bot.send_photo(chat_id=FREE_CHAT_ID, photo=InputFile(img), caption=caption, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=FREE_CHAT_ID, text=caption, reply_markup=keyboard)
    except Exception as e:
        logger.error("Erro ao postar prova social: %s", e)

# Job automático para enviar 1 sinal por jogo (configurável)
async def auto_signals_job(context: ContextTypes.DEFAULT_TYPE):
    # Defina os jogos que quer enviar sinais (um por vez, rotativo)
    jogos = ["bacbo", "aviator", "roleta", "slots", "especial"]
    jogo = choice(jogos)
    texto_sinal = {
        "bacbo": "Entrada: BANCO | Gestão 1% da banca",
        "aviator": "Aviator - Entrada conservadora: aguardar 1.20x",
        "roleta": "Roleta - Apostar no vermelho/negro (gestão conservadora)",
        "slots": "Slots - Teste spin moderado",
        "especial": "Sinal Especial: Observando padrão. Jogar com cautela."
    }.get(jogo, "Entrada genérica")

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar (Afiliado)", url=AFFILIATE_LINK)]])
    img = random_proof_image() if randint(0, 1) else random_win_image("entrada")

    caption = f"*{jogo.upper()}*\n{texto_sinal}\n\n{AFFILIATE_LINK}"

    try:
        if img:
            await bot.send_photo(chat_id=FREE_CHAT_ID, photo=InputFile(img), caption=caption, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=FREE_CHAT_ID, text=caption, reply_markup=keyboard)
        # Opcional: enviar no VIP também, dependendo da sua estratégia
        # await bot.send_message(chat_id=VIP_CHAT_ID, text=caption, reply_markup=keyboard)
        logger.info("Sinal automático enviado: %s", jogo)
    except Exception as e:
        logger.error("Erro ao enviar sinal automático: %s", e)

# Admin only: listar VIPs
async def list_vips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Apenas admin.")
        return
    vips = sorted(load_vips())
    await update.message.reply_text("VIPs:\n" + ("\n".join(vips) if vips else "Nenhum VIP"))

# Health / ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("PONG")

# ----------------------------
# Setup Bot (handlers + jobs)
# ----------------------------
def build_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("submitdeposit", submit_deposit_cmd))
    app.add_handler(CommandHandler("me_vip", me_vip))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("signal", signal_cmd))  # admin manual signal
    app.add_handler(CommandHandler("list_vips", list_vips))  # admin

   # message handler for photos/docs in private chat (deposit)
    app.add_handler(MessageHandler(filters.PHOTO & filters.ChatType.PRIVATE, handle_deposit_message))
    app.add_handler(MessageHandler(filters.Document.IMAGE & filters.ChatType.PRIVATE, handle_deposit_message))
    app.add_handler(CallbackQueryHandler(callback_admin_action))

    # Jobs: agendar provas e sinais automáticos
    job_queue = app.job_queue
    # prova social a cada 60 minutos (ajuste conforme necessidade)
    job_queue.run_repeating(post_random_proof, interval=60*60, first=10)
    # sinal rotativo a cada 10 minutos
    job_queue.run_repeating(auto_signals_job, interval=10*60, first=30)

    return app

# ----------------------------
# Main Run
# ----------------------------
if __name__ == "__main__":
    application = build_app()
    logger.info("Bot iniciando...")
    application.run_polling()
