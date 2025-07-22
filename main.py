import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# --- 1. CONFIGURAÇÃO INICIAL ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_BONUS = os.getenv("URL_BONUS", "https://seusite.com/bonus" )

# --- 2. BANCO DE FRASES VARIADAS ---
# Para que o bot não pareça um robô
frases_analise = [
    "🔎 Analisando os padrões do mercado Bac Bo agora...",
    "📈 Nossos algoritmos estão processando as últimas jogadas. Aguarde...",
    "🧠 Inteligência artificial em ação. Buscando a melhor oportunidade...",
    "📊 Cruzando dados e probabilidades. Sinal em breve...",
    "💻 Varredura completa do sistema. Preparando a próxima entrada..."
]

frases_sinal_header = [
    "💎 **SINAL DE ELITE CONFIRMADO** 💎",
    "🔥 **OPORTUNIDADE IDENTIFICADA** 🔥",
    "🎯 **ENTRADA DE ALTA PRECISÃO** 🎯",
    "✅ **LUZ VERDE! HORA DE OPERAR** ✅"
]

frases_sinal_footer = [
    "📲 Fique atento ao resultado!",
    "📊 Opere com gestão e disciplina.",
    "🍀 Boa sorte! Vamos buscar o green.",
    "🔔 Ative as notificações!"
]

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---
sinais_config = [
    {"aposta": "Banker (Azul) 🔵", "estrategia": "Tendência de Cores"},
    {"aposta": "Player (Vermelho) 🔴", "estrategia": "Quebra de Padrão"},
    {"aposta": "Banker (Azul) 🔵", "estrategia": "Análise de Pares/Ímpares"},
    {"aposta": "Player (Vermelho) 🔴", "estrategia": "Retorno à Média"}
]

# Probabilidades de acerto (ajuste se necessário)
CHANCE_WIN_ENTRADA_INICIAL = 0.70  # 70% de chance de ganhar na primeira entrada
CHANCE_WIN_GALE_1 = 0.80          # 80% no Gale 1
CHANCE_WIN_GALE_2 = 0.90          # 90% no Gale 2

# --- 4. FUNÇÕES DO BOT ---

