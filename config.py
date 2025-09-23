import os

# --- CONFIGURAÇÕES DE SEGURANÇA ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
FREE_CANAL_ID = int(os.getenv("FREE_CANAL_ID", "-1002808626127"))
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "-1003053055680"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "5011424031")) # Seu ID de admin

# --- CONFIGURAÇÕES GERAIS ---
URL_CADASTRO_DEPOSITO = "https://lkwn.cc/f1c1c45a" # SEU LINK DE AFILIADO
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
URL_VIP_ACESSO = "https://t.me/+q2CCKi1CKmljMTFh"
SUPORTE_TELEGRAM = "@Superfinds_bot"

# --- DADOS DOS JOGOS ---
JOGOS_COMPLETOS = {
    "Fortune Tiger 🐅": {"apostas": ["10 Rodadas Turbo", "15 Rodadas Normal"], "assertividade": [92, 7, 1]},
    "Aviator ✈️": {"apostas": ["Sair em 1.50x", "Sair em 2.00x"], "assertividade": [95, 4, 1]},
    "Mines 💣": {"apostas": ["3 Minas - 4 Cliques", "5 Minas - 2 Cliques"], "assertividade": [89, 9, 2]},
    "Bac Bo 🎲": {"apostas": ["Player", "Banker"], "assertividade": [94, 5, 1]},
    "Dragon Tiger 🐉🐅": {"apostas": ["Dragon", "Tiger"], "assertividade": [93, 6, 1]},
    "Roleta Brasileira 🇧🇷": {"apostas": ["Vermelho", "Preto", "1ª Dúzia"], "assertividade": [90, 8, 2]},
    "Spaceman 👨‍🚀": {"apostas": ["Sair em 1.80x", "Sair em 2.50x"], "assertividade": [94, 5, 1]},
    "Penalty Shoot-Out ⚽": {"apostas": ["Gol", "Defesa"], "assertividade": [91, 7, 2]},
    "Fortune Rabbit 🐰": {"apostas": ["8 Rodadas Turbo", "12 Rodadas Normal"], "assertividade": [90, 8, 2]},
    "Gates of Olympus ⚡": {"apostas": ["Ante Bet Ativo", "20 Rodadas Normal"], "assertividade": [88, 10, 2]},
    "Sweet Bonanza 🍭": {"apostas": ["Ante Bet 25%", "15 Rodadas Normal"], "assertividade": [89, 9, 2]},
    "Plinko 🎯": {"apostas": ["16 Pinos - Médio", "12 Pinos - Alto"], "assertividade": [87, 11, 2]},
    "Crazy Time 🎪": {"apostas": ["Número 1", "Número 2", "Coin Flip"], "assertividade": [85, 13, 2]},
    "Lightning Roulette ⚡": {"apostas": ["Números Sortudos", "Vermelho"], "assertividade": [89, 9, 2]},
    "Andar Bahar 🃏": {"apostas": ["Andar", "Bahar"], "assertividade": [92, 6, 2]}
}

# --- GIFs E IMAGENS ---
GIFS_ANALISE = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"]
GIFS_VITORIA = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"]
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
IMG_GALE = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
IMAGENS_PROVA_COUNT = 19 # Número de imagens de prova disponíveis

# --- TEMPOS DE AGENDAMENTO (em segundos ) ---
INTERVALO_SINAL_AUTOMATICO = 45 * 60
INTERVALO_MARKETING_AUTOMATICO = 90 * 60

# --- TEMPOS DE ESPERA (em segundos) ---
ESPERA_ANALISE_SINAL_VIP_MIN = 8
ESPERA_ANALISE_SINAL_VIP_MAX = 12
ESPERA_RESULTADO_SINAL_VIP_MIN = 60
ESPERA_RESULTADO_SINAL_VIP_MAX = 90
ESPERA_ANALISE_SINAL_FREE_MIN = 5
ESPERA_ANALISE_SINAL_FREE_MAX = 8
ESPERA_RESULTADO_SINAL_FREE_MIN = 70
ESPERA_RESULTADO_SINAL_FREE_MAX = 100
