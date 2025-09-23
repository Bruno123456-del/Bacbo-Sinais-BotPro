import random
import asyncio
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from config import (
    JOGOS_COMPLETOS, GIFS_ANALISE, GIFS_VITORIA, GIF_RED, IMG_GALE, IMAGENS_PROVA_COUNT,
    VIP_CANAL_ID, FREE_CANAL_ID, URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM
)
from config import (
    ESPERA_ANALISE_SINAL_VIP_MIN, ESPERA_ANALISE_SINAL_VIP_MAX,
    ESPERA_RESULTADO_SINAL_VIP_MIN, ESPERA_RESULTADO_SINAL_VIP_MAX,
    ESPERA_ANALISE_SINAL_FREE_MIN, ESPERA_ANALISE_SINAL_FREE_MAX,
    ESPERA_RESULTADO_SINAL_FREE_MIN, ESPERA_RESULTADO_SINAL_FREE_MAX
)
from messages import (
    get_vip_signal_message, get_vip_win_message, get_vip_gale_message, get_vip_loss_message,
    get_free_opportunity_message, get_free_opportunity_keyboard,
    get_free_result_message, get_free_result_keyboard
)

logger = logging.getLogger("bot_main")

async def _send_analysis_message(context, chat_id: int, jogo: str):
    """Envia a mensagem de análise inicial para o canal."""
    await context.bot.send_animation(chat_id=chat_id, animation=random.choice(GIFS_ANALISE), caption=f"Pessoal, estou analisando o {jogo} agora... Fiquem atentos.")

async def _send_vip_signal(context, jogo: str, aposta_escolhida: str):
    """Envia o sinal VIP para o canal VIP."""
    logger.info(f"Enviando sinal VIP completo para o jogo {jogo}.")
    await _send_analysis_message(context, VIP_CANAL_ID, jogo)
    await asyncio.sleep(random.randint(ESPERA_ANALISE_SINAL_VIP_MIN, ESPERA_ANALISE_SINAL_VIP_MAX))
    mensagem_sinal = get_vip_signal_message(jogo, aposta_escolhida)
    await context.bot.send_message(chat_id=VIP_CANAL_ID, text=mensagem_sinal, parse_mode=ParseMode.MARKDOWN)

async def _process_vip_result(context, jogo: str, dados_jogo: dict):
    """Processa e envia o resultado do sinal VIP."""
    bd = context.bot_data
    await asyncio.sleep(random.randint(ESPERA_RESULTADO_SINAL_VIP_MIN, ESPERA_RESULTADO_SINAL_VIP_MAX))
    
    resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=dados_jogo["assertividade"], k=1)[0]
    bd[f'{resultado}_vip'] += 1
    
    if resultado == "win_primeira":
        await context.bot.send_animation(chat_id=VIP_CANAL_ID, animation=random.choice(GIFS_VITORIA), caption=get_vip_win_message(jogo))
    elif resultado == "win_gale":
        await context.bot.send_photo(chat_id=VIP_CANAL_ID, photo=IMG_GALE, caption=get_vip_gale_message(jogo))
    else:
        await context.bot.send_animation(chat_id=VIP_CANAL_ID, animation=GIF_RED, caption=get_vip_loss_message(jogo))

async def _send_free_marketing_signal(context, jogo: str, aposta_escolhida: str, confianca: float):
    """Envia o sinal de marketing (fantasma) para o canal FREE."""
    bd = context.bot_data
    logger.info(f"Enviando Sinal Fantasma (marketing) para o jogo {jogo}.")
    await context.bot.send_animation(chat_id=FREE_CANAL_ID, animation=random.choice(GIFS_ANALISE), caption=f"Fala, pessoal! Júnior Moreira aqui. Acabei de identificar uma oportunidade no {jogo}...")
    await asyncio.sleep(random.randint(ESPERA_ANALISE_SINAL_FREE_MIN, ESPERA_ANALISE_SINAL_FREE_MAX))
    msg_oportunidade = get_free_opportunity_message(confianca, jogo)
    keyboard = InlineKeyboardMarkup(get_free_opportunity_keyboard())
    await context.bot.send_message(chat_id=FREE_CANAL_ID, text=msg_oportunidade, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    
    await asyncio.sleep(random.randint(ESPERA_RESULTADO_SINAL_FREE_MIN, ESPERA_RESULTADO_SINAL_FREE_MAX))
    
    greens_vip = bd.get("win_primeira_vip", 0) + bd.get("win_gale_vip", 0)
    reds_vip = bd.get("loss_vip", 0)
    assertividade_vip = (greens_vip / max(greens_vip + reds_vip, 1)) * 100
    
    msg_resultado = get_free_result_message(jogo, aposta_escolhida, greens_vip, reds_vip, assertividade_vip)
    keyboard_resultado = InlineKeyboardMarkup(get_free_result_keyboard())
    
    url_foto = f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{random.randint(1, IMAGENS_PROVA_COUNT)}.png"
    await context.bot.send_photo(chat_id=FREE_CANAL_ID, photo=url_foto, caption=msg_resultado, reply_markup=keyboard_resultado, parse_mode=ParseMode.MARKDOWN)

async def enviar_sinal_jogo(context, jogo: str, target_id: int, confianca: float):
    """Função principal para enviar sinais de jogo, adaptada para VIP ou FREE."""
    bd = context.bot_data
    dados_jogo = JOGOS_COMPLETOS.get(jogo, {})
    aposta_escolhida = random.choice(dados_jogo.get("apostas", ["Aposta Padrão"]))

    if target_id == VIP_CANAL_ID:
        await _send_vip_signal(context, jogo, aposta_escolhida)
        bd['sinais_vip'] += 1
        await _process_vip_result(context, jogo, dados_jogo)
    elif target_id == FREE_CANAL_ID:
        await _send_free_marketing_signal(context, jogo, aposta_escolhida, confianca)


