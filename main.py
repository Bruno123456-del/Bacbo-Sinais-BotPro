import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application, CommandHandler

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Lista de sinais simulados
sinais = [
    "🎲 SINAL BAC BO:\n🔁 Estratégia: Dupla Chance\n🕐 Entrada confirmada!",
    "🎲 SINAL BAC BO:\n🎯 Jogue no ALTO 🔺\n💰 Gestão: 2% da banca",
    "🎲 SINAL BAC BO:\n⚠️ Aposte no PARES\n📊 Probabilidade alta!",
    "🎲 SINAL BAC BO:\n🎯 Estratégia: G1 em ALTO 🔼",
    "🎲 BAC BO SINAL:\n🧠 Estatística indica BAIXO 🔻\n🚨 Gestão conservadora!"
]

# A função para enviar sinais agora deve ser 'async'
async def enviar_sinais_automaticos(bot: Bot):
    """Envia um sinal da lista a cada 10 minutos."""
    index = 0
    while True:
        sinal = sinais[index % len(sinais)]
        try:
            # A chamada de envio de mensagem agora precisa de 'await'
            await bot.send_message(chat_id=CHAT_ID, text=sinal)
            print(f"Sinal enviado: {sinal.splitlines()[0]}") # Log para o console
        except Exception as e:
            print(f"Erro ao enviar sinal: {e}") # Log de erro
        
        index += 1
        # 'asyncio.sleep' substitui 'time.sleep' em código assíncrono
        await asyncio.sleep(600) # 600 segundos = 10 minutos

# O handler do comando /start também deve ser 'async'
async def start(update, context):
    """Handler para o comando /start."""
    # 'await' é necessário para enviar a mensagem
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 Bem-vindo ao canal de sinais BAC BO!"
    )

# A função principal agora é 'async'
async def main():
    """Função principal que configura e inicia o bot."""
    # A classe Bot é usada para o envio automático de sinais
    bot = Bot(token=TOKEN)

    # ApplicationBuilder substitui o Updater
    application = Application.builder().token(TOKEN).build()

    # Adiciona o handler para o comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia a tarefa de envio de sinais em background
    # asyncio.create_task é a forma moderna de rodar tarefas concorrentes
    asyncio.create_task(enviar_sinais_automaticos(bot))

    # Inicia o bot (non-blocking)
    await application.initialize()
    await application.start()
    
    print("Bot iniciado e rodando...")

    # Mantém o bot rodando
    await application.updater.start_polling()
    
    # Para manter o programa principal rodando para sempre
    # você pode usar um loop infinito com um sleep.
    while True:
        await asyncio.sleep(3600) # Dorme por 1 hora, mas a tarefa de sinais continua rodando a cada 10 min


if __name__ == '__main__':
    # 'asyncio.run' é usado para executar a função principal assíncrona
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot desligado.")

