
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
GIF_ANALISE = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
GIF_WIN = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"

IMG_WIN_ENTRADA = "imagens/win_entrada.png"
IMG_WIN_GALE1 = "imagens/win_gale1.png"
IMG_WIN_GALE2 = "imagens/win_gale2.png"

PROVAS_SOCIAIS = ["imagens/print_win_1.png", "imagens/print_win_2.png", "imagens/print_win_3.png"]

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

CHANCE_WIN_ENTRADA_INICIAL = 0.70
CHANCE_WIN_GALE_1 = 0.80
CHANCE_WIN_GALE_2 = 0.90

placar = {"greens": 0, "reds": 0}

# --- Estratégia Escada Asiática com Cobertura ---
def escada_asiatica(historico):
    if len(historico) < 4:
        return None
    ultimos = historico[-4:]
    if ultimos[0] == ultimos[1] and ultimos[2] != ultimos[1]:
        return {
            "direcao": ultimos[1],
            "cobertura": "Empate",
            "cor_direcao": "🔴" if ultimos[1] == "Player" else "🔵",
            "cor_cobertura": "🟡"
        }
    return None

async def simular_e_enviar_sinal(bot: Bot):
    global placar

    historico = ["Player", "Player", "Banker", "Player"]  # Simulado. Substituir por histórico real.
    sinal = escada_asiatica(historico)
    if not sinal:
        print("Nenhuma oportunidade detectada.")
        return

    msg_analise = await bot.send_animation(chat_id=CHAT_ID, animation=GIF_ANALISE, caption="⏳ Analisando com IA...")
    await asyncio.sleep(10)

    botao_plataforma = InlineKeyboardButton(text="💎 ENTRAR NA PLATAFORMA 💎", url=URL_CADASTRO)
    teclado_sinal = InlineKeyboardMarkup([[botao_plataforma]])

    mensagem_sinal = (
        f"🔥 OPORTUNIDADE DE ENTRADA DETECTADA 🔥

"
        f"▪️ Ativo: BAC BO
"
        f"▪️ Direção: {sinal['direcao']} {sinal['cor_direcao']}
"
        f"▪️ Cobertura: {sinal['cobertura']} {sinal['cor_cobertura']}
"
        f"▪️ Estratégia: Escada Asiática com Cobertura

"
        f"PLANO DE AÇÃO:
"
        f"1️⃣ Entrada Principal: Meta de +4%
"
        f"2️⃣ Proteção 1 (Gale): Se necessário
"
        f"3️⃣ Proteção 2 (Gale): Se necessário

"
        f"⚠️ Opere com precisão. Siga a gestão."
    )

    await msg_analise.delete()
    msg_sinal_enviada = await bot.send_message(chat_id=CHAT_ID, text=mensagem_sinal, reply_markup=teclado_sinal)

    await asyncio.sleep(120)

    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN)
        await asyncio.sleep(2)
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_ENTRADA, 'rb'), caption="✅ WIN NA ENTRADA PRINCIPAL!
💰 LUCRO ALCANÇADO: +4%")
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown')
        return

    await bot.send_message(chat_id=CHAT_ID, text="⚠️ Ativando GALE 1.")
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN)
        await asyncio.sleep(2)
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE1, 'rb'), caption="✅ WIN NO GALE 1!
💰 LUCRO TOTAL: +8%")
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown')
        return

    await bot.send_message(chat_id=CHAT_ID, text="⚠️ Ativando GALE 2.")
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN)
        await asyncio.sleep(2)
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE2, 'rb'), caption="✅ WIN NO GALE 2!
💰 LUCRO TOTAL: +16%")
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown')
    else:
        placar["reds"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_RED, caption="❌ STOP LOSS

Encerramos para proteger o capital.")

async def ciclo_de_sinais(bot: Bot):
    sinais_enviados = 0
    while True:
        await simular_e_enviar_sinal(bot)
        sinais_enviados += 1

        if sinais_enviados % 3 == 0:
            await bot.send_message(chat_id=CHAT_ID, text=f"📊 PLACAR
✅ Greens: {placar['greens']}
❌ Reds: {placar['reds']}", parse_mode='Markdown')
            try:
                imagem = random.choice(PROVAS_SOCIAIS)
                texto = random.choice([
                    "🔥 Veja esse resultado incrível!",
                    "🚀 Nossa comunidade está lucrando pesado!",
                    "💰 Resultado que fala por si só!"
                ])
                await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem, 'rb'), caption=texto)
            except Exception as e:
                print(f"Erro ao enviar prova social: {e}")

        await asyncio.sleep(15 * 60)

async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Protocolo de Gestão Avançada...", parse_mode='Markdown')

async def enviar_e_fixar_mensagem_inicial(bot: Bot):
    try:
        msg = await bot.send_message(chat_id=CHAT_ID, text=mensagem_fixada_texto, parse_mode='Markdown')
        await bot.pin_chat_message(chat_id=CHAT_ID, message_id=msg.message_id)
    except Exception as e:
        print(f"Erro ao fixar mensagem: {e}")

async def enviar_mensagem_recorrente(bot: Bot):
    while True:
        await asyncio.sleep(6 * 60 * 60)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem_automatica_recorrente, parse_mode='Markdown')
        except Exception as e:
            print(f"Erro mensagem recorrente: {e}")

async def main():
    print("Iniciando Bot BAC BO com estratégia Escada Asiática...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("gestao", gestao))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    bot = application.bot
    asyncio.create_task(enviar_e_fixar_mensagem_inicial(bot))
    asyncio.create_task(ciclo_de_sinais(bot))
    asyncio.create_task(enviar_mensagem_recorrente(bot))

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot finalizado.")
