import os
import asyncio
import random
import datetime
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest

# --- 1. CONFIGURAÇÃO INICIAL ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a")

# --- 2. IMAGENS E GIFS ---
GIFS_WIN = [f"midia/win{i}.gif" for i in range(1, 11)]  # win1.gif até win10.gif
PRINTS_WIN = [f"midia/print{i}.jpg" for i in range(1, 11)]  # print1.jpg até print10.jpg

IMG_WIN_4 = "midia/win_4.png"   # lucro 4%
IMG_WIN_8 = "midia/win_8.png"   # lucro 8%
IMG_WIN_16 = "midia/win_16.png" # lucro 16%

# --- 3. MENSAGENS FIXAS BILÍNGUES ---
BOAS_VINDAS_PT = f"""
👋 Seja bem-vindo ao canal oficial de sinais BAC BO!

🎯 Aqui você recebe sinais automáticos baseados na estratégia asiática com cobertura.

🎲 Banca ideal inicial: R$ 1000
💸 Entrada principal: R$ 20 (5% da banca)
🛡️ Cobertura: 1-2% sobre a entrada

🎁 Comece agora com bônus especial:
👉 [🎲 Jogar BAC BO com Bônus 🎁]({URL_CADASTRO})
"""

BOAS_VINDAS_ES = f"""
👋 ¡Bienvenido al canal oficial de señales BAC BO!

🎯 Aquí recibirás señales automáticas basadas en la estrategia asiática con cobertura.

🎲 Banca ideal inicial: $1000 pesos (o equivalente)
💸 Entrada principal: $20 (5% de la banca)
🛡️ Cobertura: 1-2% sobre la entrada

🎁 Comienza ahora con un bono especial:
👉 [🎰 Jugar BAC BO con Bono 🎉]({URL_CADASTRO})
"""

MENSAGENS_GATILHO_PT = [
    "💰 Meta do dia batida! Quem pegou comenta 'VEM MAIS' 🔥",
    "📊 Gestão é tudo. Consistência traz resultados. Foco total!",
    "🎁 Bônus disponível. Já garantiu o seu hoje?",
    "💸 Com R$20 já dá pra começar e multiplicar. Bora pro game!",
    "📈 Estratégia validada. Resultados não mentem. Siga o plano."
]

MENSAGENS_GATILHO_ES = [
    "💰 ¡Meta del día alcanzada! Comenta 'VAMOS MÁS' 🔥",
    "📊 La gestión es clave. La constancia trae resultados. ¡Enfócate!",
    "🎁 Bono disponible. ¿Ya lo reclamaste hoy?",
    "💸 Con $20 ya puedes empezar a multiplicar. ¡Vamos al juego!",
    "📈 Estrategia validada. Los resultados no mienten. Sigue el plan."
]

# --- 4. VARIÁVEIS DE CONTROLE ---
placar_diario = {"greens": 0, "reds": 0}
placar_semanal = {"greens": 0, "reds": 0}

# --- 5. FUNÇÕES DE ENVIO ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=BOAS_VINDAS_PT, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar BAC BO com Bônus 🎁 | 🎰 Jugar BAC BO con Bono 🎉", url=URL_CADASTRO)]]))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=BOAS_VINDAS_ES, parse_mode="Markdown")
    except BadRequest:
        pass

async def enviar_gatilho(context: ContextTypes.DEFAULT_TYPE):
    try:
        msg_pt = random.choice(MENSAGENS_GATILHO_PT)
        msg_es = random.choice(MENSAGENS_GATILHO_ES)
        await context.bot.send_message(chat_id=CHAT_ID, text=f"{msg_pt}\n{msg_es}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar BAC BO com Bônus 🎁 | 🎰 Jugar BAC BO con Bono 🎉", url=URL_CADASTRO)]]))
    except BadRequest:
        pass

def gerar_relatorio(dia=True):
    if dia:
        greens = placar_diario["greens"]
        reds = placar_diario["reds"]
        total = greens + reds if (greens + reds) > 0 else 1
        lucro = greens * 4 - reds * 2  # cálculo aproximado simplificado
        aproveitamento = round((greens / total) * 100)
        data = datetime.date.today().strftime("%d/%m")
        titulo = "Relatório do Dia"
    else:
        greens = placar_semanal["greens"]
        reds = placar_semanal["reds"]
        total = greens + reds if (greens + reds) > 0 else 1
        lucro = greens * 20 - reds * 10  # semanal maior valor
        aproveitamento = round((greens / total) * 100)
        data = f"Semana {datetime.date.today().isocalendar()[1]}"
        titulo = "Relatório Semanal"

    relatorio = f"""
📅 *{titulo}* ({data}):
✅ Greens: {greens}
❌ Reds: {reds}
💸 Lucro aproximado: R$ {lucro},00
🏆 Aproveitamento: {aproveitamento}%

"""
    return relatorio

