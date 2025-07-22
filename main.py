import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Configuração Inicial ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_BONUS = os.getenv("URL_BONUS", "https://seusite.com/bonus" )

# --- Estrutura dos Sinais ---
# Agora cada sinal é um dicionário com mais detalhes
sinais_config = [
    {"aposta": "Banker (Azul) 🔵", "estrategia": "Sequência de Cores", "gale": 1},
    {"aposta": "Player (Vermelho) 🔴", "estrategia": "Quebra de Padrão", "gale": 0},
    {"aposta": "Banker (Azul) 🔵", "estrategia": "Análise de Pares", "gale": 1},
    {"aposta": "Player (Vermelho) 🔴", "estrategia": "Tendência Dominante", "gale": 0},
    {"aposta": "Banker (Azul) 🔵", "estrategia": "Retorno à Média", "gale": 2}
]

# --- Funções do Bot ---

async def enviar_sinais(bot: Bot):
    """Envia um sinal detalhado e agenda o envio do resultado."""
    index = 0
    while True:
        config = sinais_config[index % len(sinais_config)]
        
        # Monta a mensagem do sinal
        gale_text = f"Cobrir no Gale {config['gale']}" if config['gale'] > 0 else "Entrada única"
        mensagem_sinal = (
            f"💎 **SINAL BAC BO CONFIRMADO** 💎\n\n"
            f"👇 Apostar em: **{config['aposta']}**\n"
            f"📈 Estratégia: *{config['estrategia']}*\n"
            f"🔁 Proteção: *{gale_text}*\n\n"
            f"📲 Fique atento ao resultado!"
        )
        
        try:
            # Envia o sinal e guarda a mensagem para poder respondê-la depois
            mensagem_enviada = await bot.send_message(
                chat_id=CHAT_ID,
                text=mensagem_sinal,
                parse_mode='Markdown'
            )
            print(f"Sinal enviado: {config['aposta']}")
            
            # Agenda o envio do resultado para daqui a 2 minutos (120 segundos)
            asyncio.create_task(enviar_resultado(bot, mensagem_enviada.message_id))

        except Exception as e:
            print(f"Erro ao enviar sinal: {e}")
        
        index += 1
        # Pausa de 10 minutos para o próximo sinal
        await asyncio.sleep(600)

async def enviar_resultado(bot: Bot, id_mensagem_sinal: int):
    """Simula e envia o resultado de um sinal."""
    # Espera 2 minutos antes de enviar o resultado
    await asyncio.sleep(120) 
    
    # Simula um resultado (85% de chance de Green)
    resultado = random.choices(["GREEN ✅", "RED ❌"], weights=[0.85, 0.15], k=1)[0]
    
    mensagem_resultado = f"🏁 **Resultado do Sinal** 🏁\n\n🎉 **{resultado}**! Continue gerenciando sua banca."
    
    try:
        # Envia o resultado respondendo à mensagem do sinal original
        await bot.send_message(
            chat_id=CHAT_ID,
            text=mensagem_resultado,
            reply_to_message_id=id_mensagem_sinal,
            parse_mode='Markdown'
        )
        print(f"Resultado enviado: {resultado}")
    except Exception as e:
        print(f"Erro ao enviar resultado: {e}")

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia uma mensagem com um botão de bônus."""
    texto = "Clique no botão abaixo para pegar seu bônus exclusivo! 🎁"
    botao = InlineKeyboardButton(text="Pegar Bônus Agora!", url=URL_BONUS)
    teclado = InlineKeyboardMarkup([[botao]])
    await update.message.reply_text(text=texto, reply_markup=teclado)

async def main():
    """Configura e inicia o bot."""
    print("Iniciando o bot...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("bonus", bonus))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em execução.")

    asyncio.create_task(enviar_sinais(application.bot))
    print(f"Envio de sinais para o chat {CHAT_ID} agendado.")

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
