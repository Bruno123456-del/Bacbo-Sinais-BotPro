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

# >> GIFs
GIF_ANALISE = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
# >> NOVO: GIF DE COMEMORAÇÃO DE VITÓRIA
GIF_WIN = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"
# >> NOVAS MENSAGENS PARA COMANDOS E CONTEÚDO DE VALOR
MENSAGEM_GESTAO = """
📊 **PROTOCOLO DE GESTÃO DE BANCA DE ELITE** 📊

A gestão de risco é o que separa amadores de profissionais. Siga este protocolo à risca:

1️⃣ **ENTRADA PRINCIPAL:** Use **1%** da sua banca.
    - *Exemplo: Banca de R$200,00 -> Entrada de R$2,00.*

2️⃣ **GALE 1 (Primeira Proteção):** Use **2%** da sua banca.
    - *Exemplo: Banca de R$200,00 -> Entrada de R$4,00.*

3️⃣ **GALE 2 (Proteção Máxima):** Use **4%** da sua banca.
    - *Exemplo: Banca de R$200,00 -> Entrada de R$8,00.*

**REGRA DE OURO:** Nunca arrisque mais do que pode perder. A consistência nos juros compostos é o caminho para a fortuna.
"""

MENSAGEM_PLATAFORMA = f"""
💎 **PLATAFORMA OFICIAL - 1WIN** 💎

Todos os nossos sinais são otimizados para a **1WIN**. Operar em outra plataforma pode gerar resultados diferentes.

🔗 **Link de Cadastro Estratégico:**
{URL_CADASTRO}

Clique, cadastre-se e ative seu bônus de boas-vindas para operar em sincronia com nossos analistas!
"""

MENSAGEM_AJUDA = """
🆘 **CENTRAL DE AJUDA - COMANDOS DISPONÍVEIS** 🆘

Use os seguintes comandos para interagir com o bot:

/placar - 📊 Mostra o placar de vitórias e derrotas da sessão atual.
/gestao - 📈 Exibe nosso protocolo oficial de gestão de banca.
/plataforma - 💎 Envia o link de cadastro da nossa plataforma parceira.
/ajuda - 🆘 Mostra esta mensagem de ajuda.
"""

DICAS_DO_DIA = [
    "🧠 **Mentalidade:** Não deixe uma perda abalar seu plano. A disciplina no longo prazo sempre vence a sorte de um dia.",
    "🧘 **Controle Emocional:** Opere com a mente clara. Se estiver ansioso ou frustrado, faça uma pausa. O mercado estará aí amanhã.",
    "📈 **Juros Compostos:** Pequenos ganhos diários se transformam em uma fortuna. Pense no acumulado da semana, não apenas em uma única aposta.",
    "🚫 **Evite a Ganância:** Bateu a meta do dia? Saia do mercado. A ganância é o maior inimigo do apostador.",
    "📖 **Estude Sempre:** Entenda o porquê das suas entradas. Quanto mais você conhece o jogo, mais confia na estratégia."
]

# >> IMAGENS DE VITÓRIA (Mantidas )
IMG_WIN_ENTRADA = "imagens/win_entrada.png"
IMG_WIN_GALE1 = "imagens/win_gale1.png"
IMG_WIN_GALE2 = "imagens/win_gale2.png"

# >> IMAGENS PARA PROVA SOCIAL (Mantidas)
PROVAS_SOCIAIS = ["imagens/print_win_1.png", "imagens/print_win_2.png", "imagens/print_win_3.png"]

# >> Mensagens (sem alteração)
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

*Invista com inteligência. Jogue junto, ganhe junto.*
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

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---
sinais_config = [{"aposta": "Banker (Azul) 🔵", "estrategia": "Tendência de Cores"}, {"aposta": "Player (Vermelho) 🔴", "estrategia": "Quebra de Padrão"}]
CHANCE_WIN_ENTRADA_INICIAL = 0.70
CHANCE_WIN_GALE_1 = 0.80
CHANCE_WIN_GALE_2 = 0.90

