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

# 🔥 Novo: link VIP fixo e cupom
VIP_INVITE_LINK = "https://t.me/+2R3sRz1ZUOwzODRh"
VIP_COUPON = "GESTAO"

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
        "🔑 Use o *cupom GESTAO* para ativar seu VIP vitalício.\n\n"
        f"👉 Entre agora: {VIP_INVITE_LINK}\n\n"
        "📌 Lembre-se: dentro do VIP você terá sinais exclusivos, sorteios e bônus (verifique o canal VIP)."
    )
# ----------------------------
# Handlers / Fluxo principal
# ----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensagem inicial do /start"""
    msg = (
        "👋 Olá, seja bem-vindo!\n\n"
        "📌 Aqui você recebe sinais *GRÁTIS* todos os dias.\n\n"
        f"🚀 Para ter acesso *VITALÍCIO* ao nosso grupo VIP exclusivo, use o cupom *{VIP_COUPON}*.\n\n"
        f"👉 Link direto para o VIP: {VIP_INVITE_LINK}\n\n"
        "🔥 Dentro do VIP você terá sinais premium, sorteios e bônus exclusivos."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def post_random_proof(context: ContextTypes.DEFAULT_TYPE):
    """Posta prova social aleatória no canal FREE"""
    img = random_proof_image()
    if img:
        caption = (
            "📸 *Prova Social:*\n\n"
            "Mais um membro lucrando com nossos sinais! 🚀\n\n"
            f"👉 Quer também? Entre no VIP com o cupom *{VIP_COUPON}* e garanta acesso vitalício.\n"
            f"{VIP_INVITE_LINK}"
        )
        await context.bot.send_photo(
            chat_id=FREE_CHAT_ID,
            photo=InputFile(img),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔥 Entrar no VIP Vitalício", url=VIP_INVITE_LINK)]]
            ),
        )


async def auto_signals_job(context: ContextTypes.DEFAULT_TYPE):
    """Posta sinais automáticos em FREE e VIP"""
    signal_text = (
        "🎯 *SINAL AUTOMÁTICO*\n\n"
        "✅ Entrada confirmada no BacBo!\n\n"
        f"🚀 Quer mais sinais como esse? Entre no VIP agora com o cupom *{VIP_COUPON}* e tenha acesso vitalício:\n"
        f"{VIP_INVITE_LINK}"
    )

    # FREE
    await context.bot.send_message(
        chat_id=FREE_CHAT_ID,
        text=signal_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔥 Acessar VIP Vitalício", url=VIP_INVITE_LINK)]]
        ),
    )

    # VIP
    await context.bot.send_message(
        chat_id=VIP_CHAT_ID,
        text="💎 *VIP EXCLUSIVO:*\n\n" + signal_text,
        parse_mode="Markdown",
    )


async def handle_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Usuário envia print de depósito"""
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        filename = f"{DEPOSITS_DIR}/{update.message.from_user.id}_{datetime.now().timestamp()}.jpg"
        await photo_file.download_to_drive(filename)

        # Notifica admin para aprovar/reprovar
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✅ Aprovar", callback_data=f"approve:{update.message.from_user.id}"),
                    InlineKeyboardButton("❌ Reprovar", callback_data=f"reject:{update.message.from_user.id}"),
                ]
            ]
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📥 Novo comprovante enviado por @{update.message.from_user.username or update.message.from_user.id}\n\n"
                f"ID: {update.message.from_user.id}\n\n"
                "Aprovar para liberar VIP vitalício."
            ),
            reply_markup=keyboard,
        )
        await update.message.reply_text(
            "📌 Seu comprovante foi enviado! Aguarde aprovação do admin.\n\n"
            f"Enquanto isso, já garanta sua vaga no VIP com o cupom *{VIP_COUPON}*:\n{VIP_INVITE_LINK}",
            parse_mode="Markdown",
        )


async def callback_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin aprova/reprova comprovante"""
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split(":")
    user_id = int(user_id)

    if action == "approve":
        add_vip(user_id)
        msg = scarcity_message_template()
        try:
            await context.bot.send_message(chat_id=user_id, text=msg, parse_mode="Markdown")
        except Exception as e:
            logger.error("Erro ao enviar VIP msg para user %s: %s", user_id, e)
        await query.edit_message_text(f"✅ Usuário {user_id} aprovado e liberado VIP vitalício.")

    elif action == "reject":
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Seu comprovante foi rejeitado. Tente novamente ou fale com o suporte."
            )
        except Exception as e:
            logger.error("Erro ao enviar rejeição para user %s: %s", user_id, e)
        await query.edit_message_text(f"❌ Usuário {user_id} foi rejeitado.")
