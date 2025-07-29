import os
import asyncio
import random
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

# 1. CONFIGURAÇÕES INICIAIS
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO", "https://lkwn.cc/f1c1c45a")

bot = Bot(token=TOKEN)

# 2. LISTA DE DIREÇÕES E COBERTURAS (ESCADA ASIÁTICA COM COBERTURA)
direcoes = [
    {"direcao": "Vermelho", "cor_direcao": "🔴", "cobertura": "Amarelo", "cor_cobertura": "🟡"},
    {"direcao": "Preto", "cor_direcao": "⚫", "cobertura": "Amarelo", "cor_cobertura": "🟡"},
]

# 3. FUNÇÃO PARA GERAR UM NOVO SINAL ALEATÓRIO
def gerar_sinal():
    return random.choice(direcoes)

# 4. FUNÇÃO PRINCIPAL DE ENVIO DE SINAL
async def enviar_sinal():
    try:
        sinal = gerar_sinal()

        mensagem_sinal = f"""
🔥 OPORTUNIDADE DE ENTRADA DETECTADA 🔥

▪️ Ativo: BAC BO  
▪️ Direção: {sinal['direcao']} {sinal['cor_direcao']}  
▪️ Cobertura: {sinal['cobertura']} {sinal['cor_cobertura']}  
▪️ Estratégia: Escada Asiática com Cobertura  

PLANO DE AÇÃO:  
1️⃣ Entrada Principal: Meta de +4%  
2️⃣ Proteção 1 (Gale): Se necessário  
3️⃣ Proteção 2 (Gale): Se necessário  

⚠️ Opere com precisão. Siga a gestão.

🎁 BÔNUS DE CADASTRO + GIROS GRÁTIS  
👉 {URL_CADASTRO}
"""

        await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sinal enviado com sucesso.")

    except TelegramError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro ao enviar mensagem: {e}")

# 5. LOOP PARA ENVIAR SINAL A CADA 10 MINUTOS
async def main():
    while True:
        await enviar_sinal()
        await asyncio.sleep(600)  # 10 minutos

# 6. EXECUTAR
if __name__ == "__main__":
    asyncio.run(main())
