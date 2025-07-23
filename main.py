# -*- coding: utf-8 -*-

import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest
from telegram.constants import ChatAction

# --- 1. CONFIGURAÇÃO INICIAL ---
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lembre-se de configurar estas variáveis no seu arquivo .env ou no painel da Render
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = "https://lkwn.cc/f1c1c45a" # Seu link principal de afiliado

# --- 2. BANCO DE MÍDIA E MENSAGENS VIP ---

# >> BIBLIOTECA DE GIFS (Adicione ou troque os links para mais variedade )
GIFS_ANALISE = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2d5Y2l2aTdkc252YWtqZzN3Z3JkYm5wYjZ1Z3ZqZ3ZqZ3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1gO2bYy20VjBCs1H6U/giphy.gif"
]
GIFS_WIN = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzVnb2dpcTYzb3ZkZ3k4aGg2M3NqZzZzZzRjZzZzZzRjZzZzZzRjZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abIileRivlGr8Nq/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaW9oZDN1dTY2a29uY2tqZzZzZzZzZzZzZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/a0h7sAqhlCQoM/giphy.gif"
]
GIFS_RED = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbTZyZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/q8p2sC2q42N2M/giphy.gif"
]
GIF_PROCESSANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7bu3XUjSjbtS0g12/giphy.gif"

# >> MENSAGENS DE MARKETING E GESTÃO
mensagem_fixada_texto = f"""
💎 *BEM-VINDO À SALA VIP - BAC BO DE ELITE* 💎

Prezado(a ) investidor(a),

Para garantir uma experiência de alta performance e resultados sincronizados com nossos analistas, é *essencial* que você opere na mesma plataforma que utilizamos.

Nossos algoritmos são calibrados para a **1WIN**.

1️⃣ **PASSO 1: CADASTRO ESTRATÉGICO**
   Clique no link abaixo para criar sua conta e alinhar-se à nossa frequência operacional.
   👉 {URL_CADASTRO}

2️⃣ **PASSO 2: ATIVAÇÃO DE BÔNUS**
   Realize um depósito inicial para ativar os bônus de boas-vindas e estar pronto para as operações.

⚠️ *Operar em outra plataforma resultará em divergência de resultados.*

*Invista com inteligência. Jogue junto, ganhe junto!*
"""

reforco_pos_win = [
    f"✅ Sincronia perfeita! É por isso que operamos na **1WIN**. Se você ainda não está lá, a hora é agora 👉 {URL_CADASTRO}",
    f"🚀 Mais um resultado positivo! Nossos sinais são otimizados para a plataforma certa. Cadastre-se e comprove 👉 {URL_CADASTRO}"
]

mensagem_automatica_recorrente = f"""
🔔 *LEMBRETE DE PERFORMANCE* 🔔

Resultados consistentes exigem as ferramentas certas. Nossa estratégia é 100% compatível com a **1WIN**.

Não perca mais tempo com plataformas não sincronizadas.

🔗 **Garanta sua vaga e bônus:** {URL_CADASTRO}

*A sorte favorece os bem preparados.*
"""

texto_gestao = """
🚀 **PROTOCOLO DE GESTÃO AVANÇADA - BAC BO PROFISSIONAL**
📍 *Método utilizado por traders de elite ao redor do mundo*

(Aqui você pode colar o texto completo da sua gestão)
"""

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---
sinais_config = [{"aposta": "Banker (Azul) 🔵", "estrategia": "Tendência de Cores"}, {"aposta": "Player (Vermelho) 🔴", "estrategia": "Quebra de Padrão"}]
CHANCE_WIN_ENTRADA_INICIAL = 0.70
CHANCE_WIN_GALE_1 = 0.80
CHANCE_WIN_GALE_2 = 0.90

# --- 4. FUNÇÕES PRINCIPAIS DO BOT ---

