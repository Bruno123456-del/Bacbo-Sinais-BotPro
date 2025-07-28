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

# --- 2. BANCO DE MÍDIA, MENSAGENS E CONTEÚDO DE VALOR ---

# >> GIFs
GIFS_ANALISE = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif",
    "https://media.giphy.com/media/l0HlBOJa9QvDpP4is/giphy.gif"
]
GIFS_RED = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif",
    "https://media.giphy.com/media/d2lcHJTG5Tscg/giphy.gif"
]
GIFS_WIN = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif",
    "https://media.giphy.com/media/3o7abG5kkvCfSQawj6/giphy.gif"
]

# >> MENSAGENS PARA COMANDOS
MENSAGEM_GESTAO = """
📊 **PROTOCOLO DE GESTÃO DE BANCA DE ELITE** 📊
A gestão de risco é o que separa amadores de profissionais. Siga este protocolo à risca:
1️⃣ **ENTRADA PRINCIPAL:** Use **1%** da sua banca.
2️⃣ **GALE 1 (Primeira Proteção ):** Use **2%** da sua banca.
3️⃣ **GALE 2 (Proteção Máxima):** Use **4%** da sua banca.
**REGRA DE OURO:** Nunca arrisque mais do que pode perder.
"""
MENSAGEM_PLATAFORMA = f"""
💎 **PLATAFORMA OFICIAL - 1WIN** 💎
Todos os nossos sinais são otimizados para a **1WIN**.
🔗 **Link de Cadastro Estratégico:** {URL_CADASTRO}
Clique, cadastre-se e ative seu bônus de boas-vindas!
"""
MENSAGEM_AJUDA = """
🆘 **CENTRAL DE AJUDA - COMANDOS DISPONÍVEIS** 🆘
/placar - 📊 Mostra o placar da sessão.
/gestao - 📈 Exibe nosso protocolo de gestão.
/plataforma - 💎 Envia o link de cadastro.
/ajuda - 🆘 Mostra esta mensagem de ajuda.
"""
DICAS_DO_DIA = [
    "🧠 **Mentalidade:** Não deixe uma perda abalar seu plano. A disciplina sempre vence a sorte.",
    "🧘 **Controle Emocional:** Opere com a mente clara. Se estiver frustrado, faça uma pausa.",
    "📈 **Juros Compostos:** Pequenos ganhos diários se transformam em uma fortuna.",
    "🚫 **Evite a Ganância:** Bateu a meta? Saia do mercado. A ganância é o maior inimigo."
]

# >> IMAGENS
IMG_WIN_ENTRADA = "imagens/win_entrada.png"
IMG_WIN_GALE1 = "imagens/win_gale1.png"
IMG_WIN_GALE2 = "imagens/win_gale2.png"
PROVAS_SOCIAIS = ["imagens/print_win_1.png", "imagens/print_win_2.png", "imagens/print_win_3.png"]

# >> MENSAGENS FIXAS E RECORRENTES
mensagem_fixada_texto = f"💎 *BEM-VINDO À SALA VIP - BAC BO DE ELITE* 💎\n\nPara garantir uma experiência de alta performance, é *essencial* que você opere na mesma plataforma que utilizamos: **1WIN**.\n\n👉 **Cadastre-se e ative seu bônus:** {URL_CADASTRO}\n\n*Invista com inteligência. Jogue junto, ganhe junto.*"
reforco_pos_win = [f"✅ Sincronia perfeita! É por isso que operamos na **1WIN**. Cadastre-se e comprove 👉 {URL_CADASTRO}"]
mensagem_automatica_recorrente = f"🔔 *LEMBRETE DE PERFORMANCE* 🔔\nNossa estratégia é 100% compatível com a **1WIN**. Garanta sua vaga e bônus: {URL_CADASTRO}"

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---
sinais_config = [
    {"tipo": "padrao", "aposta": "Banker (Azul) 🔵", "estrategia": "Tendência de Cores"},
    {"tipo": "padrao", "aposta": "Player (Vermelho) 🔴", "estrategia": "Quebra de Padrão"},
    {"tipo": "cobertura_empate", "aposta_principal": "Banker (Azul) 🔵", "aposta_secundaria": "Tie (Empate) 🟢", "estrategia": "Cobertura de Empate"}
]
CHANCE_WIN_ENTRADA_INICIAL = 0.70
CHANCE_WIN_GALE_1 = 0.80
CHANCE_WIN_GALE_2 = 0.90
placar = {"greens": 0, "reds": 0}

# --- 4. FUNÇÕES DO BOT ---

async def enviar_print_fake(bot: Bot, tipo_win: str):
    mapa_resultado_imagem = {"win_entrada": IMG_WIN_ENTRADA, "win_gale1": IMG_WIN_GALE1, "win_gale2": IMG_WIN_GALE2}
    imagem_path = mapa_resultado_imagem.get(tipo_win)
    if not imagem_path: return
    try:
        legenda = random.choice(["📸 Comprovado! Resultado da nossa última entrada!", "💰 Prova social: WIN confirmado agora mesmo."])
        await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem_path, 'rb'), caption=legenda)
        print(f"✅ Print fake de '{tipo_win}' enviado.")
    except Exception as e:
        print(f"Erro ao enviar print fake: {e}")

