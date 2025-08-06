import os
import asyncio
import random
from datetime import datetime, time as dt_time
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import TelegramError
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

# Caminhos das imagens e gifs
IMG_WIN = "imagens/win-futurista.gif"
IMG_EMPATE = "imagens/empate.png"
IMG_AGRADECIMENTO = "imagens/agradecimento.png"

# Frases personalizadas
frases_ganhou = [
    "✅ ENTRADA CONFIRMADA! Aposte agora com estratégia e foco!",
    "🎯 SINAL ENVIADO! Aproveite com gestão de banca inteligente.",
    "💰 APOSTA LIBERADA! Mantenha sua disciplina e siga o plano.",
    "📊 SINAL DE ALTA CONFIANÇA! Use cobertura se necessário.",
    "🚀 NOVO SINAL! Prepare-se para a ação e siga o gerenciamento.",
    "🔥 OPORTUNIDADE QUENTE! Analise e entre com sabedoria.",
    "🔔 ATENÇÃO! Mais um sinal fresquinho para você. Bora pra cima!",
    "🍀 SINAL DA SORTE! Acompanhe e faça sua jogada.",
    "📈 HORA DE AGIR! Sinal confirmado para você. Sucesso!",
    "💎 SINAL EXCLUSIVO! Não perca essa chance. Boa sorte!",
]

frases_agradecimento = [
    "Ganhei R$320 com seus sinais hoje! Gratidão 🙏🔥",
    "Você é brabo! Bati minha meta em 1 hora 💰🚀",
    "Confiei e tô no lucro! Obrigado 🔥💸",
    "Nunca ganhei tanto assim, bora pra cima 🔥🎯",
    "Incrível! Meus lucros dispararam com seus sinais. Muito obrigado!",
    "Meta batida e com folga! Vocês são demais!",
    "Finalmente um sinal que funciona de verdade! Gratidão eterna.",
    "Que dia! Graças a vocês, meu saldo só cresce. Valeu!",
    "Estou impressionado com a assertividade. Parabéns pelo trabalho!",
    "Meu dia mudou depois de seguir seus sinais. Muito feliz!",
]

# Mensagem de boas-vindas no terminal
print("Bot de Sinais BAC BO INICIADO...")

# Variáveis de controle para mensagens de início/fim de período
mensagem_inicio_manha_enviada = False
mensagem_fim_manha_enviada = False
mensagem_inicio_noite_enviada = False
mensagem_fim_noite_enviada = False

# Verifica se está no horário permitido e envia mensagens de início/fim
def dentro_do_horario():
    global mensagem_inicio_manha_enviada, mensagem_fim_manha_enviada,
           mensagem_inicio_noite_enviada, mensagem_fim_noite_enviada

    agora = datetime.now().time()
    hora_atual = datetime.now().hour

    # Período da manhã
    if dt_time(13, 0) <= agora <= dt_time(17, 0):
        if not mensagem_inicio_manha_enviada:
            asyncio.create_task(bot.send_message(chat_id=CHAT_ID, text="☀️ Bom dia, pessoal! Nossos sinais de BAC BO estão ativos. Fiquem ligados para as melhores oportunidades!"))
            mensagem_inicio_manha_enviada = True
            mensagem_fim_manha_enviada = False # Reset para o próximo ciclo
        return True
    elif hora_atual > 17 and not mensagem_fim_manha_enviada and mensagem_inicio_manha_enviada:
        asyncio.create_task(bot.send_message(chat_id=CHAT_ID, text="👋 Pessoal, o período de sinais da manhã foi encerrado. Voltamos à noite com mais oportunidades!"))
        mensagem_fim_manha_enviada = True
        mensagem_inicio_manha_enviada = False # Reset para o próximo ciclo

    # Período da noite
    if dt_time(19, 0) <= agora <= dt_time(22, 0):
        if not mensagem_inicio_noite_enviada:
            asyncio.create_task(bot.send_message(chat_id=CHAT_ID, text="🌙 Boa noite, traders! Estamos de volta com os sinais de BAC BO. Preparem-se para lucrar!"))
            mensagem_inicio_noite_enviada = True
            mensagem_fim_noite_enviada = False # Reset para o próximo ciclo
        return True
    elif hora_atual > 22 and not mensagem_fim_noite_enviada and mensagem_inicio_noite_enviada:
        asyncio.create_task(bot.send_message(chat_id=CHAT_ID, text="😴 É isso aí, galera! Encerramos os sinais de BAC BO por hoje. Amanhã tem mais! Boa noite a todos."))
        mensagem_fim_noite_enviada = True
        mensagem_inicio_noite_enviada = False # Reset para o próximo ciclo

    return False
# Envia um sinal para o canal
async def enviar_sinal():
    if not dentro_do_horario():
        print("⏰ Fora do horário dos sinais.")
        return

    try:
        frase = random.choice(frases_ganhou)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"🎲 BAC BO SINAL AO VIVO\n\n{frase}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🎰 Jogar Bac Bo Agora", url="https://lkwn.cc/f1c1c45a")
            ]])
        )

        # Imagem empate (aleatoriamente 20% das vezes)
        if random.random() < 0.2:
            await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_EMPATE, "rb"))

        # GIF vitória futurista (aleatoriamente 60% das vezes)
        if random.random() < 0.6:
            await bot.send_animation(chat_id=CHAT_ID, animation=open(IMG_WIN, "rb"))

        # Imagem de agradecimento (aleatoriamente 40% das vezes)
        if random.random() < 0.4:
            mensagem = random.choice(frases_agradecimento)
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=open(IMG_AGRADECIMENTO, "rb"),
                caption=f"📩 *Mensagem recebida:*\n\n_{mensagem}_",
                parse_mode="Markdown"
            )

    except TelegramError as e:
        print(f"Erro ao enviar sinal: {e}")

# Loop de envio automático com intervalo randomizado
async def agendar_sinais():
    while True:
        if dentro_do_horario():
            await enviar_sinal()
            # Intervalo ajustado para o ritmo do Bac Bo (entre 30 e 90 segundos)
            intervalo = random.randint(30, 90)  # Entre 30 e 90 segundos
            print(f"⏳ Próximo sinal em {intervalo} segundos.")
            await asyncio.sleep(intervalo)
        else:
            # Fora do horário, verifica a cada 1 minuto para pegar o início do próximo período
            await asyncio.sleep(60)  # Espera 1 minuto fora do horário

# Flask para manter vivo no Render
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Bot BAC BO Sinais Ativo!"

# Executa bot e webserver
if __name__ == "__main__":
    import threading

    loop = asyncio.get_event_loop()
    threading.Thread(target=lambda: loop.run_until_complete(agendar_sinais())).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
