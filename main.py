import os
import asyncio
import random
import threading
from datetime import datetime, time as dt_time

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

# Validação inicial para garantir que as variáveis foram carregadas
if not TOKEN or not CHAT_ID:
    print("ERRO: BOT_TOKEN ou CHAT_ID não foram definidos no arquivo .env ou nas variáveis de ambiente do servidor.")
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
    "🔥 OPORTUNIDADE QUENTE! Analise e entre com sabedoria.",
    "🔔 ATENÇÃO! Mais um sinal fresquinho para você. Bora pra cima!",
    "🍀 SINAL DA SORTE! Acompanhe e faça sua jogada.",
    "📈 HORA DE AGIR! Sinal confirmado para você. Sucesso!",
    "💎 SINAL EXCLUSIVO! Não perca essa chance. Boa sorte!",
]

frases_agradecimento = [
    "Ganhei R$320 com seus sinais hoje! Gratidão 🙏🔥",
    "Você é brabo! Bati minha meta em 1 hora 💰🚀",
    "Confiei e tô no lucro! Obrigado 🔥💸",
    "Nunca ganhei tanto assim, bora pra cima 🔥🎯",
    "Incrível! Meus lucros dispararam com seus sinais. Muito obrigado!",
    "Meta batida e com folga! Vocês são demais!",
    "Finalmente um sinal que funciona de verdade! Gratidão eterna.",
    "Que dia! Graças a vocês, meu saldo só cresce. Valeu!",
    "Estou impressionado com a assertividade. Parabéns pelo trabalho!",
    "Meu dia mudou depois de seguir seus sinais. Muito feliz!",
]

# --- Variáveis de Controle de Estado ---
# Usar um dicionário é uma forma mais organizada de gerenciar o estado
estado = {
    "manha_iniciada": False,
    "noite_iniciada": False,
}

# --- Funções Assíncronas do Bot ---

async def gerenciar_periodos():
    """Verifica continuamente o horário e envia mensagens de início/fim de período."""
    print("INFO: Gerenciador de períodos iniciado.")
    while True:
        # Use datetime.utcnow() para compatibilidade com servidores (fuso UTC)
        agora = datetime.utcnow().time()
        
        # --- Lógica do Período da Manhã (16:00 - 20:00 UTC, equivale a 13:00 - 17:00 BRT) ---
        horario_manha = dt_time(16, 0) <= agora <= dt_time(20, 0)
        if horario_manha and not estado["manha_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="☀️ Bom dia, pessoal! Nossos sinais de BAC BO estão ativos. Fiquem ligados para as melhores oportunidades!")
                print("INFO: Período da manhã iniciado.")
                estado["manha_iniciada"] = True
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de início da manhã: {e}")

        elif not horario_manha and estado["manha_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="👋 Pessoal, o período de sinais da manhã foi encerrado. Voltamos à noite com mais oportunidades!")
                print("INFO: Período da manhã encerrado.")
                estado["manha_iniciada"] = False
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de fim da manhã: {e}")

        # --- Lógica do Período da Noite (22:00 - 01:00 UTC, equivale a 19:00 - 22:00 BRT) ---
        horario_noite = dt_time(22, 0) <= agora or agora <= dt_time(1, 0)
        if horario_noite and not estado["noite_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="🌙 Boa noite, traders! Estamos de volta com os sinais de BAC BO. Preparem-se para lucrar!")
                print("INFO: Período da noite iniciado.")
                estado["noite_iniciada"] = True
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de início da noite: {e}")

        elif not horario_noite and estado["noite_iniciada"]:
            try:
                await bot.send_message(chat_id=CHAT_ID, text="😴 É isso aí, galera! Encerramos os sinais de BAC BO por hoje. Amanhã tem mais! Boa noite a todos.")
                print("INFO: Período da noite encerrado.")
                estado["noite_iniciada"] = False
            except TelegramError as e:
                print(f"ERRO ao enviar mensagem de fim da noite: {e}")
        
        # Verifica a cada 30 segundos para ter uma resposta rápida às mudanças de período
        await asyncio.sleep(30)

async def enviar_sinal():
    """Envia um sinal completo com texto, botões e mídias aleatórias."""
    try:
        frase = random.choice(frases_ganhou)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"🎲 BAC BO SINAL AO VIVO\n\n{frase}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🎰 Jogar Bac Bo Agora", url="https://lkwn.cc/f1c1c45a" )
            ]])
        )

        # Usar 'with open' garante que os arquivos sejam fechados corretamente
        if random.random() < 0.2:
            with open(IMG_EMPATE, "rb") as photo:
                await bot.send_photo(chat_id=CHAT_ID, photo=photo)

        if random.random() < 0.6:
            with open(IMG_WIN, "rb") as animation:
                await bot.send_animation(chat_id=CHAT_ID, animation=animation)

        if random.random() < 0.4:
            mensagem = random.choice(frases_agradecimento)
            with open(IMG_AGRADECIMENTO, "rb") as photo:
                await bot.send_photo(
                    chat_id=CHAT_ID,
                    photo=photo,
                    caption=f"📩 *Mensagem recebida:*\n\n_{mensagem}_",
                    parse_mode="Markdown"
                )
        print("✅ Sinal enviado com sucesso!")

    except FileNotFoundError as e:
        print(f"ERRO: Arquivo de imagem não encontrado. Verifique se a pasta 'imagens' e os arquivos estão no repositório. Detalhe: {e}")
    except TelegramError as e:
        print(f"ERRO ao enviar sinal: {e}")

async def agendar_sinais():
    """Loop principal que agenda o envio de sinais em intervalos aleatórios."""
    print("INFO: Agendador de sinais iniciado.")
    while True:
        # Só envia sinais se estiver em um dos períodos ativos
        if estado["manha_iniciada"] or estado["noite_iniciada"]:
            await enviar_sinal()
            intervalo = random.randint(600, 1200)  # Entre 10 e 20 minutos
            print(f"INFO: Próximo sinal em {intervalo // 60} minutos.")
            await asyncio.sleep(intervalo)
        else:
            # Fora do horário, espera um pouco antes de verificar de novo
            await asyncio.sleep(60)

async def main_async():
    """Função principal que executa as tarefas concorrentemente."""
    # Roda o gerenciador de períodos e o agendador de sinais ao mesmo tempo
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
    # O Flask roda em sua própria thread para não bloquear o asyncio
    port = int(os.environ.get("PORT", 5000))
    # Desativar o banner do Werkzeug para um log mais limpo
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.run(host="0.0.0.0", port=port)

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    import sys
    print("INFO: Bot de Sinais BAC BO INICIADO...")
    
    # Inicia o Flask em uma thread separada
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Inicia a lógica principal do bot (asyncio)
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("INFO: Bot encerrado manualmente.")
    except Exception as e:
        print(f"ERRO CRÍTICO no loop principal: {e}")

