import random
import telebot
from telebot.types import InputFile

def adicionar_comandos_avancados(bot: telebot.TeleBot):
    def resultados(message):
        bot.send_message(message.chat.id, "📈 Performance dos últimos sinais:\n✅ 13 WINs seguidos\n❌ 2 REDS\n🎯 Aproveitamento: 86%")

    def estrategia(message):
        bot.send_message(message.chat.id, "📊 Estratégia de Gestão:\nUtilize apenas 4% da sua banca por entrada (incluindo gales).\nExemplo: banca de R$100 → apostar R$4 por sinal.")

    def suporte(message):
        bot.send_message(message.chat.id, "📞 Suporte:\nDúvidas? Fale com o admin: @seuadmin")

    def ranking(message):
        bot.send_message(message.chat.id, "🏆 Ranking dos mais engajados:\n1️⃣ @lucrador123\n2️⃣ @galezera\n3️⃣ @greenmaster")

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

        try:
            with open(imagem_escolhida, "rb") as img:
                bot.send_photo(chat_id=message.chat.id, photo=img, caption=texto_escolhido)
        except FileNotFoundError:
            bot.send_message(message.chat.id, f"Erro: Imagem não encontrada em {imagem_escolhida}. Certifique-se de que a pasta 'imagens' e os arquivos estão no local correto.")

    bot.message_handler(commands=["resultados"])(resultados)
    bot.message_handler(commands=["estrategia"])(estrategia)
    bot.message_handler(commands=["suporte"])(suporte)
    bot.message_handler(commands=["ranking"])(ranking)
    bot.message_handler(commands=["win"])(postar_win)


