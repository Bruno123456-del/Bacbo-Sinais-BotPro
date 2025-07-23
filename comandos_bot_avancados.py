import random
import telebot
from telebot.types import InputFile

def resultados(message):
    message.reply_text("📈 Performance dos últimos sinais:\n✅ 13 WINs seguidos\n❌ 2 REDS\n🎯 Aproveitamento: 86%")

def estrategia(message):
    message.reply_text("📊 Estratégia de Gestão:\nUtilize apenas 4% da sua banca por entrada (incluindo gales).\nExemplo: banca de R$100 → apostar R$4 por sinal.")

def suporte(message):
    message.reply_text("📞 Suporte:\nDúvidas? Fale com o admin: @seuadmin")

def ranking(message):
    message.reply_text("🏆 Ranking dos mais engajados:\n1️⃣ @lucrador123\n2️⃣ @galezera\n3️⃣ @greenmaster")

# Prova social com imagens
def postar_win(message):
    mensagens = [
        "🔥 Mais um membro lucrando com a gente! É disso que estamos falando. Parabéns!",
        "💰 WIN confirmado! Rumo ao topo!",
        "🏆 Isso que é consistência! Bora pra cima família!"
    ]
    imagens = ["imagens/print_win_1.png", "imagens/print_win_2.png", "imagens/print_win_3.png"]
    imagem_escolhida = random.choice(imagens)
    texto_escolhido = random.choice(mensagens)

    with open(imagem_escolhida, "rb") as img:
        message.bot.send_photo(chat_id=message.chat.id, photo=img, caption=texto_escolhido)

def adicionar_comandos_avancados(bot: telebot.TeleBot):
    bot.message_handler(commands=["resultados"])(resultados)
    bot.message_handler(commands=["estrategia"])(estrategia)
    bot.message_handler(commands=["suporte"])(suporte)
    bot.message_handler(commands=["ranking"])(ranking)
    bot.message_handler(commands=["win"])(postar_win)
