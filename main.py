# ===================================================================================
# BOT DE SINAIS - VERSÃO PREMIUM 2.1 "CONVERSOR AUTOMÁTICO"
# OTIMIZADO POR MANUS
#
# - [NOVO] Sinais 100% automáticos com intervalo e horário de operação configurável.
# - [NOVO] Comando /autosinal para admin ligar/desligar a automação em tempo real.
# - [NOVO] Agendador de tarefas mestre para gerenciar múltiplos eventos.
# - [MANTIDO] Comando /placar público para prova social em tempo real.
# - [MANTIDO] Mensagem pós-GREEN automática para criar desejo pelo VIP.
# - [MANTIDO] Lógica "anti-red" para uma experiência de sinal mais positiva.
# - [MANTIDO] Variações de texto e emojis para uma comunicação mais humana.
# - [MANTIDO] Estrutura de código profissional com classes e melhor organização.
# - [MANTIDO] Funil de DMs com gatilhos de urgência e prova social.
# - [MANTIDO] Healthcheck Flask para compatibilidade com Render.
# ===================================================================================

import os
import logging
import random
import asyncio
import threading
from datetime import timedelta, datetime
from dataclasses import dataclass, field

try:
    from telegram import Update
    from telegram.constants import ParseMode
    from telegram.ext import (
        Application, CommandHandler, ContextTypes, PicklePersistence,
        MessageHandler, filters
    )
    from flask import Flask
    _LIBRARIES_AVAILABLE = True
except ImportError:
    _LIBRARIES_AVAILABLE = False
    class Update: pass
    class ContextTypes:
        class DEFAULT_TYPE: pass
    class Application: pass

# --- 0. LOGGING E VALIDAÇÃO DE AMBIENTE ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("ManusBot")

if not _LIBRARIES_AVAILABLE:
    logger.critical("ERRO CRÍTICO: Bibliotecas essenciais (telegram, flask) não encontradas.")

# --- 1. CONFIGURAÇÕES GLOBAIS E CREDENCIAIS ---
def _to_int(v: str, default: int = 0) -> int:
    s = str(v).strip()
    if not s: return default
    if s.startswith("-"):
        s2 = s[1:]
        return -int(s2) if s2.isdigit() else default
    return int(s) if s.isdigit() else default

@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
    ADMIN_ID: int = _to_int(os.getenv("ADMIN_ID", "0"))
    FREE_CHANNEL_ID: int = _to_int(os.getenv("CHAT_ID", "0"))
    VIP_CHANNEL_ID: int = _to_int(os.getenv("VIP_CANAL_ID", "0"))

    URL_CADASTRO: str = "https://win-agegate-promo-68.lovable.app/"
    URL_TELEGRAM_FREE: str = "https://t.me/ApostasMilionariaVIP"
    SUPORTE_USERNAME: str = "@Superfinds_bot"
    VIP_ACCESS_LINK: str = "https://t.me/+q2CCKi1CKmljMTFh"

    def validate(self ):
        errors = []
        if not self.BOT_TOKEN: errors.append("BOT_TOKEN")
        if self.ADMIN_ID == 0: errors.append("ADMIN_ID")
        if self.FREE_CHANNEL_ID == 0: errors.append("CHAT_ID (FREE_CHANNEL_ID)")
        if self.VIP_CHANNEL_ID == 0: errors.append("VIP_CANAL_ID")
        if not self.VIP_ACCESS_LINK: errors.append("VIP_ACCESS_LINK")
        if errors:
            logger.critical("ERRO CRÍTICO DE CONFIGURAÇÃO! Variáveis ausentes: %s", ", ".join(errors))
            raise SystemExit(1)

CONFIG = Config()
CONFIG.validate()

# --- 2. CONTEÚDO: MÍDIAS E TEXTOS ---
@dataclass(frozen=True)
class Media:
    ANALISANDO: str = "https://media.giphy.com/media/.../giphy.gif"
    GREEN: str = "https://media.giphy.com/media/.../giphy.gif"
    GALE1: str = "https://raw.githubusercontent.com/.../win_gale1.png"
    RED: str = "https://media.giphy.com/media/.../giphy.gif"
    OFERTA: str = "https://media.giphy.com/media/.../giphy.gif"
    PROVAS_SOCIAIS: list[str] = field(default_factory=lambda: [
        f"https://raw.githubusercontent.com/.../prova{i}.png"
        for i in range(1, 14 )
    ])

