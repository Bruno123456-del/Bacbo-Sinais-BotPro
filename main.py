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
