# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS - VERSÃO 17.0 "EDIÇÃO LEGENDÁRIA"
# CRIADO E APRIMORADO POR MANUS
# - PLACAR AO VIVO NAS MENSAGENS DE RESULTADO (GREEN/RED)
# - SISTEMA DE AFILIADOS SIMPLES COM RASTREAMENTO DE CONVITES
# ===================================================================================

import logging
import os
import random
import asyncio
from datetime import time, timedelta, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes, PersistenceInput, PicklePersistence, 
    ChatMemberHandler, MessageHandler, filters
)

# --- 1. CONFIGURAÇÕES E CREDENCIAIS ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "5011424031"))
FREE_CANAL_ID = int(os.getenv("CHAT_ID", "0").strip()) 
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID", "0").strip())

URL_CADASTRO_DEPOSITO = "https://win-agegate-promo-68.lovable.app/"
URL_INSTAGRAM = "https://www.instagram.com/apostasmilionariasvip/"
URL_TELEGRAM_FREE = "https://t.me/ApostasMilionariaVIP"
SUPORTE_TELEGRAM = "@Superfinds_bot" 

if not BOT_TOKEN or FREE_CANAL_ID == 0 or VIP_CANAL_ID == 0:
    raise ValueError("ERRO CRÍTICO: BOT_TOKEN, CHAT_ID ou VIP_CANAL_ID não estão configurados!"  )

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. MÍDIAS E CONTEÚDO VISUAL (sem alterações) ---
GIF_OFERTA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzBqZ3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
GIF_ANALISANDO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
GIF_GREEN_PRIMEIRA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
IMG_GALE1 = "https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/win_gale1.png"
GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
PROVAS_SOCIAIS_URLS = [f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{i}.png" for i in range(1, 14  )]

# --- 3. MENSAGENS DE MARKETING E FUNIL (sem alterações) ---
# ... (código das mensagens omitido por brevidade)

# --- 4. CONFIGURAÇÃO DOS JOGOS E PROBABILIDADES (sem alterações) ---
# ... (código dos jogos omitido por brevidade)

# --- 5. LÓGICA PRINCIPAL DO BOT ---

def inicializar_estatisticas(bot_data):
    if 'start_time' not in bot_data:
        bot_data['start_time'] = datetime.now()
    for ch in ['free', 'vip']:
        for stat in ['sinais', 'win_primeira', 'win_gale', 'loss']:
            if f'{stat}_{ch}' not in bot_data: bot_data[f'{stat}_{ch}'] = 0
            if f'daily_{stat}_{ch}' not in bot_data: bot_data[f'daily_{stat}_{ch}'] = 0
    # Inicializa o dicionário de afiliados
    if 'afiliados' not in bot_data:
        bot_data['afiliados'] = {}

async def enviar_sinal_especifico(context: ContextTypes.DEFAULT_TYPE, jogo: str, aposta: str, target_id: int):
    bd = context.bot_data
    channel_type = 'vip' if target_id == VIP_CANAL_ID else 'free'
    if bd.get(f"sinal_em_andamento_{target_id}", False):
        logger.warning(f"Pulei o sinal de {jogo} para o canal {target_id} pois outro já estava em andamento.")
        return
    bd[f"sinal_em_andamento_{target_id}"] = True
    try:
        await context.bot.send_animation(chat_id=target_id, animation=GIF_ANALISANDO, caption=f"🔎 Analisando padrões para uma entrada em **{jogo}**...")
        await asyncio.sleep(random.randint(5, 10))
        mensagem_sinal = (f"🔥 **ENTRADA CONFIRMADA | {jogo}** 🔥\n\n"
                          f"🎯 **Apostar em:** {aposta}\n"
                          f"🔗 **JOGAR NA PLATAFORMA CERTA:** [**CLIQUE AQUI**]({URL_CADASTRO_DEPOSITO})")
        if target_id == VIP_CANAL_ID:
            mensagem_sinal += "\n\n✨ _Sinal Exclusivo VIP!_"
        await context.bot.send_message(chat_id=target_id, text=mensagem_sinal, parse_mode='Markdown')
        logger.info(f"Sinal de {jogo} enviado para o canal {target_id}.")
        bd[f'sinais_{channel_type}'] += 1
        bd[f'daily_sinais_{channel_type}'] += 1
        await asyncio.sleep(random.randint(45, 75))
        probabilidades = ASSERTIVIDADE_JOGOS.get(jogo, ASSERTIVIDADE_JOGOS["default"])
        resultado = random.choices(["win_primeira", "win_gale", "loss"], weights=probabilidades, k=1)[0]
        bd[f'{resultado}_{channel_type}'] += 1
        bd[f'daily_{resultado}_{channel_type}'] += 1

        # ★★★ ATUALIZAÇÃO: PLACAR AO VIVO ★★★
        greens_dia = bd.get(f'daily_win_primeira_{channel_type}', 0) + bd.get(f'daily_win_gale_{channel_type}', 0)
        reds_dia = bd.get(f'daily_loss_{channel_type}', 0)
        placar_do_dia = f"📊 **Placar do Dia ({channel_type.upper()}):** {greens_dia}W - {reds_dia}L"

        if resultado == "win_primeira":
            caption = f"✅✅✅ **GREEN NA PRIMEIRA!** ✅✅✅\n\nQue tiro certeiro! Parabéns a todos que confiaram! 🤑\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_GREEN_PRIMEIRA, caption=caption)
        elif resultado == "win_gale":
            caption = f"✅ **GREEN NO GALE!** ✅\n\nPaciência e gestão trazem o lucro. Parabéns, time!\n\n{placar_do_dia}"
            await context.bot.send_photo(chat_id=target_id, photo=IMG_GALE1, caption=caption)
        else:
            caption = f"❌ **RED!** ❌\n\nFaz parte do jogo. Mantenham a gestão de banca e vamos para a próxima!\n\n{placar_do_dia}"
            await context.bot.send_animation(chat_id=target_id, animation=GIF_RED, caption=caption)
            
    except Exception as e:
        logger.error(f"Erro no ciclo de sinal para {jogo} no canal {target_id}: {e}")
    finally:
        bd[f"sinal_em_andamento_{target_id}"] = False

# --- 6. COMANDOS, MODERAÇÃO, EVENTOS E LOGS ---

async def log_admin_action(context: ContextTypes.DEFAULT_TYPE, action: str):
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 **Log de Admin:**\n{action}")
    except Exception as e:
        logger.error(f"Falha ao enviar log para o admin: {e}")

# ... (Comandos start, stats, sinal, ban, divulgar, oferta, vaga permanecem os mesmos)

# ★★★ NOVO COMANDO: GERAR LINK DE AFILIADO ★★★
async def afiliado_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID: return
    try:
        nome_afiliado = context.args[0]
        
        # Cria um novo link de convite para o canal gratuito
        link_convite = await context.bot.create_chat_invite_link(
            chat_id=FREE_CANAL_ID,
            name=f"Afiliado: {nome_afiliado}",
            member_limit=10000 # Limite alto para o link ser reutilizável
        )
        
        # Armazena o link e o nome do afiliado
        context.bot_data['afiliados'][link_convite.invite_link] = nome_afiliado
        
        mensagem_resposta = (
            f"✅ **Link de Afiliado Criado!**\n\n"
            f"**Afiliado:** {nome_afiliado}\n"
            f"**Link:** `{link_convite.invite_link}`\n\n"
            f"Envie este link para o seu afiliado. Quando novos membros entrarem por ele, você será notificado no log."
        )
        await update.message.reply_text(mensagem_resposta, parse_mode='Markdown')
        await log_admin_action(context, f"Link de afiliado criado para '{nome_afiliado}'.")

    except IndexError:
        await update.message.reply_text("⚠️ **Uso incorreto!**\nUse: `/afiliado <nome_do_afiliado>`\nExemplo: `/afiliado parceiro_joao`")
    except Exception as e:
        await update.message.reply_text(f"❌ **Erro ao criar link:** `{e}`")

# ★★★ ATUALIZAÇÃO: BOAS-VINDAS COM RASTREAMENTO DE AFILIADO ★★★
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = update.chat_member
    if result.new_chat_member.status == 'member' and result.old_chat_member.status != 'member':
        novo_membro = result.new_chat_member.user
        chat_id = result.chat.id
        
        # Verifica se o membro entrou por um link de afiliado
        link_convite = result.invite_link
        if link_convite and link_convite.invite_link in context.bot_data.get('afiliados', {}):
            nome_afiliado = context.bot_data['afiliados'][link_convite.invite_link]
            log_message = (f"🎉 **Novo Membro por Afiliação!**\n"
                           f"  - **Membro:** {novo_membro.first_name} (@{novo_membro.username})\n"
                           f"  - **Afiliado:** {nome_afiliado}")
            await log_admin_action(context, log_message)
        
        # ... (o resto da lógica de boas-vindas com botões permanece a mesma)
        if chat_id == FREE_CANAL_ID:
            mensagem = f"👋 Seja bem-vindo(a), {novo_membro.first_name}!\n\nVocê está no lugar certo para começar a lucrar. Fique de olho nos sinais gratuitos e explore nossos links úteis abaixo!"
            keyboard = [[InlineKeyboardButton("💎 QUERO ACESSO VIP 💎", url=f"https://t.me/{SUPORTE_TELEGRAM.lstrip('@' )}")], [InlineKeyboardButton("📸 NOSSO INSTAGRAM", url=URL_INSTAGRAM)]]
        elif chat_id == VIP_CANAL_ID:
            mensagem = f"🚀 Bem-vindo(a) à elite, {novo_membro.first_name}!\n\nVocê está na Sala VIP. Fique com a plataforma aberta e prepare-se para a nossa maratona de sinais!"
            keyboard = [[InlineKeyboardButton("💰 ACESSAR PLATAFORMA 💰", url=URL_CADASTRO_DEPOSITO)]]
        else: return
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg_enviada = await context.bot.send_message(chat_id=chat_id, text=mensagem, reply_markup=reply_markup)
        context.job_queue.run_once(lambda ctx: ctx.bot.delete_message(chat_id=chat_id, message_id=msg_enviada.message_id), 300)
        logger.info(f"Mensagem de boas-vindas com botões enviada para {novo_membro.first_name}.")

# ... (outras funções como image_handler, keyword_handler, etc. permanecem as mesmas)

# --- 8. FUNÇÃO PRINCIPAL (MAIN) ---
def main() -> None:
    logger.info("Iniciando o bot Super Finds - Versão 17.0 'Edição Legendária'...")
    
    persistence = PicklePersistence(filepath="bot_data.pkl", store_data=PersistenceInput(bot_data=True))
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()
    inicializar_estatisticas(app.bot_data)

    # Adiciona os comandos
    # ... (todos os comandos anteriores)
    app.add_handler(CommandHandler("afiliado", afiliado_command)) # ★★★ NOVO HANDLER DE AFILIADO ★★★
    
    # Adiciona os handlers de eventos
    app.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.CHAT_MEMBER))
    # ... (outros handlers)
    
    agendar_tarefas(app)
    
    logger.info("Bot Super Finds 'Edição Legendária' iniciado com sucesso.")
    app.run_polling()

if __name__ == "__main__":
    main()
