import os
import asyncio
import random
import threading
import sys
from datetime import datetime, time as dt_time, UTC

# Tente importar as bibliotecas e forneça uma mensagem de erro clara se faltarem
try:
    from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
    from telegram.error import TelegramError
    from dotenv import load_dotenv
    from flask import Flask
except ImportError:
    print("ERRO: Bibliotecas necessárias não encontradas.")
    print("Execute 'pip install python-telegram-bot python-dotenv Flask' para instalá-las.")
    exit()

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações do Bot ---
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("ERRO: BOT_TOKEN ou CHAT_ID não foram definidos.")
    exit()

try:
    bot = Bot(token=TOKEN)
except Exception as e:
    print(f"ERRO: Falha ao criar a instância do Bot. Verifique se o TOKEN é válido. Detalhe: {e}")
    exit()

# --- Caminhos e Frases ---
IMG_WIN = "imagens/win-futurista.gif"
IMG_EMPATE = "imagens/empate.png"
IMG_AGRADECIMENTO = "imagens/agradecimento.png"

frases_ganhou = [
    "✅ ENTRADA CONFIRMADA! Aposte agora com estratégia e foco!",
    "🎯 SINAL ENVIADO! Aproveite com gestão de banca inteligente.",
    "💰 APOSTA LIBERADA! Mantenha sua disciplina e siga o plano.",
    "📊 SINAL DE ALTA CONFIANÇA! Use cobertura se necessário.",
    "🚀 NOVO SINAL! Prepare-se para a ação e siga o gerenciamento.",
]

frases_agradecimento = [
    "Ganhei R$320 com seus sinais hoje! Gratidão 🙏🔥",
    "Você é brabo! Bati minha meta em 1 hora 💰🚀",
    "Confiei e tô no lucro! Obrigado 🔥💸",
    "Nunca ganhei tanto assim, bora pra cima 🔥🎯",
]

# --- Variáveis de Controle de Estado ---
estado = {
    "madrugada_iniciada": False,
    "manha_iniciada": False,
    "noite_iniciada": False,
}

# --- Funções Assíncronas do Bot ---

async def gerenciar_periodos():
    """Verifica continuamente o horário e envia mensagens de início/fim de período."""
    print("INFO: Gerenciador de períodos iniciado.")
    while True:
        agora_utc = datetime.now(UTC).time()
        
        # --- Lógica do Período da Madrugada (04:00 - 07:00 UTC -> 01:00 - 04:00 BRT) ---
        horario_madrugada = dt_time(4, 0) <= agora_utc <= dt_time(7, 0)
        if horario_madrugada and not estado["madrugada_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="🦉 Corujão de sinais ATIVO! Vamos operar na madrugada.")
                print("INFO: Período da MADRUGADA iniciado.")
                estado["madrugada_iniciada"] = True
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de início da madrugada: {e}")
        elif not horario_madrugada and estado["madrugada_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="☀️ Período da madrugada encerrado. Voltamos em breve com os sinais da manhã!")
                print("INFO: Período da MADRUGADA encerrado.")
                estado["madrugada_iniciada"] = False
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de fim da madrugada: {e}")

        # --- Lógica do Período da Manhã (12:00 - 15:00 UTC -> 09:00 - 12:00 BRT) ---
        horario_manha = dt_time(12, 0) <= agora_utc <= dt_time(15, 0)
        if horario_manha and not estado["manha_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="☀️ Bom dia! Nossos sinais da MANHÃ estão ativos. Fiquem ligados!")
                print("INFO: Período da MANHÃ iniciado.")
                estado["manha_iniciada"] = True
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de início da manhã: {e}")
        elif not horario_manha and estado["manha_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="🌙 Período da manhã encerrado. A próxima sessão de sinais será à noite!")
                print("INFO: Período da MANHÃ encerrado.")
                estado["manha_iniciada"] = False
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de fim da manhã: {e}")

        # --- Lógica do Período da Noite (22:00 - 01:00 UTC -> 19:00 - 22:00 BRT) ---
        horario_noite = dt_time(22, 0) <= agora_utc or agora_utc <= dt_time(1, 0)
        if horario_noite and not estado["noite_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="🌙 Boa noite! Estamos de volta com os sinais da NOITE.")
                print("INFO: Período da NOITE iniciado.")
                estado["noite_iniciada"] = True
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de início da noite: {e}")
        elif not horario_noite and estado["noite_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="😴 Sinais da noite encerrados. Nos vemos na sessão da madrugada! Bom descanso.")
                print("INFO: Período da NOITE encerrado.")
                estado["noite_iniciada"] = False
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de fim da noite: {e}")
        
        await asyncio.sleep(30)

async def enviar_sinal():
    """Envia um sinal completo."""
    try:
        frase = random.choice(frases_ganhou)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"🎲 BAC BO SINAL AO VIVO\n\n{frase}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🎰 Jogar Bac Bo Agora", url="https://lkwn.cc/f1c1c45a" )
            ]])
        )
        if random.random() < 0.2:
            with open(IMG_EMPATE, "rb") as photo: await bot.send_photo(chat_id=CHAT_ID, photo=photo)
        if random.random() < 0.6:
            with open(IMG_WIN, "rb") as animation: await bot.send_animation(chat_id=CHAT_ID, animation=animation)
        if random.random() < 0.4:
            mensagem = random.choice(frases_agradecimento)
            with open(IMG_AGRADECIMENTO, "rb") as photo:
                await bot.send_photo(
                    chat_id=CHAT_ID, photo=photo,
                    caption=f"📩 *Mensagem recebida:*\n\n_{mensagem}_",
                    parse_mode="Markdown"
                )
        print("✅ Sinal enviado com sucesso!")
    except FileNotFoundError as e:
        print(f"ERRO: Arquivo de imagem não encontrado: {e}")
    except TelegramError as e:
        print(f"ERRO ao enviar sinal: {e}")

async def agendar_sinais():
    """Loop principal que agenda o envio de sinais."""
    print("INFO: Agendador de sinais iniciado.")
    while True:
        if estado["madrugada_iniciada"] or estado["manha_iniciada"] or estado["noite_iniciada"]:
            await enviar_sinal()
            intervalo = random.randint(600, 1200)
            print(f"INFO: Próximo sinal em {intervalo // 60} minutos.")
            await asyncio.sleep(intervalo)
        else:
            await asyncio.sleep(60)

async def main_async():
    """Função principal que executa as tarefas concorrentemente."""
    await asyncio.gather(
        gerenciar_periodos(),
        agendar_sinais()
    )

# --- Flask para Manter o Bot Ativo ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot de Sinais BAC BO está ativo e rodando!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.run(host="0.0.0.0", port=port)

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    print("INFO: Bot de Sinais BAC BO INICIADO...")
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("INFO: Bot encerrado manualmente.")
    except Exception as e:
        print(f"ERRO CRÍTICO no loop principal: {e}")