@dataclass(frozen=True)
class Text:
    BOAS_VINDAS_PUBLICO: str = "👋 Seja bem-vindo(a), {user_name}! ..."
    BOAS_VINDAS_DM: str = "💎 **QUER LUCRAR COM SINAIS...**"
    COMPROVANTE_RECEBIDO: str = "✅ Recebi seu comprovante! ..."
    ACESSO_VIP_LIBERADO: str = "Parabéns! 🎉 ..."
    COMPROVANTE_PARA_ADMIN: str = "📩 **Novo Comprovante...**"
    PLACA_DIA_TEMPLATE: str = "📊 **Placar do Dia...**"
    MENSAGEM_POS_GREEN_FREE: str = "🤑 **GREEN NO GRUPO FREE!** ..."
    LEGENDAS_PROVA_SOCIAL: list[str] = field(default_factory=lambda: [
        "🔥 **O GRUPO VIP ESTÁ PEGANDO FOGO!** 🔥...",
        "🚀 **RESULTADO DE MEMBRO VIP!** 🚀...",
        "🤔 **AINDA NA DÚVIDA?** 🤔...",
        "✅ **RESULTADOS FALAM MAIS QUE PALAVRAS!** ✅..."
    ])

MEDIA = Media()
TEXT = Text()

# --- 3. JOGOS E ESTATÍSTICAS ---
@dataclass
class Game:
    name: str
    bets: list[str]
    assertiveness: list[int] = field(default_factory=lambda: [70, 20, 10])

class GameManager:
    def __init__(self):
        self.games = {
            "Bac Bo 🎲": Game("Bac Bo 🎲", ["Player", "Banker", "Tie (Empate)"], [70, 20, 10]),
            "Roleta 룰렛": Game("Roleta 룰렛", ["Vermelho ⚫", "Preto 🔴", "Par", "Ímpar", "1ª Dúzia"], [68, 22, 10]),
            "Aviator ✈️": Game("Aviator ✈️", ["Buscar vela de 1.80x", "Buscar vela de 2.10x"], [75, 15, 10]),
            "Mines 💣": Game("Mines 💣", ["3 minas - Tentar 4 rodadas", "5 minas - Tentar 2 rodadas"], [65, 20, 15]),
            "Fortune Dragon 🐲": Game("Fortune Dragon 🐲", ["8 Rodadas Turbo", "10 Rodadas Normal"], [62, 23, 15]),
        }
        self.game_map = {key.split(" ")[0].lower(): key for key in self.games.keys()}

    def get_game(self, name: str) -> Game | None:
        return self.games.get(name)

    def get_game_by_short_name(self, short_name: str) -> Game | None:
        full_name = self.game_map.get(short_name.lower())
        return self.get_game(full_name) if full_name else None

    def get_random_bet(self, game_name: str) -> str | None:
        game = self.get_game(game_name)
        return random.choice(game.bets) if game else None

GAME_MANAGER = GameManager()

class StatsManager:
    def __init__(self, bot_data: dict):
        self.data = bot_data
        if 'start_time' not in self.data:
            self.data['start_time'] = datetime.now()
        for ch in ['free', 'vip']:
            for stat in ['sinais', 'win', 'gale', 'loss']:
                self.data.setdefault(f'total_{stat}_{ch}', 0)
                self.data.setdefault(f'daily_{stat}_{ch}', 0)
        self.data.setdefault('last_result_free', None)

    def record_signal(self, channel: str):
        self.data[f'total_sinais_{channel}'] += 1
        self.data[f'daily_sinais_{channel}'] += 1

    def record_result(self, channel: str, result: str):
        self.data[f'total_{result}_{channel}'] += 1
        self.data[f'daily_{result}_{channel}'] += 1
        if channel == 'free':
            self.data['last_result_free'] = result

    def get_daily_score(self, channel: str) -> tuple[int, int]:
        wins = self.data.get(f'daily_win_{channel}', 0) + self.data.get(f'daily_gale_{channel}', 0)
        losses = self.data.get(f'daily_loss_{channel}', 0)
        return wins, losses

    def reset_daily(self):
        for ch in ['free', 'vip']:
            for stat in ['sinais', 'win', 'gale', 'loss']:
                self.data[f'daily_{stat}_{ch}'] = 0
        self.data['last_result_free'] = None
        logger.info("✅ Estatísticas diárias resetadas com sucesso.")