async def simular_e_enviar_sinal(bot: Bot):
    """Ciclo completo de um sinal, com a experiência VIP definitiva."""
    config = random.choice(sinais_config)
    
    # ETAPA 1: ANÁLISE
    await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.UPLOAD_PHOTO)
    msg_analise = await bot.send_animation(
        chat_id=CHAT_ID,
        animation=random.choice(GIFS_ANALISE),
        caption="""
        📡 **Conectando aos nossos servidores...**
        
        Nossos analistas e I.A. estão em busca de uma entrada de alta probabilidade.
        
        *Aguarde, a oportunidade perfeita está sendo lapidada.*
        """
    )
    await asyncio.sleep(random.randint(10, 20))
    
    # ETAPA 2: SINAL
    botao_bonus = InlineKeyboardButton(text="🎁 Pegue seu bônus agora mesmo 🎁", url=URL_CADASTRO)
    teclado_sinal = InlineKeyboardMarkup([[botao_bonus]])
    
    mensagem_sinal = (
        f"**🔥 OPORTUNIDADE DE ENTRADA DETECTADA 🔥**\n\n"
        f"👇 Apostar em: **{config['aposta']}**\n"
        f"📈 Estratégia: *{config['estrategia']}*\n\n"
        f"**PLANO DE AÇÃO:**\n"
        f"1️⃣ **Entrada Inicial** (Meta: +4%)\n"
        f"2️⃣ **Gale 1** (Se necessário)\n"
        f"3️⃣ **Gale 2** (Se necessário)\n\n"
        f"🚨 *Opere com precisão. Siga a gestão.*"
    )
    
    await msg_analise.delete()
    await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.TYPING)
    await asyncio.sleep(2)
    msg_sinal_enviada = await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, parse_mode='Markdown', reply_markup=teclado_sinal)
    
    # ETAPA 3: PROCESSANDO RESULTADO
    await asyncio.sleep(110)
    await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.TYPING)
    msg_processando = await bot.send_message(chat_id=CHAT_ID, text="Processando resultado...", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(10)
    await msg_processando.delete()

    # ETAPA 4: RESULTADO
    # Tentativa 1: WIN
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN), caption="✅ **WIN NA ENTRADA PRINCIPAL!**\n\n💰 **LUCRO ALCANÇADO: +4%**\n\n*A precisão é a nossa marca. Parabéns a todos!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 2: GALE 1
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando primeira proteção. Entrando no **GALE 1**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN), caption="✅ **WIN NO GALE 1!**\n\n💰 **LUCRO TOTAL: +8%**\n\n*Gestão de risco executada com perfeição. Meta batida!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 3: GALE 2
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando proteção máxima. Entrando no **GALE 2**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN), caption="✅ **WIN NO GALE 2!**\n\n💰 **LUCRO TOTAL: +16%**\n\n*A persistência e a estratégia nos levaram à vitória!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_RED), caption="❌ **STOP LOSS**\n\n*O mercado não se moveu a nosso favor. Encerramos esta operação para proteger nosso capital. Disciplina é a chave do sucesso a longo prazo. Voltamos em breve.*")

# --- 5. FUNÇÕES DE CICLO E COMANDOS ---

async def ciclo_de_sinais(bot: Bot):
    """Mantém o bot enviando sinais em intervalos regulares."""
    while True:
        await simular_e_enviar_sinal(bot)
        intervalo = random.randint(900, 1800)
        print(f"Aguardando {intervalo // 60} minutos para o próximo ciclo de sinal.")
        await asyncio.sleep(intervalo)

async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia a mensagem com o protocolo de gestão."""
    await update.message.reply_text(texto_gestao, parse_mode='Markdown')

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia uma mensagem com um botão de bônus."""
    texto = "Clique no botão abaixo para pegar seu bônus exclusivo e se cadastrar na plataforma certa! 🎁"
    botao = InlineKeyboardButton(text="Pegar Bônus Agora!", url=URL_CADASTRO)
    teclado = InlineKeyboardMarkup([[botao]])
    await update.message.reply_text(text=texto, reply_markup=teclado)

async def enviar_e_fixar_mensagem_inicial(bot: Bot):
    """Envia a mensagem de boas-vindas e a fixa no canal."""
    try:
        msg = await bot.send_message(chat_id=CHAT_ID, text=mensagem_fixada_texto, parse_mode='Markdown', disable_web_page_preview=True)
        await bot.pin_chat_message(chat_id=CHAT_ID, message_id=msg.message_id)
        print("Mensagem inicial enviada e fixada no canal.")
    except Exception as e:
        print(f"Erro ao enviar/fixar mensagem inicial: {e}")

async def enviar_mensagem_recorrente(bot: Bot):
    """Envia a mensagem de marketing a cada 6 horas."""
    while True:
        await asyncio.sleep(21600) # 6 horas
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem_automatica_recorrente, parse_mode='Markdown', disable_web_page_preview=True)
            print("Mensagem automática recorrente enviada.")
        except Exception as e:
            print(f"Erro ao enviar mensagem recorrente: {e}")

# --- 6. FUNÇÃO PRINCIPAL (MAIN) ---

async def main():
    """Configura e inicia todas as tarefas do bot."""
    print("Iniciando Bot BAC BO - Versão Definitiva...")
    
    # Nota sobre o erro 'Conflict': Este erro acontece se mais de uma instância do bot
    # rodar com o mesmo TOKEN. Garanta que apenas UM serviço esteja ativo na Render.
    
    application = Application.builder().token(TOKEN).build()
    
    # Adiciona os comandos que os usuários podem chamar
    application.add_handler(CommandHandler("gestao", gestao))
    application.add_handler(CommandHandler("bonus", bonus))
    
    # Inicializa o bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em plena operação. Sinais e interações ativados.")

    # Inicia as tarefas automáticas que rodam em background
    bot = application.bot
    asyncio.create_task(enviar_e_fixar_mensagem_inicial(bot))
    asyncio.create_task(ciclo_de_sinais(bot))
    asyncio.create_task(enviar_mensagem_recorrente(bot))

    print("Todas as tarefas automáticas foram agendadas com sucesso.")
    
    # Mantém o script principal rodando indefinidamente
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado pelo usuário.")
    except Exception as e:
        print(f"Ocorreu um erro crítico: {e}")

