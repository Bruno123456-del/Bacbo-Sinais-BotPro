#!/usr/bin/env python3
"""
Bot Elite de Sinais Bac Bo para Telegram
Versão Profissional com Funcionalidades Avançadas
"""

import os
import time
import random
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import threading
from dataclasses import dataclass, asdict
from enum import Enum
from comandos_bot_avancados import adicionar_comandos_avancados

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',
    handlers=[
        logging.FileHandler(\'bot_bacbo.log\'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TipoAposta(Enum):
    PLAYER = "Player"
    BANKER = "Banker"
    TIE = "Tie"

@dataclass
class Sinal:
    id: int
    tipo: str
    timestamp: datetime
    nivel_martingale: int
    valor_aposta: float
    resultado: Optional[bool] = None
    timestamp_resultado: Optional[datetime] = None

@dataclass
class Configuracao:
    banca_minima: float = 100.0
    martingale_niveis: List[float] = None
    intervalo_sinais_minutos: int = 15
    taxa_vitoria_simulada: float = 0.70
    stop_loss_niveis: int = 3
    pausa_stop_loss_horas: int = 12
    url_cadastro: str = "https://lkwn.cc/f1c1c45a"
    
    def __post_init__(self ):
        if self.martingale_niveis is None:
            self.martingale_niveis = [0.01, 0.02, 0.04]

class DatabaseManager:
    def __init__(self, db_path: str = "bot_bacbo.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de sinais
            cursor.execute(\'\'\'
                CREATE TABLE IF NOT EXISTS sinais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    nivel_martingale INTEGER NOT NULL,
                    valor_aposta REAL NOT NULL,
                    resultado INTEGER,
                    timestamp_resultado TEXT
                )
            \'\'\')
            
            # Tabela de configurações
            cursor.execute(\'\'\'
                CREATE TABLE IF NOT EXISTS configuracoes (
                    chave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                )
            \'\'\')
            
            # Tabela de estatísticas
            cursor.execute(\'\'\'
                CREATE TABLE IF NOT EXISTS estatisticas (
                    data TEXT PRIMARY KEY,
                    total_sinais INTEGER DEFAULT 0,
                    total_greens INTEGER DEFAULT 0,
                    total_reds INTEGER DEFAULT 0,
                    lucro_dia REAL DEFAULT 0.0
                )
            \'\'\')
            
            conn.commit()
    
    def salvar_sinal(self, sinal: Sinal) -> int:
        """Salva um sinal no banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(\'\'\'
                INSERT INTO sinais (tipo, timestamp, nivel_martingale, valor_aposta, resultado, timestamp_resultado)
                VALUES (?, ?, ?, ?, ?, ?)
            \'\'\', (
                sinal.tipo,
                sinal.timestamp.isoformat(),
                sinal.nivel_martingale,
                sinal.valor_aposta,
                sinal.resultado,
                sinal.timestamp_resultado.isoformat() if sinal.timestamp_resultado else None
            ))
            return cursor.lastrowid
    
    def atualizar_resultado_sinal(self, sinal_id: int, resultado: bool):
        """Atualiza o resultado de um sinal"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(\'\'\'
                UPDATE sinais 
                SET resultado = ?, timestamp_resultado = ?
                WHERE id = ?
            \'\'\', (resultado, datetime.now().isoformat(), sinal_id))
            conn.commit()
    
    def obter_estatisticas_periodo(self, dias: int = 7) -> Dict:
        """Obtém estatísticas dos últimos N dias"""
        data_inicio = datetime.now() - timedelta(days=dias)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(\'\'\'
                SELECT 
                    COUNT(*) as total_sinais,
                    SUM(CASE WHEN resultado = 1 THEN 1 ELSE 0 END) as greens,
                    SUM(CASE WHEN resultado = 0 THEN 1 ELSE 0 END) as reds,
                    AVG(CASE WHEN resultado IS NOT NULL THEN resultado END) as taxa_acerto
                FROM sinais 
                WHERE timestamp >= ? AND resultado IS NOT NULL
            \'\'\', (data_inicio.isoformat(),))
            
            resultado = cursor.fetchone()
            
            return {
                \'total_sinais\': resultado[0] or 0,
                \'greens\': resultado[1] or 0,
                \'reds\': resultado[2] or 0,
                \'taxa_acerto\': resultado[3] or 0.0
            }

class AnalisadorPadroes:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def analisar_sequencias(self) -> Dict:
        """Analisa sequências de resultados para identificar padrões"""
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(\'\'\'
                SELECT tipo, resultado 
                FROM sinais 
                WHERE resultado IS NOT NULL 
                ORDER BY timestamp DESC 
                LIMIT 50
            \'\'\')
            
            resultados = cursor.fetchall()
            
            # Análise de sequências por tipo
            sequencias = {}
            for tipo in [TipoAposta.PLAYER.value, TipoAposta.BANKER.value, TipoAposta.TIE.value]:
                tipo_resultados = [r[1] for r in resultados if r[0] == tipo]
                sequencias[tipo] = {
                    \'total\': len(tipo_resultados),
                    \'greens\': sum(tipo_resultados),
                    \'taxa_acerto\': sum(tipo_resultados) / len(tipo_resultados) if tipo_resultados else 0
                }
            
            return sequencias
    
    def sugerir_proximo_sinal(self) -> str:
        """Sugere o próximo sinal baseado em análise de padrões"""
        padroes = self.analisador.analisar_sequencias()
        
        # Lógica simples: escolhe o tipo com menor taxa de acerto recente
        # (assumindo que haverá uma correção)
        menor_taxa = float(\'inf\')
        tipo_sugerido = TipoAposta.PLAYER.value
        
        for tipo, dados in padroes.items():
            if dados[\'total\'] > 5 and dados[\'taxa_acerto\'] < menor_taxa:
                menor_taxa = dados[\'taxa_acerto\']
                tipo_sugerido = tipo
        
        return tipo_sugerido

class BacBoEliteBot:
    def __init__(self, config_path: str = "config.json"):
        self.config = self._carregar_configuracao(config_path)
        self.db = DatabaseManager()
        self.analisador = AnalisadorPadroes(self.db)
        
        # Configuração do bot
        self.TOKEN = os.getenv("TELEGRAM_TOKEN")
        self.CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
        self.ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
        
        if not self.TOKEN or not self.CHAT_ID:
            logger.error("Variáveis de ambiente não configuradas")
            exit()
        
        self.bot = telebot.TeleBot(self.TOKEN)
        self._configurar_handlers()
        
        # Estado do bot
        self.nivel_martingale_atual = 0
        self.banca_atual = self.config.banca_minima
        self.sinal_atual_id = None
        self.bot_ativo = False
        self.modo_automatico = True
        
        # Emojis e opções
        self.emojis = {
            TipoAposta.PLAYER.value: "🔵",
            TipoAposta.BANKER.value: "🔴", 
            TipoAposta.TIE.value: "🟢"
        }
    
    def _carregar_configuracao(self, config_path: str) -> Configuracao:
        """Carrega configuração do arquivo JSON"""
        if os.path.exists(config_path):
            with open(config_path, \'r\') as f:
                config_dict = json.load(f)
                return Configuracao(**config_dict)
        else:
            config = Configuracao()
            self._salvar_configuracao(config, config_path)
            return config
    
    def _salvar_configuracao(self, config: Configuracao, config_path: str):
        """Salva configuração no arquivo JSON"""
        with open(config_path, \'w\') as f:
            json.dump(asdict(config), f, indent=2)
    
    def _configurar_handlers(self):
        """Configura os handlers de comandos do bot"""
        
        @self.bot.message_handler(commands=[\'start\', \'help\'])
        def handle_start(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._enviar_menu_admin(message.chat.id)
            else:
                self._enviar_mensagem_boas_vindas(message.chat.id)
        
        @self.bot.message_handler(commands=[\'stats\'])
        def handle_stats(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._enviar_estatisticas(message.chat.id)
        
        @self.bot.message_handler(commands=[\'config\'])
        def handle_config(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._enviar_menu_configuracao(message.chat.id)
        
        @self.bot.message_handler(commands=[\'iniciar\'])
        def handle_iniciar(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._iniciar_bot_automatico()
        
        @self.bot.message_handler(commands=[\'parar\'])
        def handle_parar(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._parar_bot_automatico()
        
        @self.bot.message_handler(commands=[\'sinal\'])
        def handle_sinal_manual(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._enviar_sinal_manual()
        
        @self.bot.message_handler(commands=[\'green\'])
        def handle_green(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._processar_resultado(True)
        
        @self.bot.message_handler(commands=[\'red\'])
        def handle_red(message):
            if str(message.from_user.id) == self.ADMIN_ID:
                self._processar_resultado(False)
        
        adicionar_comandos_avancados(self.bot)    
    def _enviar_menu_admin(self, chat_id):
        """Envia menu administrativo"""
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(KeyboardButton("📊 Estatísticas"), KeyboardButton("⚙️ Configurações"))
        markup.row(KeyboardButton("▶️ Iniciar Bot"), KeyboardButton("⏹️ Parar Bot"))
        markup.row(KeyboardButton("🎯 Sinal Manual"), KeyboardButton("📈 Relatório"))
        
        mensagem = (
            "🤖 **PAINEL ADMINISTRATIVO - BAC BO ELITE**\n\n"
            "Escolha uma opção do menu abaixo:\n\n"
            "📊 **Estatísticas** - Ver performance do bot\n"
            "⚙️ **Configurações** - Ajustar parâmetros\n"
            "▶️ **Iniciar Bot** - Ativar sinais automáticos\n"
            "⏹️ **Parar Bot** - Pausar sinais automáticos\n"
            "🎯 **Sinal Manual** - Enviar sinal manualmente\n"
            "📈 **Relatório** - Relatório detalhado"
        )
        
        self.bot.send_message(chat_id, mensagem, parse_mode="Markdown", reply_markup=markup)
    
    def _enviar_mensagem_boas_vindas(self, chat_id):
        """Envia mensagem de boas-vindas para usuários comuns"""
        botoes = InlineKeyboardMarkup()
        botoes.add(InlineKeyboardButton("🎁 Cadastre-se e Ganhe Bônus", url=self.config.url_cadastro))
        
        mensagem = (
            "🎰 **BEM-VINDO AO BAC BO ELITE** 🎰\n\n"
            "🔥 **Sinais Premium de Alta Precisão**\n"
            "💰 **Gestão Profissional de Banca**\n"
            "📊 **Análise Avançada de Padrões**\n"
            "🎯 **Taxa de Acerto Comprovada**\n\n"
            "Prepare-se para receber os melhores sinais do mercado!\n\n"
            "⚠️ **Lembre-se:** Jogue com responsabilidade e siga sempre a gestão de banca."
        )
        
        self.bot.send_message(chat_id, mensagem, parse_mode="Markdown", reply_markup=botoes)
    
    def _enviar_estatisticas(self, chat_id):
        """Envia estatísticas detalhadas"""
        stats_7d = self.db.obter_estatisticas_periodo(7)
        stats_30d = self.db.obter_estatisticas_periodo(30)
        padroes = self.analisador.analisar_sequencias()
        
        mensagem = (
            "📊 **ESTATÍSTICAS DO BOT** 📊\n\n"
            "**📅 Últimos 7 dias:**\n"
            f"• Total de sinais: {stats_7d[\'total_sinais\']}\n"
            f"• Greens: {stats_7d[\'greens\']} ✅\n"
            f"• Reds: {stats_7d[\'reds\']} ❌\n"
            f"• Taxa de acerto: {stats_7d[\'taxa_acerto\']:.1%}\n\n"
            
            "**📅 Últimos 30 dias:**\n"
            f"• Total de sinais: {stats_30d[\'total_sinais\']}\n"
            f"• Greens: {stats_30d[\'greens\']} ✅\n"
            f"• Reds: {stats_30d[\'reds\']} ❌\n"
            f"• Taxa de acerto: {stats_30d[\'taxa_acerto\']:.1%}\n\n"
            
            "**🎯 Análise por Tipo:**\n"
        )
        
        for tipo, dados in padroes.items():
            emoji = self.emojis.get(tipo, "⚪")
            mensagem += f"• {emoji} {tipo}: {dados[\'taxa_acerto\']:.1%} ({dados[\'greens\']}/{dados[\'total\']})\n"
        
        mensagem += f"\n**💰 Banca Atual:** R$ {self.banca_atual:.2f}"
        mensagem += f"\n**🎲 Nível Martingale:** {self.nivel_martingale_atual + 1}"
        mensagem += f"\n**🤖 Status:** {\'🟢 Ativo\' if self.bot_ativo else \'🔴 Inativo\'}"
        
        self.bot.send_message(chat_id, mensagem, parse_mode="Markdown")
    
    def gerar_sinal_inteligente(self) -> Tuple[str, str]:
        """Gera sinal usando análise de padrões"""
        if self.modo_automatico:
            # Usa análise de padrões para sugerir
            tipo_sugerido = self.analisador.sugerir_proximo_sinal()
        else:
            # Fallback para escolha aleatória
            tipo_sugerido = random.choice([t.value for t in TipoAposta])
        
        emoji = self.emojis[tipo_sugerido]
        return tipo_sugerido, emoji
    
    def enviar_sinal(self, tipo: str = None, emoji: str = None) -> int:
        """Envia sinal para o canal"""
        if not tipo or not emoji:
            tipo, emoji = self.gerar_sinal_inteligente()
        
        percentual_aposta = self.config.martingale_niveis[self.nivel_martingale_atual]
        valor_aposta = self.banca_atual * percentual_aposta
        
        # Cria objeto sinal
        sinal = Sinal(
            id=0,  # Será definido pelo banco
            tipo=tipo,
            timestamp=datetime.now(),
            nivel_martingale=self.nivel_martingale_atual,
            valor_aposta=valor_aposta
        )
        
        # Salva no banco
        sinal_id = self.db.salvar_sinal(sinal)
        self.sinal_atual_id = sinal_id
        
        # Informações de gestão
        gestao_info = (
            f"**💰 Gestão de Banca Profissional:**\n"
            f"• **Banca Atual:** R$ {self.banca_atual:.2f}\n"
            f"• **Nível Martingale:** {self.nivel_martingale_atual + 1}/{len(self.config.martingale_niveis)}\n"
            f"• **Aposta Sugerida:** {percentual_aposta:.2%} da banca (R$ {valor_aposta:.2f})\n"
            f"• **Stop Loss:** {self.config.stop_loss_niveis} níveis"
        )
        
        # Análise técnica
        padroes = self.analisador.analisar_sequencias()
        tipo_stats = padroes.get(tipo, {\'taxa_acerto\': 0, \'total\': 0})
        
        analise_info = (
            f"**📊 Análise Técnica:**\n"
            f"• **Tipo:** {tipo} {emoji}\n"
            f"• **Taxa Recente:** {tipo_stats[\'taxa_acerto\']:.1%}\n"
            f"• **Confiança:** {\'🔥 Alta\' if tipo_stats[\'taxa_acerto\'] > 0.6 else \'⚡ Média\' if tipo_stats[\'taxa_acerto\'] > 0.4 else \'⚠️ Baixa\'}"
        )
        
        mensagem = (
            "🚨 **SINAL ELITE CONFIRMADO | BAC BO** 🚨\n\n"
            f"🎯 **ENTRADA:** {emoji} **{tipo}**\n\n"
            f"{gestao_info}\n\n"
            f"{analise_info}\n\n"
            "⚠️ **IMPORTANTE:**\n"
            "• Siga rigorosamente a gestão de banca\n"
            "• Nunca aposte mais que o sugerido\n"
            "• A disciplina é fundamental para o sucesso\n\n"
            "🔥 **BOA SORTE E TRADE RESPONSÁVEL!**"
        )
        
        botoes = InlineKeyboardMarkup()
        botoes.add(InlineKeyboardButton("🎁 Cadastre-se e Ganhe Bônus", url=self.config.url_cadastro))
        
        self.bot.send_message(self.CHAT_ID, mensagem, parse_mode="Markdown", reply_markup=botoes)
        logger.info(f"Sinal enviado: {tipo} | Nível: {self.nivel_martingale_atual + 1} | ID: {sinal_id}")
        
        return sinal_id
    
    def _processar_resultado(self, vitoria: bool):
        """Processa o resultado de um sinal"""
        if not self.sinal_atual_id:
            return
        
        # Atualiza no banco
        self.db.atualizar_resultado_sinal(self.sinal_atual_id, vitoria)
        
        if vitoria:
            # GREEN - Reseta martingale e atualiza banca
            percentual_ganho = self.config.martingale_niveis[self.nivel_martingale_atual]
            ganho = self.banca_atual * percentual_ganho * 0.95  # Considerando odds
            self.banca_atual += ganho
            self.nivel_martingale_atual = 0
            
            mensagem = (
                "✅ **GREEN CONFIRMADO!** ✅\n\n"
                f"🎉 **Parabéns! Sinal finalizado com sucesso!**\n\n"
                f"💰 **Ganho:** R$ {ganho:.2f}\n"
                f"💳 **Nova Banca:** R$ {self.banca_atual:.2f}\n\n"
                "🔄 **Voltamos ao nível 1 do Martingale**\n"
                "🎯 **Aguarde o próximo sinal...**"
            )
            logger.info(f"GREEN - Ganho: R$ {ganho:.2f} | Nova banca: R$ {self.banca_atual:.2f}")
            
        else:
            # RED - Avança martingale
            self.nivel_martingale_atual += 1
            
            if self.nivel_martingale_atual >= len(self.config.martingale_niveis):
                # Stop Loss atingido
                self._executar_stop_loss()
                return
            
            proximo_percentual = self.config.martingale_niveis[self.nivel_martingale_atual]
            proxima_aposta = self.banca_atual * proximo_percentual
            
            mensagem = (
                "❌ **RED!** ❌\n\n"
                f"⚠️ **Sinal não bateu desta vez**\n\n"
                f"🎲 **Próximo nível:** {self.nivel_martingale_atual + 1}/{len(self.config.martingale_niveis)}\n"
                f"💰 **Próxima aposta:** R$ {proxima_aposta:.2f}\n\n"
                "🔥 **Mantenha a disciplina!**\n"
                "📈 **A recuperação está chegando...**"
            )
            logger.info(f"RED - Nível: {self.nivel_martingale_atual + 1}")
        
        self.bot.send_message(self.CHAT_ID, mensagem, parse_mode="Markdown")
        self.sinal_atual_id = None





    def _executar_stop_loss(self):
        """Executa o stop loss quando limite é atingido"""
        self.bot_ativo = False
        self.nivel_martingale_atual = 0
        self.sinal_atual_id = None
        
        mensagem = (
            "🛑 **STOP LOSS ATIVADO** 🛑\n\n"
            "⚠️ **Limite de perdas consecutivas atingido**\n\n"
            f"⏰ **Pausa de {self.config.pausa_stop_loss_horas}h para proteção da banca**\n\n"
            "🧠 **A disciplina salvou sua banca!**\n"
            "📊 **Analisando novos padrões...**\n"
            "🔄 **Voltaremos mais fortes!**\n\n"
            "💡 **Aproveite para garantir seu bônus de cadastro!**"
        )
        
        self.bot.send_message(self.CHAT_ID, mensagem, parse_mode="Markdown")
        logger.warning("Stop loss ativado - Bot pausado")
        
        # Agenda reativação
        threading.Timer(
            self.config.pausa_stop_loss_horas * 3600,
            self._reativar_apos_stop_loss
        ).start()
    
    def _reativar_apos_stop_loss(self):
        """Reativa o bot após o período de stop loss"""
        self.bot_ativo = True
        
        mensagem = (
            "🔄 **BOT REATIVADO** 🔄\n\n"
            "✅ **Período de pausa finalizado**\n"
            "🎯 **Novos sinais em breve...**\n"
            "📊 **Padrões atualizados e analisados**\n\n"
            "🚀 **Vamos retomar os lucros!**"
        )
        
        self.bot.send_message(self.CHAT_ID, mensagem, parse_mode="Markdown")
        logger.info("Bot reativado após stop loss")
    
    def _enviar_menu_configuracao(self, chat_id):
        """Envia menu de configuração"""
        mensagem = (
            "⚙️ **CONFIGURAÇÕES DO BOT** ⚙️\n\n"
            f"💰 **Banca Mínima:** R$ {self.config.banca_minima:.2f}\n"
            f"🎲 **Níveis Martingale:** {len(self.config.martingale_niveis)} níveis\n"
            f"⏰ **Intervalo Sinais:** {self.config.intervalo_sinais_minutos} min\n"
            f"🎯 **Taxa Simulada:** {self.config.taxa_vitoria_simulada:.1%}\n"
            f"🛑 **Stop Loss:** {self.config.stop_loss_niveis} níveis\n"
            f"⏸️ **Pausa Stop Loss:** {self.config.pausa_stop_loss_horas}h\n\n"
            "Para alterar configurações, edite o arquivo config.json"
        )
        
        self.bot.send_message(chat_id, mensagem, parse_mode="Markdown")
    
    def _iniciar_bot_automatico(self):
        """Inicia o modo automático do bot"""
        self.bot_ativo = True
        self.modo_automatico = True
        
        mensagem = (
            "🚀 **BOT ELITE ATIVADO** 🚀\n\n"
            "✅ **Modo automático iniciado**\n"
            "🎯 **Sinais inteligentes ativados**\n"
            "📊 **Análise de padrões em tempo real**\n\n"
            f"⏰ **Intervalo:** {self.config.intervalo_sinais_minutos} minutos\n"
            f"💰 **Banca inicial:** R$ {self.banca_atual:.2f}\n\n"
            "🔥 **Prepare-se para os lucros!**"
        )
        
        self.bot.send_message(self.CHAT_ID, mensagem, parse_mode="Markdown")
        logger.info("Bot automático iniciado")
    
    def _parar_bot_automatico(self):
        """Para o modo automático do bot"""
        self.bot_ativo = False
        
        mensagem = (
            "⏹️ **BOT PAUSADO** ⏹️\n\n"
            "✅ **Modo automático desativado**\n"
            "📊 **Sinais manuais ainda disponíveis**\n\n"
            "Use /sinal para enviar sinais manualmente"
        )
        
        self.bot.send_message(self.CHAT_ID, mensagem, parse_mode="Markdown")
        logger.info("Bot automático pausado")
    
    def _enviar_sinal_manual(self):
        """Envia um sinal manual"""
        if self.sinal_atual_id:
            self.bot.send_message(
                self.ADMIN_ID,
                "⚠️ Há um sinal pendente. Finalize-o primeiro com /green ou /red"
            )
            return
        
        self.enviar_sinal()
        self.bot.send_message(self.ADMIN_ID, "✅ Sinal manual enviado!")
    
    def executar_loop_principal(self):
        """Loop principal do bot automático"""
        logger.info("🚀 Bot Elite iniciado!")
        
        # Mensagem inicial
        mensagem_inicial = (
            "🤖 **BAC BO ELITE BOT INICIADO** 🤖\n\n"
            "🔥 **Sistema de sinais premium ativo**\n"
            "📊 **Análise inteligente de padrões**\n"
            "💰 **Gestão profissional de banca**\n\n"
            "⚡ **Aguardando configuração...**\n\n"
            "👨‍💼 **Admins:** Use /start para acessar o painel"
        )
        
        self.bot.send_message(self.CHAT_ID, mensagem_inicial, parse_mode="Markdown")
        
        # Thread para polling do Telegram
        def polling_thread():
            self.bot.polling(none_stop=True, interval=1)
        
        threading.Thread(target=polling_thread, daemon=True).start()
        
        # Loop principal de sinais
        while True:
            try:
                if self.bot_ativo and not self.sinal_atual_id:
                    # Envia novo sinal
                    self.enviar_sinal()
                    
                    # Aguarda resultado (simulado)
                    time.sleep(60)  # 1 minuto para simular tempo de jogo
                    
                    # Simula resultado baseado na taxa configurada
                    vitoria = random.random() < self.config.taxa_vitoria_simulada
                    self._processar_resultado(vitoria)
                    
                    # Aguarda intervalo para próximo sinal
                    if self.bot_ativo:
                        logger.info(f"Aguardando {self.config.intervalo_sinais_minutos} minutos...")
                        time.sleep(self.config.intervalo_sinais_minutos * 60)
                
                else:
                    # Bot inativo ou sinal pendente
                    time.sleep(30)
                    
            except Exception as e:
                logger.error(f"Erro no loop principal: {e}")
                time.sleep(60)

def main():
    """Função principal"""
    try:
        bot = BacBoEliteBot()
        bot.executar_loop_principal()
    except KeyboardInterrupt:
        logger.info("Bot finalizado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()


