import asyncio
import logging
import random
from telegram import Bot, InputFile, Update
from telegram.ext import Application, CallbackContext, JobQueue
from telegram.error import TelegramError

# Importações locais
from config import Config
from main import Messages
from estrategia import Estrategia

# Configuração de logging para depuração
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variáveis globais para o placar
greens = 0
reds = 0

async def enviar_mensagem_fixada(bot: Bot, chat_id: str, messages: Messages):
    """Envia e fixa a mensagem de boas-vindas."""
    try:
        mensagem = await bot.send_message(chat_id=chat_id, text=messages.get_mensagem_fixada(), parse_mode='Markdown')
        await bot.pin_chat_message(chat_id=chat_id, message_id=mensagem.message_id)
        logger.info("Mensagem de boas-vindas enviada e fixada.")
    except TelegramError as e:
        logger.error(f"Erro ao enviar ou fixar mensagem: {e}")

async def ciclo_de_sinal(context: CallbackContext):
    """Executa um ciclo completo de envio de sinal e verificação de resultado."""
    global greens, reds
    
    bot = context.bot
    config = context.job.data['config']
    messages = context.job.data['messages']
    estrategia = context.job.data['estrategia']
    
    try:
        # 1. Mensagem de Análise
        logger.info("Iniciando análise para novo sinal.")
        msg_analise = await bot.send_animation(chat_id=config.CHAT_ID, animation=config.GIF_ANALISE, caption="🔍 Analisando o mercado em busca de uma nova oportunidade... Aguarde!")
        await asyncio.sleep(config.TEMPO_ANALISE)
        await bot.delete_message(chat_id=config.CHAT_ID, message_id=msg_analise.message_id)

        # 2. Gerar e Enviar Sinal
        sinal = estrategia.gerar_sinal()
        mensagem_sinal = messages.get_mensagem_sinal(sinal)
        await bot.send_message(chat_id=config.CHAT_ID, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal enviado: {sinal['direcao']}")

        # 3. Simular e Anunciar Resultado
        resultado = estrategia.simular_resultado()
        captions = messages.get_captions_win()
        
        if resultado == "entrada":
            greens += 1
            await bot.send_photo(chat_id=config.CHAT_ID, photo=open(config.IMG_WIN_ENTRADA, 'rb'), caption=captions["entrada"])
        elif resultado == "gale1":
            greens += 1
            await bot.send_photo(chat_id=config.CHAT_ID, photo=open(config.IMG_WIN_GALE1, 'rb'), caption=captions["gale1"])
        elif resultado == "gale2":
            greens += 1
            await bot.send_photo(chat_id=config.CHAT_ID, photo=open(config.IMG_WIN_GALE2, 'rb'), caption=captions["gale2"])
        else: # Stop Loss
            reds += 1
            await bot.send_animation(chat_id=config.CHAT_ID, animation=config.GIF_RED, caption=captions["stop_loss"])
        
        logger.info(f"Resultado: {resultado}. Placar atual: Greens {greens}, Reds {reds}")

        # 4. Enviar Placar
        placar_msg = messages.get_mensagem_placar(greens, reds)
        await bot.send_message(chat_id=config.CHAT_ID, text=placar_msg)

        # 5. Reforço e Prova Social (se for green)
        if resultado != "stop_loss":
            reforco = random.choice(messages.get_reforco_pos_win())
            await bot.send_message(chat_id=config.CHAT_ID, text=reforco, parse_mode='Markdown')
            
            prova_social_img = random.choice(config.PROVAS_SOCIAIS)
            prova_social_texto = random.choice(messages.get_textos_prova_social())
            await bot.send_photo(chat_id=config.CHAT_ID, photo=open(prova_social_img, 'rb'), caption=prova_social_texto)

    except FileNotFoundError as e:
        logger.error(f"Erro de arquivo não encontrado: {e}. Verifique se os caminhos em config.py estão corretos e se os arquivos existem.")
    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado no ciclo de sinal: {e}")

async def mensagem_recorrente(context: CallbackContext):
    """Envia a mensagem de reforço de cadastro periodicamente."""
    bot = context.bot
    config = context.job.data['config']
    messages = context.job.data['messages']
    
    try:
        await bot.send_message(chat_id=config.CHAT_ID, text=messages.get_mensagem_automatica_recorrente(), parse_mode='Markdown')
        logger.info("Mensagem recorrente enviada.")
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem recorrente: {e}")

async def post_init(application: Application):
    """Funções a serem executadas após a inicialização do bot."""
    config = application.bot_data['config']
    messages = application.bot_data['messages']
    await enviar_mensagem_fixada(application.bot, config.CHAT_ID, messages)

def main():
    """Função principal que inicializa e executa o bot."""
    try:
        config = Config()
        config.validate()
    except (ValueError, FileNotFoundError) as e:
        logger.critical(f"Erro crítico na configuração: {e}")
        return

    messages = Messages(config.URL_CADASTRO)
    estrategia = Estrategia(config)

    application = Application.builder().token(config.BOT_TOKEN).post_init(post_init).build()
    
    # Armazena instâncias para acesso nos jobs
    application.bot_data['config'] = config
    application.bot_data['messages'] = messages
    application.bot_data['estrategia'] = estrategia
    
    job_queue = application.job_queue
    
    # Agendar jobs
    job_queue.run_repeating(ciclo_de_sinal, interval=config.INTERVALO_SINAIS, first=10, data={'config': config, 'messages': messages, 'estrategia': estrategia})
    job_queue.run_repeating(mensagem_recorrente, interval=config.INTERVALO_MENSAGEM_RECORRENTE, first=60, data={'config': config, 'messages': messages})

    logger.info("Bot iniciado e jobs agendados.")
    application.run_polling()

if __name__ == '__main__':
    main()
