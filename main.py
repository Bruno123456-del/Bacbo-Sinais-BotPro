import os
import time
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURAÇÕES PRINCIPAIS ---

# Use variáveis de ambiente para o Token e Chat ID para maior segurança.
# Você irá configurar isso diretamente no site da Render.com.
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Verificação inicial para garantir que as variáveis de ambiente foram configuradas.
if not TOKEN or not CHAT_ID:
    print("Erro: As variáveis de ambiente TELEGRAM_TOKEN e TELEGRAM_CHAT_ID não foram configuradas.")
    exit()

bot = telebot.TeleBot(TOKEN)

# --- CONFIGURAÇÕES DO JOGO E ESTRATÉGIA ---

# Opções de aposta e seus respectivos emojis
options = ["Player", "Banker", "Tie"]
emojis = {"Player": "🔵", "Banker": "🔴", "Tie": "🟢"}

# Gestão de Banca e Martingale (totalmente configurável)
# Recomendação: Banca mínima para a estratégia.
BANCA_MINIMA_RECOMENDADA = 100.00
# Níveis de Martingale como percentual da banca (Ex: 1%, 2%, 4%)
MARTINGALE_NIVEIS_PERCENTUAL = [0.01, 0.02, 0.04] 
# Intervalo entre os sinais em minutos
INTERVALO_SINAIS_MINUTOS = 15

# --- FUNÇÕES DO BOT ---

def gerar_sinal():
    """Gera uma escolha aleatória para o sinal."""
    escolha = random.choice(options)
    emoji = emojis[escolha]
    return escolha, emoji

def enviar_sinal(escolha, emoji, nivel_martingale, banca_atual):
    """Envia a mensagem de sinal formatada para o canal."""
    percentual_aposta = MARTINGALE_NIVEIS_PERCENTUAL[nivel_martingale]
    valor_aposta = banca_atual * percentual_aposta

    gestao_info = (
        f"**Gestão de Risco (Juros Compostos):**\n"
        f"- **Banca Atual:** R$ {banca_atual:.2f}\n"
        f"- **Nível Martingale:** {nivel_martingale + 1}\n"
        f"- **Aposta Sugerida:** {percentual_aposta:.2%} da banca (R$ {valor_aposta:.2f})"
    )

    mensagem = (
        "🚨 **SINAL CONFIRMADO | BAC BO** 🚨\n\n"
        f"🎯 **Entrada:** {emoji} {escolha}\n\n"
        f"{gestao_info}\n\n"
        "**Aviso:** Siga sempre a gestão de banca. Pequenos ganhos consistentes se transformam em grandes fortunas. "
        "A disciplina é a chave do sucesso!\n\n"
        "🔥 **Boa sorte!**"
    )
    
    botoes = InlineKeyboardMarkup()
    botoes.add(InlineKeyboardButton("🎁 Cadastre-se e Ganhe Bônus", url="https://lkwn.cc/f1c1c45a" ))

    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown", reply_markup=botoes)
    print(f"✅ Sinal enviado: {escolha} | Nível Martingale: {nivel_martingale + 1}")

def enviar_mensagem_status(vitoria):
    """Envia uma mensagem de GREEN (vitória) ou RED (derrota)."""
    if vitoria:
        mensagem = "✅ **GREEN!** ✅\n\nParabéns! Sinal finalizado com vitória. Voltamos ao nível 1."
        print("✅ Resultado: GREEN")
    else:
        mensagem = "❌ **RED!** ❌\n\nAtenção! Sinal não bateu. Prepare-se para o próximo nível de Martingale."
        print("❌ Resultado: RED")
        
    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")

def enviar_mensagem_pausa():
    """Envia uma mensagem informando que o bot pausou após atingir o limite de perdas."""
    mensagem = (
        "⚠️ **STOP LOSS ATINGIDO** ⚠️\n\n"
        "Atingimos o limite de perdas consecutivas. Para proteger sua banca, o bot fará uma pausa.\n"
        "A disciplina é fundamental. Voltaremos em breve com novos sinais.\n\n"
        "Aproveite para garantir seu bônus de cadastro!"
    )
    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
    print("⚠️ Stop loss atingido. Bot pausado.")

# --- LÓGICA PRINCIPAL ---

def iniciar_bot():
    """Função principal que executa o loop do bot."""
    print("🚀 Bot iniciado com sucesso!")
    bot.send_message(CHAT_ID, "🤖 **Bot de Sinais BAC BO iniciado!**\nAguardando o próximo sinal...", parse_mode="Markdown")
    
    nivel_martingale_atual = 0
    # Simulação de uma banca inicial. Em um sistema real, isso seria gerenciado de forma mais complexa.
    banca_simulada = BANCA_MINIMA_RECOMENDADA 

    while True:
        try:
            # 1. Gerar e enviar o sinal
            escolha, emoji = gerar_sinal()
            enviar_sinal(escolha, emoji, nivel_martingale_atual, banca_simulada)

            # Aguarda um tempo para simular a aposta
            time.sleep(60) 

            # 2. Simular o resultado (70% de chance de vitória para fins de teste)
            vitoria = random.choices([True, False], weights=[0.70, 0.30])[0]
            
            enviar_mensagem_status(vitoria)

            # 3. Atualizar o nível de Martingale
            if vitoria:
                nivel_martingale_atual = 0  # Reseta em caso de vitória
            else:
                nivel_martingale_atual += 1 # Avança para o próximo nível

            # 4. Verificar condição de Stop Loss
            if nivel_martingale_atual >= len(MARTINGALE_NIVEIS_PERCENTUAL):
                enviar_mensagem_pausa()
                # Pausa longa (ex: 12 horas) antes de tentar novamente
                time.sleep(12 * 3600) 
                nivel_martingale_atual = 0 # Reseta os níveis após a pausa
                continue

            # 5. Aguardar o intervalo para o próximo sinal
            print(f"Aguardando {INTERVALO_SINAIS_MINUTOS} minutos para o próximo sinal...")
            time.sleep(INTERVALO_SINAIS_MINUTOS * 60)

        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}")
            time.sleep(60) # Espera 1 minuto antes de tentar novamente

if __name__ == "__main__":
    iniciar_bot()
