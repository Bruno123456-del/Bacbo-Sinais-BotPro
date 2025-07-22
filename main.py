import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest

# --- 1. CONFIGURAÇÃO INICIAL ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = "https://lkwn.cc/f1c1c45a" # SEU LINK PRINCIPAL

# --- 2. BANCO DE MENSAGENS (Mantido como antes ) ---
# (As mensagens de boas-vindas, reforço, etc., continuam aqui)
mensagem_fixada_texto = f"""
🎰 *Bem-vindo aos SINAIS 1WIN - BAC BO VIP*
... (o resto da mensagem) ...
"""
reforco_pos_win = [ f"🔔 Ainda não está usando a mesma plataforma que a gente? ... {URL_CADASTRO} ...", f"🎯 Green confirmado! ... {URL_CADASTRO}"]
mensagem_automatica_recorrente = f"⏱️ *Dica do dia:* ... {URL_CADASTRO}"

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---
sinais_config = [{"aposta": "Banker (Azul) 🔵", "estrategia": "Tendência"}, {"aposta": "Player (Vermelho) 🔴", "estrategia": "Quebra de Padrão"}]
CHANCE_WIN_ENTRADA_INICIAL = 0.70
CHANCE_WIN_GALE_1 = 0.80
CHANCE_WIN_GALE_2 = 0.90

# --- 4. FUNÇÕES DO BOT ---

async def simular_e_enviar_sinal(bot: Bot):
    """Ciclo completo: analisa, envia sinal com botão de bônus e gerencia os resultados."""
    config = random.choice(sinais_config)
    
    # Mensagem de "Analisando..."
    await bot.send_message(chat_id=CHAT_ID, text="🔎 Analisando os padrões do mercado...")
    await asyncio.sleep(random.randint(5, 10))

    # --- MUDANÇA PRINCIPAL AQUI ---
    # Criação do botão e do teclado que serão anexados à mensagem do sinal
    botao_bonus = InlineKeyboardButton(
        text="🎁 Pegue seu bônus agora 🎁", # Texto do botão
        url=URL_CADASTRO                   # Link que o botão abre
    )
    teclado_com_bonus = InlineKeyboardMarkup([[botao_bonus]]) # Agrupa o botão

    # Montagem da mensagem do sinal
    mensagem_sinal = (
        f"💎 **SINAL DE ENTRADA CONFIRMADO!** 💎\n\n"
        f"🎲 **Jogo:** BAC BO\n"
        f"🎯 **ENTRADA:** **{config['aposta']}**\n"
        f"⏳ **Validade:** 2 minutos\n\n"
        f"🔥 *Mantenha o foco e siga a estratégia!*"
    )
    
    # Envio do sinal JÁ COM O BOTÃO
    msg_sinal_enviada = await bot.send_message(
        chat_id=CHAT_ID,
        text=mensagem_sinal,
        parse_mode='Markdown',
        reply_markup=teclado_com_bonus # Anexa o teclado com o botão à mensagem
    )
    print(f"Sinal enviado com botão de bônus: {config['aposta']}")
    
    await asyncio.sleep(120) # Espera 2 minutos pelo resultado

    # --- Lógica de Resultados com Gales (Exatamente como antes) ---
    # Tentativa 1: WIN
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        resultado_msg = "✅ **WIN DE PRIMEIRA!** ✅\n\n💰 **LUCRO: +4% DA BANCA**"
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        await asyncio.sleep(5)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 2: GALE 1
    await bot.send_message(chat_id=CHAT_ID, text="🔁 **ATENÇÃO!** Vamos para o **GALE 1**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        resultado_msg = "✅ **WIN NO GALE 1!** ✅\n\n💰 **LUCRO: +4% LÍQUIDO (META +8%)**"
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        await asyncio.sleep(5)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 3: GALE 2 ou RED
    # (O resto da lógica continua igual)
    await bot.send_message(chat_id=CHAT_ID, text="🔁 **ÚLTIMA PROTEÇÃO!** Vamos para o **GALE 2**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        resultado_msg = "✅ **WIN NO GALE 2!** ✅\n\n💰 **LUCRO: +4% LÍQUIDO (META +16%)**"
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        await asyncio.sleep(5)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
    else:
        resultado_msg = "❌ **RED!** ❌\n\n⛔️ **STOP LOSS ATINGIDO.** Respeite a gestão."
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')


# --- O resto do código (ciclo_de_sinais, gestao, bonus, main) permanece o mesmo ---
# ...
async def ciclo_de_sinais(bot: Bot):
    """Mantém o bot enviando sinais em intervalos regulares."""
    while True:
        await simular_e_enviar_sinal(bot)
        intervalo = random.randint(600, 900)
        print(f"Aguardando {intervalo // 60} minutos para o próximo sinal.")
        await asyncio.sleep(intervalo)

async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # (O código da função gestao, que é bem longa, pode ser mantido aqui como na versão anterior)
    await update.message.reply_text("Aqui vai a mensagem de gestão completa...", parse_mode='Markdown')

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "Clique no botão abaixo para pegar seu bônus exclusivo! 🎁"
    botao = InlineKeyboardButton(text="Pegar Bônus Agora!", url=URL_CADASTRO)
    teclado = InlineKeyboardMarkup([[botao]])
    await update.message.reply_text(text=texto, reply_markup=teclado)

async def enviar_e_fixar_mensagem_inicial(bot: Bot):
    # (código da função mantido)
    pass

async def enviar_mensagem_recorrente(bot: Bot):
    # (código da função mantido)
    pass

async def main():
    """Configura e inicia todas as tarefas do bot."""
    print("Iniciando o bot profissional com marketing...")
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("gestao", gestao))
    application.add_handler(CommandHandler("bonus", bonus))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em execução.")

    asyncio.create_task(enviar_e_fixar_mensagem_inicial(application.bot))
    asyncio.create_task(ciclo_de_sinais(application.bot))
    asyncio.create_task(enviar_mensagem_recorrente(application.bot))

    print("Todas as tarefas automáticas foram agendadas.")

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
