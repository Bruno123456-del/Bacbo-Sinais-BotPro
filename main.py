importar sistema operacional
importar asyncio
importar aleatório
de dotenv importar load_dotenv
do telegrama importar atualização, bot, botão de teclado em linha, marcação de teclado em linha
de telegram.ext importar Application, CommandHandler, ContextTypes
de telegram.error importar BadRequest

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

Prezado(a) Investidor(a),

Para garantir uma experiência de alta performance e resultados sincronizados com nossos analistas, é *essencial* que você opere na mesma plataforma que utilizamos.

Nossos algoritmos são calibrados para **1WIN**.

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

Resultados consistentes desativar as ferramentas certas. Nossa estratégia é 100% compatível com **1WIN**.

Não perca mais tempo com plataformas não sincronizadas.

🔗 **Garanta sua vaga e bônus:** {URL_CADASTRO}

*A espécie favorecendo os bem preparados.*
"""

CHANCE_WIN_ENTRADA_INICIAL = 0,70
CHANCE_DE_VITÓRIA_1 = 0,80
CHANCE_DE_VITÓRIA_2 = 0,90

placar = {"verdes": 0, "vermelhos": 0}

# --- Estratégia Escada Asiática com Cobertura ---
def escada_asiatica(histórico):
    se len(histórico) < 4:
        retornar Nenhum
    últimos = histórico[-4:]
    if últimos[0] == últimos[1] e últimos[2] != últimos[1]:
        retornar {
            "direção": últimos[1],
            "cobertura": "Empatar",
            "cor_direcao": "🔴" if ultimos[1] == "Jogador" else "🔵",
            "cor_cobertura": "🟡"
        }
    retornar Nenhum

assíncrono def simular_e_enviar_sinal(bot: Bot):
    cartaz global

    historico = ["Jogador", "Jogador", "Banqueiro", "Jogador"] # Simulado. Substitua por histórico real.
    sinal = escada_asiatica(histórico)
    se não sinal:
        print("Nenhuma oportunidade bloqueada.")
        retornar

    msg_analise = await bot.send_animation(chat_id=CHAT_ID, animation=GIF_ANALISE, caption="⏳ Analisando com IA...")
    aguardar asyncio.sleep(10)

    botao_plataforma = InlineKeyboardButton(text="🎰 JOGAR BAC BO COM BÔNUS", url=URL_CADASTRO)
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
        f"▪️ Estratégia: Escada Asiática com Cobertura 🧠
▪️ Cor da Cobertura: Amarelo (🟡)
