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
URL_CADASTRO = "https://lkwn.cc/f1c1c45a" # URL principal para cadastro
URL_BONUS = os.getenv("URL_BONUS", URL_CADASTRO ) # URL para o comando /bonus

# --- 2. BANCO DE MENSAGENS ---

# Mensagem para ser fixada no início
mensagem_fixada_texto = f"""
🎰 *Bem-vindo aos SINAIS 1WIN - BAC BO VIP*

📢 Estamos usando a *melhor plataforma do momento*, com os *maiores bônus* e um *algoritmo 100% alinhado com nossa estratégia*.

✅ Para garantir que você tenha os mesmos resultados que a gente:

1️⃣ *Cadastre-se pela plataforma correta:*
👉 {URL_CADASTRO}

2️⃣ *Deposite para liberar os bônus*

🔐 Usar outro site pode gerar sinais diferentes!

🎯 *Jogue junto, ganhe junto!*
"""

# Mensagens de reforço para depois de um WIN
reforco_pos_win = [
    f"""
🔔 Ainda não está usando a mesma plataforma que a gente?

🎰 Cadastre-se aqui 👉 {URL_CADASTRO}
🎁 Ganhe bônus + sinais sincronizados com nosso algoritmo!

💡 Nosso bot é otimizado para a 1win – outras plataformas NÃO batem!
""",
    f"""
🎯 Green confirmado!

🔁 Use sempre a mesma plataforma para sincronizar com a nossa estratégia.
👉 {URL_CADASTRO}
"""
]

# Mensagem automática a cada 6 horas
mensagem_automatica_recorrente = f"""
⏱️ *Dica do dia:*

Se você ainda não se cadastrou na 1win pelo nosso link, aproveite AGORA!

🎰 Plataforma 100% compatível com nossos sinais
🎁 Bônus de boas-vindas pra novos jogadores
📊 Resultados melhores com nosso algoritmo exclusivo

🎯 Link para cadastro: {URL_CADASTRO}
"""

# Frases variadas para os sinais (mantidas da versão anterior)
frases_analise = ["🔎 Analisando os padrões...", "📈 Processando as últimas jogadas...", "🧠 I.A. em ação, buscando a melhor oportunidade..."]
frases_sinal_header = ["💎 **SINAL DE ELITE CONFIRMADO** 💎", "🔥 **OPORTUNIDADE IDENTIFICADA** 🔥", "🎯 **ENTRADA DE ALTA PRECISÃO** 🎯"]
frases_sinal_footer = ["📲 Fique atento ao resultado!", "📊 Opere com gestão e disciplina.", "🍀 Boa sorte!"]

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---
sinais_config = [{"aposta": "Banker (Azul) 🔵", "estrategia": "Tendência"}, {"aposta": "Player (Vermelho) 🔴", "estrategia": "Quebra de Padrão"}]
CHANCE_WIN_ENTRADA_INICIAL = 0.70
CHANCE_WIN_GALE_1 = 0.80
CHANCE_WIN_GALE_2 = 0.90

# --- 4. FUNÇÕES DO BOT ---

async def enviar_e_fixar_mensagem_inicial(bot: Bot):
    """Envia a mensagem de boas-vindas e a fixa no canal."""
    try:
        msg = await bot.send_message(chat_id=CHAT_ID, text=mensagem_fixada_texto, parse_mode='Markdown', disable_web_page_preview=True)
        await bot.pin_chat_message(chat_id=CHAT_ID, message_id=msg.message_id)
        print("Mensagem inicial enviada e fixada no canal.")
    except BadRequest as e:
        if "message to pin not found" in e.message:
            print("A mensagem já foi enviada e talvez deletada. Não foi possível fixar.")
        else:
            print(f"Erro ao enviar/fixar mensagem inicial: {e}")
    except Exception as e:
        print(f"Erro inesperado ao enviar/fixar mensagem: {e}")

