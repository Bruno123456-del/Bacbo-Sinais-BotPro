# -*- coding: utf-8 -*-
import os
from telegram import Bot

# Carrega variáveis de ambiente do Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
FREE_CHAT_ID = int(os.getenv("FREE_CHAT_ID", "-1002808626127"))
VIP_CHAT_ID = int(os.getenv("VIP_CHAT_ID", "-1003053055680"))

bot = Bot(token=BOT_TOKEN)

def testar_envio():
    print("Iniciando teste de envio...")

    # Teste no canal FREE
    try:
        bot.send_message(chat_id=FREE_CHAT_ID, text="🚀 Teste no canal FREE funcionando!")
        print("✅ Mensagem enviada no canal FREE com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar no canal FREE: {e}")

    # Teste no canal VIP
    try:
        bot.send_message(chat_id=VIP_CHAT_ID, text="🚀 Teste no canal VIP funcionando!")
        print("✅ Mensagem enviada no canal VIP com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar no canal VIP: {e}")

if __name__ == "__main__":
    testar_envio()
