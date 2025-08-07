import os
import asyncio
import random
from datetime import datetime, time as dt_time
from telegram import Bot, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
LINK_AFILIADO = os.getenv("LINK_AFILIADO", "https://lkwn.cc/f1c1c45a")

bot = Bot(token=TOKEN)

# Estratégia
def gerar_sinal():
    return random.choice([
        ("Azul 🔵 ➡️ Verde 🟢", "Amarelo 🟡"),
        ("Verde 🟢 ➡️ Azul 🔵", "Amarelo 🟡"),
        ("Azul 🔵 ➡️ Amarelo 🟡", "Verde 🟢"),
        ("Verde 🟢 ➡️ Amarelo 🟡", "Azul 🔵"),
        ("Amarelo 🟡 ➡️ Azul 🔵", "Verde 🟢"),
        ("Amarelo 🟡 ➡️ Verde 🟢", "Azul 🔵"),
    ])

def dentro_do_horario():
    agora = datetime.now().time()
    return (
        dt_time(13, 0) <= agora <= dt_time(17, 59) or
        dt_time(19, 0) <= agora <= dt_time(22, 0)
    )

async def enviar_imagem_aleatoria(pasta, prefixo):
    arquivos = [
        f for f in os.listdir(pasta)
        if f.startswith(prefixo) and f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]
    if arquivos:
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        with open(caminho, 'rb') as f:
            if escolhido.endswith(".gif"):
                await bot.send_animation(chat_id=CHANNEL_ID, animation=InputFile(f))
            else:
                await bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(f))
        print(f"✅ Enviado: {escolhido}")
    else:
        print(f"❌ Nenhuma imagem encontrada com prefixo: {prefixo}")

async def enviar_sinal():
    if dentro_do_horario():
        principal, cobertura = gerar_sinal()
        horario = datetime.now().strftime("%H:%M:%S")

        texto = (
            f"🚨 *NOVO SINAL BAC BO AO VIVO*\n\n"
            f"🎯 Estratégia: Escada Asiática\n"
            f"🎲 Entrada: {principal}\n"
            f"🛡️ Cobertura: {cobertura} (Empate)\n\n"
            f"🕐 Horário: {horario}\n"
            f"⚠️ Validade: 3 rodadas\n\n"
            f"🎰 Casa: 1WIN - Use o botão abaixo:"
        )

        botoes = InlineKeyboardMarkup([[
            InlineKeyboardButton("🎰 APOSTAR AGORA", url=LINK_AFILIADO),
            InlineKeyboardButton("🎓 Ver Estratégia", url="https://bac-bo-ignite.lovable.app/")
        ]])

        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=texto,
                reply_markup=botoes,
                parse_mode='Markdown'
            )
            print(f"[{horario}] Sinal enviado.")

            # Após o sinal, envia automaticamente imagens sociais:
            await asyncio.sleep(15)
            await enviar_imagem_aleatoria("imagens", "win_entrada")

            await asyncio.sleep(15)
            await enviar_imagem_aleatoria("imagens", "win_gale1")

            await asyncio.sleep(15)
            await enviar_imagem_aleatoria("imagens", "win_gale2")

            await asyncio.sleep(15)
            await enviar_imagem_aleatoria("imagens", "win_empate")

            await asyncio.sleep(15)
            await enviar_imagem_aleatoria("imagens", "prova")

        except Exception as e:
            print(f"❌ Erro ao enviar sinal: {e}")
    else:
        print("⏰ Fora do horário permitido.")

async def agendar_sinais():
    while True:
        agora = datetime.now()
        if dentro_do_horario() and agora.minute % 10 == 0 and agora.second < 10:
            await enviar_sinal()
            await asyncio.sleep(60)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(agendar_sinais())
