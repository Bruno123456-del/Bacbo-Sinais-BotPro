from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
import random

async def resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Performance dos últimos sinais:\n✅ 13 WINs seguidos\n❌ 2 REDS\n🎯 Aproveitamento: 86%")

async def estrategia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Estratégia de Gestão:\nUtilize apenas 4% da sua banca por entrada (incluindo gales).\nExemplo: banca de R$100 → apostar R$4 por sinal.")

async def suporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Suporte:\nDúvidas? Fale com o admin: @seuadmin")

async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏆 Ranking dos mais engajados:\n1️⃣ @lucrador123\n2️⃣ @galezera\n3️⃣ @greenmaster")

# Prova social com imagens
async def postar_win(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagens = [
        "🔥 Mais um membro lucrando com a gente! É disso que estamos falando. Parabéns!",
        "💰 WIN confirmado! Rumo ao topo!",
        "🏆 Isso que é consistência! Bora pra cima família!"
    ]
    imagens = ["imagens/print_win_1.png", "imagens/print_win_2.png", "imagens/print_win_3.png"]
    imagem_escolhida = random.choice(imagens)
    texto_escolhido = random.choice(mensagens)

    with open(imagem_escolhida, "rb") as img:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(img), caption=texto_escolhido)

def adicionar_comandos_avancados(application: Application):
    application.add_handler(CommandHandler("resultados", resultados))
    application.add_handler(CommandHandler("estrategia", estrategia))
    application.add_handler(CommandHandler("suporte", suporte))
    application.add_handler(CommandHandler("ranking", ranking))
    application.add_handler(CommandHandler("win", postar_win))  # comando manual para postar win
