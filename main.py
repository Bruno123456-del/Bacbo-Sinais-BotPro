#!/usr/bin/env python3
"""
Bot de Sinais BAC BO para Telegram
Desenvolvido para Square Cloud

Autor: Sistema Automatizado
Data: 2025
"""

import os
import sys
import asyncio
import logging
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.telegram_bot import TelegramSignalBot
from config.config import SIGNAL_INTERVAL_MINUTES, MAX_SIGNALS_PER_DAY

def setup_logging():
    """
    Configura o sistema de logging
    """
    # Cria diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # Configuração do logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

async def main():
    """
    Função principal do bot
    """
    print("🤖 Iniciando Bot de Sinais BAC BO...")
    print("=" * 50)
    
    # Configura logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Cria instância do bot
        bot = TelegramSignalBot()
        
        # Testa conexão
        logger.info("Testando conexão com Telegram...")
        if await bot.test_connection():
            logger.info("✅ Conexão estabelecida com sucesso!")
            print("✅ Conexão com Telegram estabelecida!")
            print(f"📊 Configurações:")
            print(f"   • Intervalo entre sinais: {SIGNAL_INTERVAL_MINUTES} minutos")
            print(f"   • Máximo de sinais por dia: {MAX_SIGNALS_PER_DAY}")
            print("🚀 Iniciando envio de sinais...")
            print("=" * 50)
            
            # Inicia o loop de sinais
            bot.start_signal_loop(
                interval_minutes=SIGNAL_INTERVAL_MINUTES,
                max_signals_per_day=MAX_SIGNALS_PER_DAY
            )
        else:
            logger.error("❌ Falha na conexão com Telegram!")
            print("❌ Erro na conexão com Telegram!")
            print("Verifique:")
            print("1. Token do bot está correto")
            print("2. Bot foi adicionado ao grupo/canal")
            print("3. Conexão com internet está funcionando")
            
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
        print("\n🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        print(f"❌ Erro crítico: {e}")
    finally:
        print("👋 Bot finalizado!")

if __name__ == "__main__":
    # Executa o bot
    asyncio.run(main())

