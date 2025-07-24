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

# >> GIFs (Mantidos para análise e red )
GIF_ANALISE = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"

# >> NOVAS IMAGENS DE VITÓRIA (coloque os caminhos corretos )
IMG_WIN_ENTRADA = "imagens/win_entrada.png"  # Imagem para Win na entrada (+4%)
IMG_WIN_GALE1 = "imagens/win_gale1.png"      # Imagem para Win no Gale 1 (+8%)
IMG_WIN_GALE2 = "imagens/win_gale2.png"      # Imagem para Win no Gale 2 (+16%)

# >> NOVAS IMAGENS PARA PROVA SOCIAL
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

# >> NOVO: PLACAR DE RESULTADOS
placar = {"greens": 0, "reds": 0}

# --- 4. FUNÇÕES DO BOT ---

async def simular_e_enviar_sinal(bot: Bot):
    """Ciclo completo de um sinal, com estética de luxo e novas funcionalidades."""
    global placar
    config = random.choice(sinais_config)
    
    # ETAPA 1: ANÁLISE (com GIF)
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
    
    # ETAPA 2: SINAL (com botão integrado)
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

    # ETAPA 3: RESULTADO (com IMAGENS PERSONALIZADAS)
    # Tentativa 1: WIN
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        placar["greens"] += 1
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_ENTRADA, 'rb'), caption="✅ **WIN NA ENTRADA PRINCIPAL!**\n\n💰 **LUCRO ALCANÇADO: +4%**\n\n*A precisão é a nossa marca. Parabéns a todos!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 2: GALE 1
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando primeira proteção. Entrando no **GALE 1**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        placar["greens"] += 1
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE1, 'rb'), caption="✅ **WIN NO GALE 1!**\n\n💰 **LUCRO TOTAL: +8%**\n\n*Gestão de risco executada com perfeição. Meta batida!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Tentativa 3: GALE 2
    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando proteção máxima. Entrando no **GALE 2**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        placar["greens"] += 1
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE2, 'rb'), caption="✅ **WIN NO GALE 2!**\n\n💰 **LUCRO TOTAL: +16%**\n\n*A persistência e a estratégia nos levaram à vitória!*")
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
    else:
        placar["reds"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_RED, caption="❌ **STOP LOSS**\n\n*O mercado não se moveu a nosso favor. Encerramos esta operação para proteger nosso capital. Disciplina é a chave do sucesso a longo prazo. Voltamos em breve.*")

# --- Funções de Ciclo e Comandos ---

async def ciclo_de_sinais(bot: Bot):
    """NOVO: Ciclo de sinais com placar e prova social."""
    sinais_enviados = 0
    while True:
        await simular_e_enviar_sinal(bot)
        sinais_enviados += 1
        
        # A cada 3 sinais, envia o placar e uma prova social
        if sinais_enviados % 3 == 0:
            await asyncio.sleep(15) # Pequena pausa
            
            # Envia o placar atualizado
            placar_texto = f"📊 **PLACAR ATUALIZADO** 📊\n\n✅ **Greens:** {placar['greens']}\n❌ **Reds:** {placar['reds']}\n\n*Consistência é o nosso jogo.*"
            await bot.send_message(chat_id=CHAT_ID, text=placar_texto, parse_mode='Markdown')
            await asyncio.sleep(10)

            # Envia uma prova social
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

        # Intervalo de 15 minutos entre os sinais
        intervalo_fixo = 15 * 60  # 900 segundos
        print(f"Aguardando 15 minutos para o próximo ciclo de sinal.")
        await asyncio.sleep(intervalo_fixo)

async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Protocolo de Gestão Avançada...", parse_mode='Markdown')

# --- 5. FUNÇÃO PRINCIPAL ---
async def main():
    print("Iniciando Bot BAC BO - Versão de Luxo Aprimorada...")
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

# --- Funções Auxiliares (sem alteração) ---
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