async def enviar_mensagem_recorrente(bot: Bot):
    """Envia a mensagem automática a cada 6 horas."""
    while True:
        await asyncio.sleep(21600) # 6 horas = 21600 segundos
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem_automatica_recorrente, parse_mode='Markdown', disable_web_page_preview=True)
            print("Mensagem automática recorrente enviada.")
        except Exception as e:
            print(f"Erro ao enviar mensagem recorrente: {e}")

async def simular_e_enviar_sinal(bot: Bot):
    """Ciclo completo: analisa, envia sinal e gerencia os resultados com gales."""
    config = random.choice(sinais_config)
    await bot.send_message(chat_id=CHAT_ID, text=random.choice(frases_analise))
    await asyncio.sleep(random.randint(5, 15))

    mensagem_sinal = (f"{random.choice(frases_sinal_header)}\n\n"
                      f"👇 Apostar em: **{config['aposta']}**\n"
                      f"📈 Estratégia: *{config['estrategia']}*\n\n"
                      f"1️⃣ **Entrada Inicial** (Meta: +4%)\n"
                      f"2️⃣ **Gale 1** (Se necessário)\n"
                      f"3️⃣ **Gale 2** (Se necessário)\n\n"
                      f"{random.choice(frases_sinal_footer)}")
    msg_sinal_enviada = await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, parse_mode='Markdown')
    print(f"Sinal enviado: {config['aposta']}")
    await asyncio.sleep(120)

    # Lógica de Resultados com Gales
    # Tentativa 1: WIN
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        resultado_msg = "✅ **WIN DE PRIMEIRA!** ✅\n\n💰 **LUCRO: +4% DA BANCA**"
        await bot.send_message(chat_id=CHAT_ID, text=resultado_msg, reply_to_message_id=msg_sinal_enviada.message_id, parse_mode='Markdown')
        await asyncio.sleep(5) # Pequena pausa antes do reforço
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

    # Tentativa 3: GALE 2
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

async def ciclo_de_sinais(bot: Bot):
    """Mantém o bot enviando sinais em intervalos regulares."""
    while True:
        await simular_e_enviar_sinal(bot)
        intervalo = random.randint(600, 900)
        print(f"Aguardando {intervalo // 60} minutos para o próximo sinal.")
        await asyncio.sleep(intervalo)

# --- Comandos (/gestao, /bonus) ---
async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # (O código da função gestao, que é bem longa, pode ser mantido aqui como na versão anterior)
    await update.message.reply_text("Aqui vai a mensagem de gestão completa...", parse_mode='Markdown')

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "Clique no botão abaixo para pegar seu bônus exclusivo! 🎁"
    botao = InlineKeyboardButton(text="Pegar Bônus Agora!", url=URL_BONUS)
    teclado = InlineKeyboardMarkup([[botao]])
    await update.message.reply_text(text=texto, reply_markup=teclado)

# --- 5. FUNÇÃO PRINCIPAL ---
async def main():
    """Configura e inicia todas as tarefas do bot."""
    print("Iniciando o bot profissional com marketing...")
    application = Application.builder().token(TOKEN).build()
    
    # Adiciona os comandos que os usuários podem chamar
    application.add_handler(CommandHandler("gestao", gestao))
    application.add_handler(CommandHandler("bonus", bonus))
    
    # Inicializa o bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em execução.")

    # --- Inicia as tarefas automáticas ---
    # 1. Envia e fixa a mensagem de boas-vindas (só uma vez)
    asyncio.create_task(enviar_e_fixar_mensagem_inicial(application.bot))
    
    # 2. Inicia o ciclo de envio de sinais
    asyncio.create_task(ciclo_de_sinais(application.bot))
    
    # 3. Inicia o ciclo de mensagens automáticas de marketing
    asyncio.create_task(enviar_mensagem_recorrente(application.bot))

    print("Todas as tarefas automáticas foram agendadas.")

    # Mantém o script principal rodando
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