# >> PLACAR DE RESULTADOS (Mantido)
placar = {"greens": 0, "reds": 0}

# --- 4. FUNÇÕES DO BOT ---

async def simular_e_enviar_sinal(bot: Bot):
    """Ciclo completo de um sinal, com ordem corrigida e GIFs de comemoração."""
    global placar
    config = random.choice(sinais_config)
    
    # ETAPA 1: ANÁLISE
    msg_analise = await bot.send_animation(
        chat_id=CHAT_ID,
        animation=GIF_ANALISE,
        caption="""
        📡 **Conectando aos nossos servidores...**
        
        Nossos analistas e I.A. estão em busca de uma entrada de alta probabilidade.
        
        *Aguarde, a oportunidade perfeita está sendo lapidada.*
        """
    )
    await asyncio.sleep(random.randint(10, 20))
    
    # ETAPA 2: SINAL
    botao_plataforma = InlineKeyboardButton(text="💎 ENTRAR NA PLATAFORMA 💎", url=URL_CADASTRO)
    teclado_sinal = InlineKeyboardMarkup([[botao_plataforma]])
    
    mensagem_sinal = (
        f"**🔥 OPORTUNIDADE DE ENTRADA DETECTADA 🔥**\n\n"
        f"▪️ **Ativo:** `BAC BO`\n"
        f"▪️ **Direção:** `{config['aposta']}`\n"
        f"▪️ **Estratégia:** `{config['estrategia']}`\n\n"
        f"**PLANO DE AÇÃO:**\n"
        f"1️⃣ **Entrada Principal:** `Meta de +4%`\n"
        f"2️⃣ **Proteção 1 (Gale):** `Se necessário`\n"
        f"3️⃣ **Proteção 2 (Gale):** `Se necessário`\n\n"
        f"🚨 *Opere com precisão. Siga a gestão.*"
    )
    
    await msg_analise.delete()
    msg_sinal_enviada = await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, parse_mode='Markdown', reply_markup=teclado_sinal)
    
    await asyncio.sleep(120)

    # ETAPA 3: RESULTADO (COM ORDEM CORRIGIDA E GIFS ADICIONADOS)
    # Tentativa 1: WIN
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN) # GIF de comemoração
        await asyncio.sleep(2) # Pausa para garantir a ordem
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_ENTRADA, 'rb'), caption="✅ **WIN NA ENTRADA PRINCIPAL!**\n\n💰 **LUCRO ALCANÇADO: +4%**\n\n*A precisão é a nossa marca. Parabéns a todos!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 2: GALE 1
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando primeira proteção. Entrando no **GALE 1**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN) # GIF de comemoração
        await asyncio.sleep(2) # Pausa para garantir a ordem
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE1, 'rb'), caption="✅ **WIN NO GALE 1!**\n\n💰 **LUCRO TOTAL: +8%**\n\n*Gestão de risco executada com perfeição. Meta batida!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 3: GALE 2
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando proteção máxima. Entrando no **GALE 2**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN) # GIF de comemoração
        await asyncio.sleep(2) # Pausa para garantir a ordem
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE2, 'rb'), caption="✅ **WIN NO GALE 2!**\n\n💰 **LUCRO TOTAL: +16%**\n\n*A persistência e a estratégia nos levaram à vitória!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
    else:
        placar["reds"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_RED, caption="❌ **STOP LOSS**\n\n*O mercado não se moveu a nosso favor. Encerramos esta operação para proteger nosso capital. Disciplina é a chave do sucesso a longo prazo. Voltamos em breve.*")

# --- Funções de Ciclo e Comandos (sem alterações) ---

