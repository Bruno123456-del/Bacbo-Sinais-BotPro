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

# >> GIFs (Adicionados novos GIFs para variedade )
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

# >> MENSAGENS PARA COMANDOS (Sem alterações )
MENSAGEM_GESTAO = "..." # Mantido o mesmo
MENSAGEM_PLATAFORMA = f"..." # Mantido o mesmo
MENSAGEM_AJUDA = "..." # Mantido o mesmo
DICAS_DO_DIA = ["..."] # Mantido o mesmo

# >> IMAGENS
# As imagens que você criou para os resultados
IMG_WIN_ENTRADA = "imagens/win_entrada.png"
IMG_WIN_GALE1 = "imagens/win_gale1.png"
IMG_WIN_GALE2 = "imagens/win_gale2.png"
# As imagens para os "prints fakes" de prova social
PROVAS_SOCIAIS = ["imagens/print_win_1.png", "imagens/print_win_2.png", "imagens/print_win_3.png"]

# >> MENSAGENS FIXAS E RECORRENTES (Sem alterações)
mensagem_fixada_texto = f"..." # Mantido o mesmo
reforco_pos_win = ["..."] # Mantido o mesmo
mensagem_automatica_recorrente = f"..." # Mantido o mesmo

# --- 3. CONFIGURAÇÃO DOS SINAIS E GESTÃO ---

# >> NOVA ESTRATÉGIA COM COBERTURA DE EMPATE
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
    """NOVO: Envia um print fake de vitória correspondente ao resultado."""
    mapa_resultado_imagem = {
        "win_entrada": IMG_WIN_ENTRADA,
        "win_gale1": IMG_WIN_GALE1,
        "win_gale2": IMG_WIN_GALE2
    }
    imagem_path = mapa_resultado_imagem.get(tipo_win)
    
    if not imagem_path:
        return

    try:
        legenda = random.choice([
            "📸 Comprovado! Resultado da nossa última entrada!",
            "💰 Prova social: WIN confirmado agora mesmo.",
            "🔥 Lucro real capturado e printado!"
        ])
        await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem_path, 'rb'), caption=legenda)
        print(f"✅ Print fake de '{tipo_win}' enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao tentar enviar print fake: {e}")

async def ciclo_de_sinais(bot: Bot):
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
                texto_prova = random.choice(["🔥 Nossos membros não param de lucrar!", "🚀 Mais um resultado positivo!", "💰 Print que fala por si só."])
                await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem_prova, 'rb'), caption=texto_prova)
            except Exception as e:
                print(f"Erro ao enviar prova social: {e}")

        intervalo_fixo = 15 * 60
        print(f"Aguardando 15 minutos para o próximo ciclo de sinal.")
        await asyncio.sleep(intervalo_fixo)

async def simular_e_enviar_sinal(bot: Bot):
    global placar
    config = random.choice(sinais_config)
    
    msg_analise = await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_ANALISE), caption="📡 **Conectando aos nossos servidores...**\n\n*Aguarde, a oportunidade perfeita está sendo lapidada.*")
    await asyncio.sleep(random.randint(10, 20))
    
    # >> BOTÃO COM TEXTO ALTERADO
    botao_plataforma = InlineKeyboardButton(text="💎 JOGAR BAC BO AGORA 💎", url=URL_CADASTRO)
    teclado_sinal = InlineKeyboardMarkup([[botao_plataforma]])
    
    # >> LÓGICA PARA ENVIAR O SINAL CORRETO (PADRÃO OU COBERTURA)
    if config["tipo"] == "cobertura_empate":
        mensagem_sinal = (
            f"**🔥 OPORTUNIDADE COM COBERTURA DETECTADA 🔥**\n\n"
            f"▪️ **Ativo:** `BAC BO`\n"
            f"▪️ **Estratégia:** `{config['estrategia']}`\n\n"
            f"**PLANO DE AÇÃO:**\n"
            f"1️⃣ **Entrada Principal (70% da aposta):** `{config['aposta_principal']}`\n"
            f"2️⃣ **Cobertura (30% da aposta):** `{config['aposta_secundaria']}`\n\n"
            f"🚨 *Esta estratégia visa cobrir o empate, que paga muito mais. Siga a gestão!*"
        )
    else: # Sinal padrão
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

    # >> LÓGICA DE RESULTADO COM ENVIO DE PRINT FAKE
    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN))
        await asyncio.sleep(2)
        await enviar_print_fake(bot, "win_entrada") # Envia o print fake
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando primeira proteção. Entrando no **GALE 1**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN))
        await asyncio.sleep(2)
        await enviar_print_fake(bot, "win_gale1") # Envia o print fake
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
        return

    await bot.send_message(chat_id=CHAT_ID, text="⚠️ **Atenção:** Ativando proteção máxima. Entrando no **GALE 2**.", reply_to_message_id=msg_sinal_enviada.message_id)
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_WIN))
        await asyncio.sleep(2)
        await enviar_print_fake(bot, "win_gale2") # Envia o print fake
        await asyncio.sleep(10)
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown', disable_web_page_preview=True)
    else:
        placar["reds"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=random.choice(GIFS_RED), caption="❌ **STOP LOSS**\n\n*O mercado não se moveu a nosso favor. Encerramos esta operação para proteger nosso capital. Disciplina é a chave do sucesso a longo prazo. Voltamos em breve.*")

# --- 5. FUNÇÕES PARA COMANDOS E TAREFAS AUTOMÁTICAS (Sem alterações) ---
async def placar_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #...código mantido
async def gestao_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #...código mantido
async def plataforma_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #...código mantido
async def ajuda_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #...código mantido
async def enviar_dica_do_dia(bot: Bot):
    #...código mantido
async def enviar_e_fixar_mensagem_inicial(bot: Bot):
    #...código mantido
async def enviar_mensagem_recorrente(bot: Bot):
    #...código mantido

# --- 6. FUNÇÃO PRINCIPAL QUE INICIA TUDO (Sem alterações) ---
async def main():
    #...código mantido

if __name__ == '__main__':
    #...código mantido