# --- 4. ENVIO DE SINAIS ---
async def send_signal(context: ContextTypes.DEFAULT_TYPE, game_name: str, channel_type: str = "free"):
    chat_id = CONFIG.FREE_CHANNEL_ID if channel_type == "free" else CONFIG.VIP_CHANNEL_ID
    stats = StatsManager(context.bot_data)

    game = GAME_MANAGER.get_game(game_name)
    if not game:
        logger.error("Jogo não encontrado: %s", game_name)
        return
    bet_choice = random.choice(game.bets)

    stats.record_signal(channel_type)

    await context.bot.send_animation(
        chat_id=chat_id,
        animation=MEDIA.ANALISANDO,
        caption=f"📊 Analisando jogo {game.name}...\nAguardando oportunidade...",
        parse_mode=ParseMode.MARKDOWN
    )
    await asyncio.sleep(3)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"🚨 **ENTRADA CONFIRMADA** 🚨\n\n🎮 Jogo: {game.name}\n🎯 Apostar em: *{bet_choice}*\n\nBoa sorte a todos 🍀",
        parse_mode=ParseMode.MARKDOWN
    )
    await asyncio.sleep(3)
    
    resultado = random.choices(["win", "gale", "loss"], weights=game.assertiveness, k=1)[0]

    if resultado == "win":
        await context.bot.send_animation(chat_id=chat_id, animation=MEDIA.GREEN, caption="✅ **GREEN DE PRIMEIRA!** 🤑", parse_mode=ParseMode.MARKDOWN)
        stats.record_result(channel_type, "win")
    elif resultado == "gale":
        await context.bot.send_photo(chat_id=chat_id, photo=MEDIA.GALE1, caption="⚠️ Deu Gale 1! Entrar novamente.", parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(3)
        await context.bot.send_animation(chat_id=chat_id, animation=MEDIA.GREEN, caption="✅ **GREEN NO GALE 1!** 💰", parse_mode=ParseMode.MARKDOWN)
        stats.record_result(channel_type, "gale")
    else:  # red
        if channel_type == "free":
            await context.bot.send_animation(chat_id=chat_id, animation=MEDIA.GREEN, caption="✅ **GREEN DE PRIMEIRA!** 🤑", parse_mode=ParseMode.MARKDOWN)
            stats.record_result(channel_type, "win") # Grava como WIN para o placar público
            await context.bot.send_message(chat_id=chat_id, text=TEXT.MENSAGEM_POS_GREEN_FREE.format(link_cadastro=CONFIG.URL_CADASTRO), parse_mode=ParseMode.MARKDOWN)
        else: # No VIP, o RED é mostrado normalmente
            await context.bot.send_animation(chat_id=chat_id, animation=MEDIA.RED, caption="❌ Infelizmente Red...", parse_mode=ParseMode.MARKDOWN)
            stats.record_result(channel_type, "loss")

    if channel_type == "free":
        await context.bot.send_animation(chat_id=chat_id, animation=MEDIA.OFERTA, caption=f"🔥 Não fique de fora do nosso VIP! Acesse agora mesmo {CONFIG.VIP_ACCESS_LINK}", parse_mode=ParseMode.MARKDOWN)

# --- 5. PROVAS SOCIAIS ---
async def send_social_proof(context: ContextTypes.DEFAULT_TYPE):
    chat_id = CONFIG.FREE_CHANNEL_ID
    img_url = random.choice(MEDIA.PROVAS_SOCIAIS)
    caption = random.choice(TEXT.LEGENDAS_PROVA_SOCIAL)
    await context.bot.send_photo(chat_id=chat_id, photo=img_url, caption=caption, parse_mode=ParseMode.MARKDOWN)

# --- 6. FUNIL DE DMs ---
async def dm_funnel_sequence(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    try:
        await context.bot.send_message(chat_id=user_id, text=TEXT.BOAS_VINDAS_DM.format(link_cadastro=CONFIG.URL_CADASTRO), parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(3)
        await context.bot.send_message(chat_id=user_id, text="⚡ *Apenas hoje*: Deposite e ganhe +500% de bônus! Promoção limitada.", parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(3)
        prova_url = random.choice(MEDIA.PROVAS_SOCIAIS)
        await context.bot.send_photo(chat_id=user_id, photo=prova_url, caption="Olha o que os membros VIP estão lucrando! 💰", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning("Não foi possível enviar funil para %s: %s", user_id, e)

# --- 7. TAREFAS AGENDADAS ---
# [SEÇÃO TOTALMENTE ATUALIZADA POR MANUS PARA SINAIS AUTOMÁTICOS]

async def scheduled_signal_task(context: ContextTypes.DEFAULT_TYPE):
    """
    Tarefa agendada para enviar um sinal automático para o canal gratuito.
    Esta função é chamada pelo agendador principal.
    """
    logger.info("ROTINA AUTOMÁTICA: Iniciando tarefa de envio de sinal agendado.")
    try:
        # 1. Escolhe um jogo aleatório da lista de jogos disponíveis no GameManager
        game_name = random.choice(list(GAME_MANAGER.games.keys()))
        logger.info(f"ROTINA AUTOMÁTICA: Jogo aleatório selecionado para o sinal: {game_name}")

        # 2. Chama a função principal de envio de sinal, direcionando para o canal "free"
        await send_signal(context, game_name, channel_type="free")

        logger.info(f"ROTINA AUTOMÁTICA: Sinal para o jogo {game_name} enviado com sucesso para o canal gratuito.")

    except Exception as e:
        logger.error(f"ROTINA AUTOMÁTICA: Falha crítica ao executar a tarefa de sinal agendado: {e}", exc_info=True)

async def reset_daily_stats(context: ContextTypes.DEFAULT_TYPE):
    """Esta função reseta as estatísticas diárias. Permanece inalterada."""
    StatsManager(context.bot_data).reset_daily()

async def scheduled_tasks(application: Application):
    """
    Loop principal que gerencia TODAS as tarefas agendadas do bot.
    - Reseta as estatísticas diariamente à meia-noite.
    - Envia sinais automáticos em intervalos definidos.
    """
    logger.info("AGENDADOR DE TAREFAS MESTRE INICIADO.")
    
    # --- CONFIGURAÇÕES DO SINAL AUTOMÁTICO ---
    # Altere aqui o intervalo em minutos entre cada sinal
    SIGNAL_INTERVAL_MINUTES = 35 
    SIGNAL_INTERVAL_SECONDS = SIGNAL_INTERVAL_MINUTES * 60
    
    last_signal_time = datetime.now() - timedelta(seconds=SIGNAL_INTERVAL_SECONDS)

    while True:
        now = datetime.now()
        ctx = ContextTypes.DEFAULT_TYPE(application=application, bot=application.bot)

        # --- TAREFA 1: Resetar estatísticas diárias (executa perto da meia-noite) ---
        if now.hour == 0 and now.minute < 2:
            try:
                await reset_daily_stats(ctx)
                logger.info("AGENDADOR: Tarefa de reset de estatísticas diárias executada com sucesso.")
                await asyncio.sleep(120) 
            except Exception as e:
                logger.error(f"AGENDADOR: Erro crítico ao resetar estatísticas diárias: {e}")

        # --- TAREFA 2: Enviar sinal automático em intervalos ---
        is_autosinal_enabled = ctx.bot_data.get('autosinal_enabled', True)
        is_operating_hours = 8 <= now.hour < 23

        if is_autosinal_enabled and is_operating_hours:
            time_since_last_signal = (now - last_signal_time).total_seconds()
            if time_since_last_signal >= SIGNAL_INTERVAL_SECONDS:
                logger.info(f"AGENDADOR: Intervalo de {SIGNAL_INTERVAL_MINUTES} minutos atingido. Disparando sinal automático.")
                try:
                    await scheduled_signal_task(ctx)
                    last_signal_time = now
                except Exception as e:
                    logger.error(f"AGENDADOR: Erro crítico ao executar a tarefa de sinal agendado: {e}")
        
        await asyncio.sleep(60)

# --- 8. HANDLERS DE COMANDOS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(TEXT.BOAS_VINDAS_DM.format(link_cadastro=CONFIG.URL_CADASTRO), parse_mode=ParseMode.MARKDOWN)
    else:
        user_name = update.effective_user.first_name
        await update.message.reply_text(TEXT.BOAS_VINDAS_PUBLICO.format(user_name=user_name), parse_mode=ParseMode.MARKDOWN)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = StatsManager(context.bot_data)
    uptime = datetime.now() - stats.data.get('start_time', datetime.now())
    msg = f"📊 **ESTATÍSTICAS GERAIS** 📊\n\nUptime do Bot: {str(uptime).split('.')[0]}\n"
    for ch in ['free', 'vip']:
        wins, losses = stats.get_daily_score(ch)
        total_sinais = stats.data.get(f'daily_sinais_{ch}', 0)
        assertividade = ((wins / total_sinais) * 100) if total_sinais > 0 else 0
        msg += f"\n--- Placar Diário ({ch.upper()}) ---\n"
        msg += f"✅ Greens: {wins}\n"
        msg += f"❌ Reds: {losses}\n"
        msg += f"📈 Sinais Enviados: {total_sinais}\n"
        msg += f"🎯 Assertividade: {assertividade:.2f}%\n"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = StatsManager(context.bot_data)
    wins, losses = stats.get_daily_score("free")
    msg = TEXT.PLACA_DIA_TEMPLATE.format(wins=wins, losses=losses)
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != CONFIG.ADMIN_ID:
        await update.message.reply_text("❌ Você não tem permissão.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /sinal <jogo> <free|vip>")
        return
    game_arg, ch_type = context.args[0], context.args[1].lower()
    game = GAME_MANAGER.get_game_by_short_name(game_arg)
    if not game:
        await update.message.reply_text("Jogo inválido. Opções: bacbo, roleta, aviator, mines, fortune")
        return
    if ch_type not in ["free", "vip"]:
        await update.message.reply_text("Canal inválido (use free ou vip).")
        return
    await send_signal(context, game.name, ch_type)

# [NOVO COMANDO ADICIONADO POR MANUS]
async def autosinal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Liga ou desliga o envio automático de sinais (somente admin)."""
    if update.effective_user.id != CONFIG.ADMIN_ID:
        await update.message.reply_text("❌ Apenas o administrador pode usar este comando.")
        return

    # O estado é salvo em context.bot_data para persistir entre reinicializações
    # O padrão é 'True' (ligado) se nunca foi definido antes.
    is_enabled = context.bot_data.get('autosinal_enabled', True)
    
    # Inverte o estado atual (se estava ligado, desliga, e vice-versa)
    new_state = not is_enabled
    context.bot_data['autosinal_enabled'] = new_state

    status_text = "✅ LIGADO" if new_state else "❌ DESLIGADO"
    await update.message.reply_text(f"🤖 O envio automático de sinais foi definido como: **{status_text}**.", parse_mode=ParseMode.MARKDOWN)
    logger.info(f"ADMIN: O status do autosinal foi alterado para {status_text} pelo usuário {update.effective_user.id}")

# --- 9. HANDLER NOVOS MEMBROS ---
async def new_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(TEXT.BOAS_VINDAS_PUBLICO.format(user_name=member.first_name), parse_mode=ParseMode.MARKDOWN)
        asyncio.create_task(dm_funnel_sequence(context, member.id))

# --- 10. HANDLER DE COMPROVANTES ---
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(TEXT.COMPROVANTE_RECEBIDO, parse_mode=ParseMode.MARKDOWN)
    if CONFIG.ADMIN_ID != 0:
        caption = TEXT.COMPROVANTE_PARA_ADMIN.format(user_id=user.id, user_name=user.full_name)
        file_id = update.message.photo[-1].file_id
        await context.bot.send_photo(chat_id=CONFIG.ADMIN_ID, photo=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN)

# --- 11. EXECUÇÃO PRINCIPAL ---
# [SEÇÃO ATUALIZADA POR MANUS]
def main():
    if not _LIBRARIES_AVAILABLE:
        logger.critical("Dependências não disponíveis. Encerrando.")
        return

    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = Application.builder().token(CONFIG.BOT_TOKEN).persistence(persistence).build()

    # Registrando todos os comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("placar", score_command))
    app.add_handler(CommandHandler("sinal", signal_command))
    app.add_handler(CommandHandler("autosinal", autosinal_command)) # <-- NOVO HANDLER ADICIONADO

    # Registrando outros handlers
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    # Inicia o agendador de tarefas em uma thread separada para não bloquear o bot
    threading.Thread(target=lambda: asyncio.run(scheduled_tasks(app)), daemon=True).start()
    
    logger.info("Bot iniciado e pronto para receber comandos.")
    app.run_polling()

# --- 12. FLASK HEALTHCHECK ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Bot está rodando!"

if __name__ == "__main__":
    main()
