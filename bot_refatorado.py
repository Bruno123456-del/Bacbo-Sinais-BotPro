import os
import asyncio
import random
import logging
from typing import Optional
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest, TelegramError

from config import Config
from messages import Messages
from strategy import EscadaAsiaticaStrategy, GestaoRisco

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BacBoBotRefatorado:
    """
    Bot do Telegram para sinais de Bac Bo com estratégia Escada Asiática.
    Versão refatorada com melhor organização e tratamento de erros.
    """
    
    def __init__(self):
        self.config = Config()
        self.config.validate()
        
        self.messages = Messages(self.config.URL_CADASTRO)
        self.strategy = EscadaAsiaticaStrategy()
        self.gestao_risco = GestaoRisco(
            self.config.CHANCE_WIN_ENTRADA_INICIAL,
            self.config.CHANCE_WIN_GALE_1,
            self.config.CHANCE_WIN_GALE_2
        )
        
        self.placar = {"greens": 0, "reds": 0}
        self.historico_wins = []  # Para ajuste dinâmico das probabilidades
        
    async def simular_e_enviar_sinal(self, bot: Bot) -> None:
        """
        Simula e envia um sinal baseado na estratégia Escada Asiática.
        
        Args:
            bot: Instância do bot do Telegram
        """
        try:
            # Em produção, substituir por dados reais da API
            historico = self.strategy.get_historico_para_teste()
            sinal = self.strategy.analisar_historico(historico)
            
            if not sinal:
                logger.info("Nenhuma oportunidade detectada.")
                return

            # Envia GIF de análise
            msg_analise = await bot.send_animation(
                chat_id=self.config.CHAT_ID, 
                animation=self.config.GIF_ANALISE, 
                caption="⏳ Analisando com IA..."
            )
            
            await asyncio.sleep(self.config.TEMPO_ANALISE)

            # Prepara teclado inline
            botao_plataforma = InlineKeyboardButton(
                text="💎 ENTRAR NA PLATAFORMA 💎", 
                url=self.config.URL_CADASTRO
            )
            teclado_sinal = InlineKeyboardMarkup([[botao_plataforma]])

            # Envia sinal
            mensagem_sinal = self.messages.get_mensagem_sinal(sinal)
            
            await msg_analise.delete()
            await bot.send_message(
                chat_id=self.config.CHAT_ID, 
                text=mensagem_sinal, 
                reply_markup=teclado_sinal
            )

            # Simula resultado da operação
            await self._processar_resultado_operacao(bot)
            
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao enviar sinal: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar sinal: {e}")

    async def _processar_resultado_operacao(self, bot: Bot) -> None:
        """
        Processa o resultado da operação (entrada, gale1, gale2).
        
        Args:
            bot: Instância do bot do Telegram
        """
        await asyncio.sleep(self.config.TEMPO_ENTRADA)

        # Tenta entrada principal
        if self.gestao_risco.simular_resultado_entrada():
            await self._processar_win(bot, "entrada")
            return

        # Primeiro Gale
        await bot.send_message(chat_id=self.config.CHAT_ID, text="⚠️ Ativando GALE 1.")
        await asyncio.sleep(self.config.TEMPO_GALE)
        
        if self.gestao_risco.simular_resultado_gale1():
            await self._processar_win(bot, "gale1")
            return

        # Segundo Gale
        await bot.send_message(chat_id=self.config.CHAT_ID, text="⚠️ Ativando GALE 2.")
        await asyncio.sleep(self.config.TEMPO_GALE)
        
        if self.gestao_risco.simular_resultado_gale2():
            await self._processar_win(bot, "gale2")
        else:
            await self._processar_loss(bot)

    async def _processar_win(self, bot: Bot, tipo: str) -> None:
        """
        Processa um resultado de vitória.
        
        Args:
            bot: Instância do bot do Telegram
            tipo: Tipo de win ('entrada', 'gale1', 'gale2')
        """
        try:
            self.placar["greens"] += 1
            self.historico_wins.append(True)
            
            # Envia GIF de vitória
            await bot.send_animation(chat_id=self.config.CHAT_ID, animation=self.config.GIF_WIN)
            await asyncio.sleep(2)
            
            # Envia imagem correspondente
            captions = self.messages.get_captions_win()
            imagem_path = getattr(self.config, f"IMG_WIN_{tipo.upper()}")
            
            if os.path.exists(imagem_path):
                with open(imagem_path, 'rb') as img:
                    await bot.send_photo(
                        chat_id=self.config.CHAT_ID, 
                        photo=img, 
                        caption=captions[tipo]
                    )
            else:
                logger.warning(f"Imagem não encontrada: {imagem_path}")
                await bot.send_message(
                    chat_id=self.config.CHAT_ID, 
                    text=captions[tipo]
                )
            
            # Envia mensagem de reforço
            reforcos = self.messages.get_reforco_pos_win()
            await bot.send_message(
                chat_id=self.config.CHAT_ID, 
                text=random.choice(reforcos), 
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro ao processar win: {e}")

    async def _processar_loss(self, bot: Bot) -> None:
        """
        Processa um resultado de perda.
        
        Args:
            bot: Instância do bot do Telegram
        """
        try:
            self.placar["reds"] += 1
            self.historico_wins.append(False)
            
            captions = self.messages.get_captions_win()
            await bot.send_animation(
                chat_id=self.config.CHAT_ID, 
                animation=self.config.GIF_RED, 
                caption=captions["stop_loss"]
            )
            
        except Exception as e:
            logger.error(f"Erro ao processar loss: {e}")

    async def ciclo_de_sinais(self, bot: Bot) -> None:
        """
        Executa o ciclo principal de envio de sinais.
        
        Args:
            bot: Instância do bot do Telegram
        """
        sinais_enviados = 0
        
        while True:
            try:
                await self.simular_e_enviar_sinal(bot)
                sinais_enviados += 1

                # A cada 3 sinais, envia placar e prova social
                if sinais_enviados % 3 == 0:
                    await self._enviar_placar_e_prova_social(bot)
                    
                    # Ajusta probabilidades baseado no histórico recente
                    if len(self.historico_wins) >= 10:
                        self.gestao_risco.ajustar_probabilidades(self.historico_wins[-10:])

                await asyncio.sleep(self.config.INTERVALO_SINAIS)
                
            except Exception as e:
                logger.error(f"Erro no ciclo de sinais: {e}")
                await asyncio.sleep(60)  # Espera 1 minuto antes de tentar novamente

    async def _enviar_placar_e_prova_social(self, bot: Bot) -> None:
        """
        Envia o placar atual e uma prova social.
        
        Args:
            bot: Instância do bot do Telegram
        """
        try:
            # Envia placar
            mensagem_placar = self.messages.get_mensagem_placar(
                self.placar['greens'], 
                self.placar['reds']
            )
            await bot.send_message(
                chat_id=self.config.CHAT_ID, 
                text=mensagem_placar, 
                parse_mode='Markdown'
            )
            
            # Envia prova social
            imagem = random.choice(self.config.PROVAS_SOCIAIS)
            textos = self.messages.get_textos_prova_social()
            texto = random.choice(textos)
            
            if os.path.exists(imagem):
                with open(imagem, 'rb') as img:
                    await bot.send_photo(
                        chat_id=self.config.CHAT_ID, 
                        photo=img, 
                        caption=texto
                    )
            else:
                logger.warning(f"Prova social não encontrada: {imagem}")
                
        except Exception as e:
            logger.error(f"Erro ao enviar placar e prova social: {e}")

    async def gestao(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handler para o comando /gestao.
        
        Args:
            update: Update do Telegram
            context: Contexto do comando
        """
        try:
            await update.message.reply_text(
                "📊 **Protocolo de Gestão Avançada**\n\n"
                f"✅ Greens: {self.placar['greens']}\n"
                f"❌ Reds: {self.placar['reds']}\n"
                f"📈 Taxa de Acerto: {self._calcular_taxa_acerto():.1%}\n\n"
                "💡 Mantenha a disciplina e siga sempre a gestão de risco.",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erro no comando gestao: {e}")

    def _calcular_taxa_acerto(self) -> float:
        """
        Calcula a taxa de acerto atual.
        
        Returns:
            Taxa de acerto como float entre 0 e 1
        """
        total = self.placar['greens'] + self.placar['reds']
        if total == 0:
            return 0.0
        return self.placar['greens'] / total

    async def enviar_e_fixar_mensagem_inicial(self, bot: Bot) -> None:
        """
        Envia e fixa a mensagem inicial do grupo.
        
        Args:
            bot: Instância do bot do Telegram
        """
        try:
            mensagem = self.messages.get_mensagem_fixada()
            msg = await bot.send_message(
                chat_id=self.config.CHAT_ID, 
                text=mensagem, 
                parse_mode='Markdown'
            )
            await bot.pin_chat_message(
                chat_id=self.config.CHAT_ID, 
                message_id=msg.message_id
            )
            logger.info("Mensagem inicial enviada e fixada com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao fixar mensagem inicial: {e}")

    async def enviar_mensagem_recorrente(self, bot: Bot) -> None:
        """
        Envia mensagens recorrentes de lembrete.
        
        Args:
            bot: Instância do bot do Telegram
        """
        while True:
            try:
                await asyncio.sleep(self.config.INTERVALO_MENSAGEM_RECORRENTE)
                mensagem = self.messages.get_mensagem_automatica_recorrente()
                await bot.send_message(
                    chat_id=self.config.CHAT_ID, 
                    text=mensagem, 
                    parse_mode='Markdown'
                )
                logger.info("Mensagem recorrente enviada")
                
            except Exception as e:
                logger.error(f"Erro ao enviar mensagem recorrente: {e}")
                await asyncio.sleep(300)  # Espera 5 minutos antes de tentar novamente

    async def run(self) -> None:
        """
        Executa o bot principal.
        """
        try:
            logger.info("Iniciando Bot BAC BO com estratégia Escada Asiática...")
            
            application = Application.builder().token(self.config.BOT_TOKEN).build()
            application.add_handler(CommandHandler("gestao", self.gestao))
            
            await application.initialize()
            await application.start()
            await application.updater.start_polling()

            bot = application.bot
            
            # Inicia tarefas assíncronas
            asyncio.create_task(self.enviar_e_fixar_mensagem_inicial(bot))
            asyncio.create_task(self.ciclo_de_sinais(bot))
            asyncio.create_task(self.enviar_mensagem_recorrente(bot))

            logger.info("Bot iniciado com sucesso. Pressione Ctrl+C para parar.")
            
            # Loop principal
            while True:
                await asyncio.sleep(3600)
                
        except Exception as e:
            logger.error(f"Erro crítico no bot: {e}")
            raise

if __name__ == '__main__':
    bot_instance = BacBoBotRefatorado()
    try:
        asyncio.run(bot_instance.run())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot finalizado pelo usuário.")
    except Exception as e:
        logger.error(f"Bot finalizado com erro: {e}")

