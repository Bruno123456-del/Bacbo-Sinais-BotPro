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
URL_CADASTRO = "https://lkwn.cc/f1c1c45a"

# --- 2. BANCO DE MÍDIA E MENSAGENS DE LUXO ---

# >> Galerias de GIFs para máxima variedade
GIFS_ANALISE = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2dnbmZrd2c1aGg3Z3Y2dDE4c3E4eGg2d3JzY2w0aHFuY2dqd21qZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dSpH2nS0i2ssg/giphy.gif"
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

# >> Mensagens (mantidas da versão de luxo )
# ... (todas as mensagens de fixada, reforço, etc., continuam aqui) ...

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---
# ... (configurações mantidas) ...

# --- 4. FUNÇÕES DO BOT ---

async def simular_e_enviar_sinal(bot: Bot):
    """Ciclo completo de um sinal, com estética de luxo e o novo botão."""
    config = random.choice(sinais_config)
    
    # ETAPA 1: ANÁLISE (com GIF aleatório)
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
    
    # ETAPA 2: SINAL (com o novo botão)
    # --- MUDANÇA PRINCIPAL AQUI ---
    botao_bonus = InlineKeyboardButton(
        text="🎁 Pegue seu bônus agora mesmo 🎁", # Texto alterado conforme solicitado
        url=URL_CADASTRO
    )
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
    msg_sinal_enviada = await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, parse_mode='Markdown', reply_markup=teclado_sinal)
    
    # ETAPA 3: PROCESSANDO RESULTADO (aumenta o suspense)
    await asyncio.sleep(110) # Espera quase 2 minutos
    msg_processando = await bot.send_animation(chat_id=CHAT_ID, animation=GIF_PROCESSANDO, reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(10) # Espera final
    await msg_processando.delete()

    # ETAPA 4: RESULTADO (com GIF aleatório e textos de lucro corretos)
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

# --- O resto do código (ciclo_de_sinais, gestao, bonus, main, etc.) permanece o mesmo ---
# ...

if __name__ == '__main__':
    try:
        # (A função main e as outras funções auxiliares estão aqui, sem alterações)
        pass # Placeholder para o resto do código que não mudou
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