async def enviar_relatorio_diario(bot: Bot):
    relatorio = gerar_relatorio(dia=True)
    msg_pt = random.choice(MENSAGENS_GATILHO_PT)
    msg_es = random.choice(MENSAGENS_GATILHO_ES)
    gif = random.choice(GIFS_WIN)
    print_img = random.choice(PRINTS_WIN)

    try:
        await bot.send_message(chat_id=CHAT_ID, text=relatorio, parse_mode="Markdown")
        await bot.send_animation(chat_id=CHAT_ID, animation=open(gif, "rb"))
        await bot.send_photo(chat_id=CHAT_ID, photo=open(print_img, "rb"), caption="Resultados recentes da comunidade!")
        await bot.send_message(chat_id=CHAT_ID, text=f"{msg_pt}\n{msg_es}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar BAC BO com Bônus 🎁 | 🎰 Jugar BAC BO con Bono 🎉", url=URL_CADASTRO)]]))
    except Exception as e:
        print(f"Erro ao enviar relatório diário: {e}")

async def enviar_relatorio_semanal(bot: Bot):
    relatorio = gerar_relatorio(dia=False)
    msg_pt = random.choice(MENSAGENS_GATILHO_PT)
    msg_es = random.choice(MENSAGENS_GATILHO_ES)
    gif = random.choice(GIFS_WIN)
    print_img = random.choice(PRINTS_WIN)

    try:
        await bot.send_message(chat_id=CHAT_ID, text=relatorio, parse_mode="Markdown")
        await bot.send_animation(chat_id=CHAT_ID, animation=open(gif, "rb"))
        await bot.send_photo(chat_id=CHAT_ID, photo=open(print_img, "rb"), caption="Resultados semanales de la comunidad!")
        await bot.send_message(chat_id=CHAT_ID, text=f"{msg_pt}\n{msg_es}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar BAC BO com Bônus 🎁 | 🎰 Jugar BAC BO con Bono 🎉", url=URL_CADASTRO)]]))
    except Exception as e:
        print(f"Erro ao enviar relatório semanal: {e}")

# Função simulada para sinal e update do placar (exemplo)
async def simular_sinal(bot: Bot):
    # Essa função você pode adaptar para enviar sinais reais e atualizar placar
    global placar_diario, placar_semanal

    # Simular win ou loss
    resultado = random.choices(["green", "red"], weights=[0.8, 0.2])[0]

    if resultado == "green":
        placar_diario["greens"] += 1
        placar_semanal["greens"] += 1
        # Enviar GIF de vitória e imagem 4% exemplo
        await bot.send_animation(chat_id=CHAT_ID, animation=open(random.choice(GIFS_WIN), "rb"))
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_4, "rb"), caption="✅ WIN - +4% de lucro")
    else:
        placar_diario["reds"] += 1
        placar_semanal["reds"] += 1
        # Enviar gif de derrota (você pode criar e adicionar)
        # await bot.send_animation(chat_id=CHAT_ID, animation=open("midia/loss.gif", "rb"))
        await bot.send_message(chat_id=CHAT_ID, text="❌ STOP LOSS - Proteja seu capital!")

    # Enviar mensagem motivacional
    msg_pt = random.choice(MENSAGENS_GATILHO_PT)
    msg_es = random.choice(MENSAGENS_GATILHO_ES)
    await bot.send_message(chat_id=CHAT_ID, text=f"{msg_pt}\n{msg_es}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Jogar BAC BO com Bônus 🎁 | 🎰 Jugar BAC BO con Bono 🎉", url=URL_CADASTRO)]]))

# --- 6. CONFIGURAÇÃO DO BOT ---
async def main():
    print("🤖 Bot BAC BO iniciado.")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    bot = application.bot

    # Enviar mensagem de boas vindas fixada 1 vez (opcional)
    try:
        msg = await bot.send_message(chat_id=CHAT_ID, text=BOAS_VINDAS_PT + "\n" + BOAS_VINDAS_ES, parse_mode="Markdown")
        await bot.pin_chat_message(chat_id=CHAT_ID, message_id=msg.message_id)
    except Exception as e:
        print(f"Erro ao fixar mensagem inicial: {e}")

    # Agendar gatilhos de retenção a cada 3 horas
    application.job_queue.run_repeating(enviar_gatilho, interval=10800, first=30)

    # Agendar relatório diário às 20h
    application.job_queue.run_daily(enviar_relatorio_diario, time=datetime.time(hour=20, minute=0, second=0))

    # Agendar relatório semanal aos domingos 20h
    application.job_queue.run_weekly(enviar_relatorio_semanal, time=datetime.time(hour=20, minute=0, second=0), day_of_week=6)

    # Simular envio de sinal a cada 15 minutos (para demo)
    application.job_queue.run_repeating(lambda ctx: asyncio.create_task(simular_sinal(bot)), interval=900, first=10)

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Loop infinito para manter o bot ativo
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot finalizado.")
