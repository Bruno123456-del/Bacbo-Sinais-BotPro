# --- CÓDIGO COM AS MELHORIAS PEDIDAS ---

GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
GIF_WIN = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"

MENSAGEM_GESTAO = """
📊 **PROTOCOLO DE GESTÃO DE BANCA DE ELITE** 📊

A gestão de risco é o que separa amadores de profissionais. Siga este protocolo à risca:

1️⃣ **ENTRADA PRINCIPAL:** Use **1%** da sua banca.
    - *Exemplo: Banca de R$500,00 -> Entrada de R$5,00.*

2️⃣ **GALE 1 (Primeira Proteção):** Use **2%** da sua banca.
    - *Exemplo: Banca de R$500,00 -> Entrada de R$10,00.*

3️⃣ **GALE 2 (Proteção Máxima):** Use **4%** da sua banca.
    - *Exemplo: Banca de R$500,00 -> Entrada de R$20,00.*

🔁 **COBERTURA DO EMPATE:** Sempre cubra o empate com R$2,00 a cada entrada, pois o retorno é de até 80x.

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

IMG_WIN_ENTRADA = "imagens/win_entrada.png"

# NOVA FUNÇÃO: Enviar imagem de prova social automaticamente a cada 2 horas
import random
import os
from telegram import InputFile

async def enviar_prova_social_aleatoria(bot: Bot):
    imagens_prova = [
        "imagens/print_win_1.png",
        "imagens/print_win_2.png",
        "imagens/print_win_3.png",
        "imagens/print_usuario_msg1.png",
        "imagens/print_usuario_msg2.png"
    ]
    mensagens = [
        "🔥 Mano, faturei 280 com essa entrada! VLW 🔥",
        "📲 'Tava desacreditado e fiz 500 pila hoje kkk valeu! 💸",
        "👑 Mais um print real direto do grupo... gestão e disciplina dando certo!",
        "🚀 Não é sorte, é gestão + estratégia validada. CONFIA."
    ]

    imagem_escolhida = random.choice(imagens_prova)
    legenda = random.choice(mensagens)

    try:
        with open(imagem_escolhida, 'rb') as img:
            await bot.send_photo(chat_id=CANAL_ID, photo=InputFile(img), caption=legenda)
    except Exception as e:
        print(f"Erro ao enviar prova social: {e}")

# AGENDAR a cada 2 horas
async def loop_prova_social(bot: Bot):
    while True:
        await enviar_prova_social_aleatoria(bot)
        await asyncio.sleep(7200)  # 2 horas

# BOTÃO "JOGAR BAC BO" - Com estratégia embutida
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def botao_jogar_bacbo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
🎯 **ESTRATÉGIA BAC BO VALIDADA** 🎯

✅ Requisitos: Banca mínima de R$500,00

📌 Entradas:
- Vermelho: R$5
- Gale 1: R$10
- Gale 2: R$20

🎯 Cobertura de empate: R$2 por entrada (paga até 80x)

💡 Estratégia baseada em análise de padrão de repetições + estatística do histórico 1WIN.

🎮 Comece agora clicando no botão abaixo:
"""
    keyboard = [[InlineKeyboardButton("🎰 Jogar BAC BO na 1WIN", url=URL_CADASTRO)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode='Markdown')

# HANDLER
application.add_handler(CommandHandler("jogar", botao_jogar_bacbo))

# AGENDANDO
asyncio.create_task(loop_prova_social(bot))