async def simular_e_enviar_sinal(bot: Bot):
    """Ciclo completo: analisa, envia sinal e gerencia os resultados com gales."""
    config = random.choice(sinais_config)
    
    # a) Mensagem de "Analisando..."
    await bot.send_message(chat_id=CHAT_ID, text=random.choice(frases_analise))
    await asyncio.sleep(random.randint(5, 15)) # Pausa para simular análise

    # b) Envio do Sinal Principal
    mensagem_sinal = (
        f"{random.choice(frases_sinal_header)}\n\n"
        f"👇 Apostar em: **{config['aposta']}**\n"
        f"📈 Estratégia: *{config['estrategia']}*\n\n"
        f"1️⃣ **Entrada Inicial** (Meta: +4%)\n"
        f"2️⃣ **Gale 1** (Se necessário)\n"
        f"3️⃣ **Gale 2** (Se necessário)\n\n"
        f"{random.choice(frases_sinal_footer)}"
    )
    msg_sinal_enviada = await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, parse_mode='Markdown')
    print(f"Sinal enviado: {config['aposta']}")
    
    await asyncio.sleep(120) # Espera 2 minutos pelo resultado

    # c) Lógica de Resultados com Gales
    # Tentativa 1: Entrada Inicial
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        resultado_msg = (
            f"🏁 **RESULTADO FINAL** 🏁\n\n"
            f"✅ **WIN DE PRIMEIRA!** ✅\n\n"
            f"💰 **LUCRO: +4% DA BANCA**\n"
            f"🎯 Meta batida com sucesso! Parabéns!"
        )
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        print("Resultado: WIN na Entrada Inicial")
        return # Encerra o ciclo do sinal

    # Tentativa 2: Gale 1
    await bot.send_message(chat_id=CHAT_ID, text="🔁 **ATENÇÃO!** Vamos para o **GALE 1**. Cobrindo a entrada anterior.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)

    if random.random() < CHANCE_WIN_GALE_1:
        resultado_msg = (
            f"🏁 **RESULTADO FINAL** 🏁\n\n"
            f"✅ **WIN NO GALE 1!** ✅\n\n"
            f"💰 **LUCRO: +4% LÍQUIDO (META +8%)**\n"
            f"🎯 Perda recuperada e meta batida!"
        )
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        print("Resultado: WIN no Gale 1")
        return

    # Tentativa 3: Gale 2
    await bot.send_message(chat_id=CHAT_ID, text="🔁 **ÚLTIMA PROTEÇÃO!** Vamos para o **GALE 2**. Foco máximo!", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)

    if random.random() < CHANCE_WIN_GALE_2:
        resultado_msg = (
            f"🏁 **RESULTADO FINAL** 🏁\n\n"
            f"✅ **WIN NO GALE 2!** ✅\n\n"
            f"💰 **LUCRO: +4% LÍQUIDO (META +16%)**\n"
            f"🎯 Missão cumprida! Gestão impecável!"
        )
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        print("Resultado: WIN no Gale 2")
    else:
        # Loss final
        resultado_msg = (
            f"🏁 **RESULTADO FINAL** 🏁\n\n"
            f"❌ **RED!** ❌\n\n"
            f"⛔️ **STOP LOSS ATINGIDO.**\n"
            f"Respeite a gestão. Pausamos por hoje e voltamos amanhã mais fortes."
        )
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        print("Resultado: LOSS (Stop Loss)")

async def ciclo_de_sinais(bot: Bot):
    """Mantém o bot enviando sinais em intervalos regulares."""
    while True:
        await simular_e_enviar_sinal(bot)
        # Pausa de 10 a 15 minutos para o próximo ciclo de sinal
        intervalo = random.randint(600, 900)
        print(f"Aguardando {intervalo // 60} minutos para o próximo sinal.")
        await asyncio.sleep(intervalo)

async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia a mensagem com o protocolo de gestão."""
    texto_gestao = (
        "🚀 **PROTOCOLO DE GESTÃO AVANÇADA - BAC BO PROFISSIONAL**\n"
        "📍 *Método utilizado por traders de elite ao redor do mundo*\n\n"
        "🔒 Operamos com uma estratégia avançada de gestão de banca, desenvolvida para maximizar ganhos e controlar riscos com precisão cirúrgica.\n\n"
        "📊 **OBJETIVO DIÁRIO DE LUCRO:**\n"
        "✅ Ganho-alvo entre **4% e 16%** ao dia sobre a banca.\n"
        "⛔️ Limite de perda (Stop Loss): **2% a 8%** — gestão de risco real.\n\n"
        "⚙️ **ESTRUTURA DE ENTRADA COM GALES INTELIGENTES**\n\n"
        "1️⃣ **Entrada Inicial (Sem Gale)**\n"
        "   🎯 Meta: **+4% da banca.**\n"
        "   ➡️ Se bater o alvo, encerramos o dia com lucro garantido.\n\n"
        "2️⃣ **Gale 1 (caso de loss)**\n"
        "   🎯 Meta: **+8%**\n"
        "   ➡️ Recupera a perda anterior e ainda entrega +4% de lucro líquido.\n\n"
        "3️⃣ **Gale 2 (caso de novo loss)**\n"
        "   🎯 Meta: **+16%**\n"
        "   ➡️ Cobre 100% das perdas anteriores e fecha com +4% líquido garantido.\n\n"
        "🧠 **POR QUE ESSA GESTÃO FUNCIONA?**\n"
        "🔹 Baseada na teoria dos ciclos de acerto\n"
        "🔹 Desenvolvida com backtests de alta performance\n"
        "🔹 Segue o modelo dos melhores profissionais da Ásia e Europa\n"
        "🔹 Evita exposição excessiva, preservando o capital com disciplina\n\n"
        "📌 **REGRAS DE OURO DO CANAL**\n"
        "✅ Respeite a gestão.\n"
        "✅ Nunca ultrapasse o limite de 2 Gales.\n"
        "✅ Nunca opere fora da sua banca.\n"
        "✅ Parou no gain ou no stop, só volta no outro dia.\n\n"
        "💬 *“Quem domina a gestão, domina o jogo.”*"
    )
    await update.message.reply_text(texto_gestao, parse_mode='Markdown')

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia uma mensagem com um botão de bônus."""
    texto = "Clique no botão abaixo para pegar seu bônus exclusivo! 🎁"
    botao = InlineKeyboardButton(text="Pegar Bônus Agora!", url=URL_BONUS)
    teclado = InlineKeyboardMarkup([[botao]])
    await update.message.reply_text(text=texto, reply_markup=teclado)

async def main():
    """Configura e inicia o bot."""
    print("Iniciando o bot profissional...")
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("gestao", gestao))
    application.add_handler(CommandHandler("bonus", bonus))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em execução. Aguardando comandos e enviando sinais.")

    asyncio.create_task(ciclo_de_sinais(application.bot))

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