async def ciclo_de_sinais(bot: Bot):
    sinais_enviados = 0
    while True:
        await simular_e_enviar_sinal(bot)
        sinais_enviados += 1
        if sinais_enviados % 3 == 0:
            await asyncio.sleep(15)
            placar_texto = f"📊 **PLACAR ATUALIZADO** 📊\n\n✅ **Greens:** {placar['greens']}\n❌ **Reds:** {placar['reds']}"
            await bot.send_message(chat_id=CHAT_ID, text=placar_texto, parse_mode='Markdown')
            await asyncio.sleep(10)
            try:
                imagem_prova = random.choice(PROVAS_SOCIAIS)
                texto_prova = random.choice(["🔥 Nossos membros não param de lucrar!", "🚀 Mais um resultado positivo!"])
                await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem_prova, 'rb'), caption=texto_prova)
            except Exception as e:
                print(f"Erro ao enviar prova social: {e}")
        intervalo_fixo = 15 * 60
        print(f"Aguardando {intervalo_fixo // 60} minutos para o próximo sinal.")
        await asyncio.sleep(intervalo_fixo)

async def simular_e_enviar_sinal(bot: Bot):
    global placar
    config = random.choice(sinais_config)
    msg_analise = await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_ANALISE), caption="📡 **Analisando...**")
    await asyncio.sleep(random.randint(10, 20))
    botao_plataforma = InlineKeyboardButton(text="💎 JOGAR BAC BO AGORA 💎", url=URL_CADASTRO)
    teclado_sinal = InlineKeyboardMarkup([[botao_plataforma]])
    if config["tipo"] == "cobertura_empate":
        mensagem_sinal = (f"**🔥 OPORTUNIDADE COM COBERTURA 🔥**\n\n▪️ **Estratégia:** `{config['estrategia']}`\n\n**PLANO DE AÇÃO:**\n1️⃣ **Principal (70%):** `{config['aposta_principal']}`\n2️⃣ **Cobertura (30%):** `{config['aposta_secundaria']}`\n\n🚨 *Siga a gestão!*")
    else:
        mensagem_sinal = (f"**🔥 OPORTUNIDADE DE ENTRADA 🔥**\n\n▪️ **Direção:** `{config['aposta']}`\n▪️ **Estratégia:** `{config['estrategia']}`\n\n**PLANO DE AÇÃO:**\n1️⃣ **Entrada Principal**\n2️⃣ **Gale 1** (Se necessário)\n3️⃣ **Gale 2** (Se necessário)\n\n🚨 *Siga a gestão.*")
    await msg_analise.delete()
    msg_sinal_enviada = await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, parse_mode='Markdown', reply_markup=teclado_sinal)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        placar["greens"] += 1; await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN)); await asyncio.sleep(2); await enviar_print_fake(bot, "win_entrada"); await asyncio.sleep(10); await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção: GALE 1**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        placar["greens"] += 1; await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN)); await asyncio.sleep(2); await enviar_print_fake(bot, "win_gale1"); await asyncio.sleep(10); await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção: GALE 2**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        placar["greens"] += 1; await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN)); await asyncio.sleep(2); await enviar_print_fake(bot, "win_gale2"); await asyncio.sleep(10); await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
    else:
        placar["reds"] += 1; await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_RED), caption="❌ **STOP LOSS**")

# --- 5. FUNÇÕES PARA COMANDOS E TAREFAS AUTOMÁTICAS (CORRIGIDO) ---

async def placar_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    placar_texto = f"📊 **PLACAR ATUAL** 📊\n\n✅ **Greens:** {placar['greens']}\n❌ **Reds:** {placar['reds']}"
    await update.message.reply_text(placar_texto, parse_mode='Markdown')

async def gestao_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAGEM_GESTAO, parse_mode='Markdown')

async def plataforma_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAGEM_PLATAFORMA, parse_mode='Markdown', disable_web_page_preview=False)

async def ajuda_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAGEM_AJUDA, parse_mode='Markdown')

async def enviar_dica_do_dia(bot: Bot):
    while True:
        await asyncio.sleep(4 * 3600)
        dica = random.choice(DICAS_DO_DIA)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=f"💡 **DICA DE VALOR** 💡\n\n{dica}", parse_mode='Markdown')
            print("💡 Dica do dia enviada.")
        except Exception as e:
            print(f"Erro ao enviar dica do dia: {e}")

async def enviar_e_fixar_mensagem_inicial(bot: Bot):
    try:
        msg = await bot.send_message(chat_id=CHAT_ID, text=mensagem_fixada_texto, parse_mode='Markdown', disable_web_page_preview=True)
        await bot.pin_chat_message(chat_id=CHAT_ID, message_id=msg.message_id)
    except Exception as e: print(f"Erro ao fixar msg: {e}")

async def enviar_mensagem_recorrente(bot: Bot):
    while True:
        await asyncio.sleep(21600)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem_automatica_recorrente, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e: print(f"Erro na msg recorrente: {e}")

# --- 6. FUNÇÃO PRINCIPAL QUE INICIA TUDO ---

async def main():
    print("Iniciando Bot BAC BO - Versão COMUNIDADE VIP...")
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("placar", placar_comando))
    application.add_handler(CommandHandler("gestao", gestao_comando))
    application.add_handler(CommandHandler("plataforma", plataforma_comando))
    application.add_handler(CommandHandler("ajuda", ajuda_comando))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em plena operação.")

    bot = application.bot
    
    asyncio.create_task(enviar_e_fixar_mensagem_inicial(bot))
    asyncio.create_task(ciclo_de_sinais(bot))
    asyncio.create_task(enviar_mensagem_recorrente(bot))
    asyncio.create_task(enviar_dica_do_dia(bot))

    print("Todas as tarefas automáticas foram agendadas.")
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