async def ciclo_de_sinais(bot: Bot):
    """Ciclo de sinais com placar e prova social."""
    sinais_enviados = 0
    while True:
        await simular_e_enviar_sinal(bot)
        sinais_enviados += 1
        
        if sinais_enviados % 3 == 0:
            await asyncio.sleep(15)
            
            placar_texto = f"📊 **PLACAR ATUALIZADO** 📊\n\n✅ **Greens:** {placar['greens']}\n❌ **Reds:** {placar['reds']}\n\n*Consistência é o nosso jogo.*"
            await bot.send_message(chat_id=CHAT_ID, text=placar_texto, parse_mode='Markdown')
            await asyncio.sleep(10)

            try:
                imagem_prova = random.choice(PROVAS_SOCIAIS)
                texto_prova = random.choice([
                    "🔥 Nossos membros não param de lucrar! Veja esse resultado!",
                    "🚀 É por isso que nossa comunidade cresce a cada dia. Parabéns pelo resultado!",
                    "💰 Mais um print que fala por si só. Venha fazer parte do time!"
                ])
                await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem_prova, 'rb'), caption=texto_prova)
            except FileNotFoundError:
                print(f"Aviso: Arquivo de prova social não encontrado. Verifique a pasta 'imagens'.")
            except Exception as e:
                print(f"Erro ao enviar prova social: {e}")

        intervalo_fixo = 15 * 60
        print(f"Aguardando 15 minutos para o próximo ciclo de sinal.")
        await asyncio.sleep(intervalo_fixo)

async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Protocolo de Gestão Avançada...", parse_mode='Markdown')

# --- 5. FUNÇÃO PRINCIPAL (sem alterações) ---
# --- NOVAS FUNÇÕES PARA OS COMANDOS ---

async def placar_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia o placar atual quando o comando /placar é usado."""
    placar_texto = f"📊 **PLACAR ATUAL** 📊\n\n✅ **Greens:** {placar['greens']}\n❌ **Reds:** {placar['reds']}\n\n*Sessão em andamento...*"
    await update.message.reply_text(placar_texto, parse_mode='Markdown')

async def gestao_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia as regras de gestão de banca."""
    await update.message.reply_text(MENSAGEM_GESTAO, parse_mode='Markdown')

async def plataforma_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia o link da plataforma oficial."""
    await update.message.reply_text(MENSAGEM_PLATAFORMA, parse_mode='Markdown', disable_web_page_preview=False)

async def ajuda_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia a lista de comandos disponíveis."""
    await update.message.reply_text(MENSAGEM_AJUDA, parse_mode='Markdown')

async def enviar_dica_do_dia(bot: Bot):
   async def main():
    print("Iniciando Bot BAC BO - Versão COMUNIDADE VIP...")
    application = Application.builder().token(TOKEN).build()
    
    # ATIVANDO OS NOVOS COMANDOS
    application.add_handler(CommandHandler("placar", placar_comando))
    application.add_handler(CommandHandler("gestao", gestao_comando))
    application.add_handler(CommandHandler("plataforma", plataforma_comando))
    application.add_handler(CommandHandler("ajuda", ajuda_comando))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em plena operação.")

    bot = application.bot
    
    # AGENDANDO AS TAREFAS AUTOMÁTICAS
    asyncio.create_task(enviar_e_fixar_mensagem_inicial(bot))
    asyncio.create_task(ciclo_de_sinais(bot))
    asyncio.create_task(enviar_mensagem_recorrente(bot))
    # ATIVANDO A NOVA TAREFA: DICA DO DIA
    asyncio.create_task(enviar_dica_do_dia(bot))

    print("Todas as tarefas automáticas (Sinais, Lembretes e Dicas) foram agendadas.")
    while True:
        await asyncio.sleep(3600)


async def main():
    print("Iniciando Bot BAC BO - Versão Final...")
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("gestao", gestao))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot em plena operação.")

    bot = application.bot
    asyncio.create_task(enviar_e_fixar_mensagem_inicial(bot))
    asyncio.create_task(ciclo_de_sinais(bot))
    asyncio.create_task(enviar_mensagem_recorrente(bot))

    print("Todas as tarefas automáticas de elite foram agendadas.")
    while True:
        await asyncio.sleep(3600)

# --- Funções Auxiliares (sem alterações) ---
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


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")
