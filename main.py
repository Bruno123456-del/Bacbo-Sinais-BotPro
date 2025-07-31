import os
import asyncio
import random
import threading
from datetime import datetime
from flask import Flask, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

# --- Carregando variáveis do ambiente ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_CADASTRO = os.getenv("URL_CADASTRO")

if not TOKEN or not CHAT_ID or not URL_CADASTRO:
    raise ValueError("❌ Variáveis BOT_TOKEN, CHAT_ID ou URL_CADASTRO não foram definidas.")

# --- Inicialização ---
bot = Bot(token=TOKEN)
app = Flask(__name__)
CORS(app)

# --- Variáveis de controle de risco e sinais ---
last_signal = None
win_streak = 0
loss_streak = 0

# --- URLs dos GIFs (substituir por URLs reais após upload) ---
GIF_WIN = "https://example.com/win.gif" # Substituir
GIF_LOSS = "https://example.com/loss.gif" # Substituir
GIF_TIE = "https://example.com/tie.gif" # Substituir

# --- Função principal de envio de sinais ---
async def send_signal():
    global last_signal, win_streak, loss_streak

    while True:
        # Lógica de gestão de risco (exemplo simples)
        if loss_streak >= 2: # Após 2 perdas consecutivas, tenta recuperar
            sinal = last_signal # Repete o último sinal
            risk_message = "⚠️ *Modo Recuperação Ativado!* ⚠️"
        elif win_streak >= 3: # Após 3 vitórias consecutivas, muda a estratégia
            sinal = random.choice([s for s in ["⚪ Branco", "🔴 Vermelho", "🔵 Azul"] if s != last_signal]) # Sinal diferente do último
            risk_message = "📈 *Ótima Sequência! Mudando a Estratégia.* 📈"
        else:
            sinal = random.choice(["⚪ Branco", "🔴 Vermelho", "🔵 Azul"])
            risk_message = ""

        # Simulação de resultado (para teste, remover em produção real)
        resultado_simulado = random.choice(["win", "loss", "tie"])

        if resultado_simulado == "win":
            win_streak += 1
            loss_streak = 0
            gif_url = GIF_WIN
            status_emoji = "✅"
            status_text = "VITÓRIA!"
        elif resultado_simulado == "loss":
            loss_streak += 1
            win_streak = 0
            gif_url = GIF_LOSS
            status_emoji = "❌"
            status_text = "DERROTA!"
        else: # Empate
            win_streak = 0
            loss_streak = 0
            gif_url = GIF_TIE
            status_emoji = "🟡"
            status_text = "EMPATE!"

        last_signal = sinal

        mensagem = (
            f"🎯 *SINAL BAC BO AUTOMÁTICO*\n\n"
            f"🎰 Entrada: {sinal}\n"
            f"\n"
            f"{status_emoji} *{status_text}*\n"
            f"[GIF do Resultado]({gif_url})\n\n"
            f"{risk_message}\n\n"
            f"🎁 Bônus de boas-vindas já disponível!\n"
            f"➡️ Cadastre-se: {URL_CADASTRO}"
        )

        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="Markdown")
            print(f"[{datetime.now().strftime('%d/%m %H:%M:%S')}] ✅ Sinal enviado: {sinal} - Resultado: {status_text}")
        except TelegramError as e:
            print(f"❌ Erro ao enviar sinal: {e}")

        await asyncio.sleep(600)  # 10 minutos

# --- Rota web do Flask ---
@app.route("/")
def home():
    html_content = f'''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bac Bo Sinais</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
                color: #e0e0e0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                overflow: hidden;
                position: relative;
            }}
            body::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: url('https://example.com/futuristic_bg.jpg') no-repeat center center fixed; /* Substituir */
                background-size: cover;
                opacity: 0.2;
                z-index: 0;
            }}
            .container {{
                background-color: rgba(25, 25, 40, 0.85);
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                text-align: center;
                position: relative;
                z-index: 1;
                max-width: 500px;
                width: 90%;
                border: 1px solid rgba(70, 70, 100, 0.5);
                backdrop-filter: blur(5px);
            }}
            h1 {{
                color: #00f2fe; /* Neon Blue */
                margin-bottom: 20px;
                font-size: 2.5em;
                text-shadow: 0 0 15px #00f2fe, 0 0 25px #00f2fe;
            }}
            p {{
                font-size: 1.1em;
                line-height: 1.6;
                margin-bottom: 30px;
            }}
            .btn-play {{
                background: linear-gradient(45deg, #ff00ff, #00f2fe); /* Neon Pink to Neon Blue */
                border: none;
                padding: 15px 30px;
                border-radius: 30px;
                color: white;
                font-size: 1.2em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                box-shadow: 0 5px 20px rgba(0, 242, 254, 0.4);
            }}
            .btn-play:hover {{
                transform: translateY(-5px) scale(1.05);
                box-shadow: 0 8px 25px rgba(0, 242, 254, 0.6);
            }}
            .footer {{
                margin-top: 30px;
                font-size: 0.9em;
                color: #a0a0a0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bem-vindo ao Bot de Sinais Bac Bo!</h1>
            <p>Prepare-se para uma experiência de jogo otimizada com nossos sinais automáticos e gestão de risco avançada. Junte-se à nossa comunidade e maximize suas chances de vitória!</p>
            <a href="{URL_CADASTRO}" target="_blank" class="btn-play">JOGAR BAC BO</a>
            <p class="footer">Seu sucesso é a nossa prioridade.</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content)

# --- Executa Flask em thread separada ---
def run_flask():
    app.run(host="0.0.0.0", port=10000)

# --- Inicia o bot e o servidor ---
def start():
    threading.Thread(target=run_flask).start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_signal())

if __name__ == "__main__":
    start()

