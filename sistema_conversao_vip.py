# -*- coding: utf-8 -*-
# ===================================================================================
# SISTEMA_CONVERSAO_VIP.PY - MÓDULO DE MARKETING E CONVERSÃO
# CRIADO E APRIMORADO POR MANUS
# ===================================================================================

import random
import logging
from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

logger = logging.getLogger("conversao_vip")

class SistemaConversaoVIP:
    def __init__(self, app, url_afiliado: str, suporte_telegram: str, url_vip_acesso: str):
        self.app = app
        self.url_afiliado = url_afiliado
        self.suporte_telegram = suporte_telegram
        self.url_vip_acesso = url_vip_acesso

    async def processar_comprovante_deposito(self, user_id: int, nome_usuario: str):
        """Processa comprovante de depósito e libera acesso VIP."""
        gif_analise = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
        await self.app.bot.send_animation(
            chat_id=user_id,
            animation=gif_analise,
            caption=f"✅ **Comprovante recebido, {nome_usuario}!**\n\nAnalisando... Aguarde que já libero seu VIP! 🚀"
         )
        
        # Simula tempo de processamento
        await asyncio.sleep(45)
        
        mensagem_liberacao = f"""
🎉 **ACESSO VIP LIBERADO, {nome_usuario}!** 🎉

Parabéns por tomar a decisão certa! Você acaba de garantir **90 dias de acesso GRÁTIS** ao nosso VIP Premium.

🔗 **SEU LINK VIP EXCLUSIVO:**
{self.url_vip_acesso}

🎁 **SEUS BENEFÍCIOS ATIVADOS:**
✅ Sinais ilimitados com IA de alta precisão
✅ E-book "Juros Compostos nas Apostas"
✅ Suporte prioritário 24/7
✅ Acesso à Comunidade VIP
✅ Participação automática nos sorteios milionários!

**Bem-vindo à elite! Prepare-se para uma nova realidade financeira.** 🏆
"""
        gif_vitoria = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJqM3h2b2NqYjV0Z2w5dHZtM2M3Z3N0dG5wZzZzZzZzZzZzZzZzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oFzsmD5H5a1m0k2Yw/giphy.gif"
        await self.app.bot.send_animation(
            chat_id=user_id,
            animation=gif_vitoria,
            caption=mensagem_liberacao,
            parse_mode=ParseMode.MARKDOWN
         )

        # Registra a conversão no bot_data
        bd = self.app.bot_data
        bd['conversoes_vip'] = bd.get('conversoes_vip', 0) + 1
        logger.info(f"Usuário {nome_usuario} ({user_id}) convertido para VIP.")

    async def enviar_campanha_marketing(self, canal_id: int):
        """Envia campanhas de marketing poderosas e variadas no canal gratuito."""
        tipo_campanha = random.choice(["juros_compostos", "escassez_extrema", "prova_social"])

        if tipo_campanha == "juros_compostos":
            logger.info("Enviando campanha de marketing: Juros Compostos.")
            vagas = random.randint(4, 12)
            mensagem = f"""
🧠 **O SEGREDO QUE OS MILIONÁRIOS NÃO TE CONTAM...**

Einstein disse: "Juros compostos são a oitava maravilha do mundo".

Imagine transformar R$100 em R$10.000. Parece impossível? Não com matemática.

No nosso E-book exclusivo VIP, "Juros Compostos nas Apostas", ensinamos o método exato.

**Exemplo real de um membro VIP:**
- Semana 1: R$100 ➔ R$250
- Semana 2: R$250 ➔ R$625
- Semana 3: R$625 ➔ R$1.560
- Semana 4: R$1.560 ➔ R$3.900

Isso não é sorte. É estratégia. E está esperando por você no VIP.

🚨 **LIBERAMOS MAIS {vagas} VAGAS PARA A OFERTA DE 90 DIAS GRÁTIS + BÔNUS DE R$600!**
"""
            keyboard = [[InlineKeyboardButton("📈 QUERO APRENDER O SEGREDO DOS JUROS COMPOSTOS", callback_data="oferta_vip")]]
            await self.app.bot.send_message(canal_id, mensagem, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

        elif tipo_campanha == "escassez_extrema":
            logger.info("Enviando campanha de marketing: Escassez Extrema.")
            horas = random.randint(2, 4)
            mensagem = f"""
🔥🔥 **ÚLTIMA CHAMADA - TUDO OU NADA!** 🔥🔥

A diretoria vai **ENCERRAR A OFERTA** de 90 dias VIP grátis + Bônus de R$600 nas próximas **{horas} HORAS**!

Depois disso, o acesso VIP será apenas para convidados e com valor muito superior.

Você tem duas escolhas:
1. Continuar olhando os outros lucrarem.
2. Agir agora, garantir sua vaga e ter a chance de concorrer a uma Lamborghini, Rolex e viagens de luxo.

A decisão é sua. O tempo está correndo. ⏳
"""
            keyboard = [[InlineKeyboardButton(f"⚡️ EU QUERO! ÚLTIMA CHANCE (EXPIRA EM {horas}H)", callback_data="oferta_vip")]]
            await self.app.bot.send_message(canal_id, mensagem, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

        else: # prova_social
            logger.info("Enviando campanha de marketing: Prova Social.")
            greens_vip = self.app.bot_data.get('win_primeira_vip', 0) + self.app.bot_data.get('win_gale_vip', 0)
            reds_vip = self.app.bot_data.get('loss_vip', 0)
            assertividade_vip = (greens_vip / max(greens_vip + reds_vip, 1)) * 100
            
            mensagem = f"""
📈 **RESULTADOS NÃO MENTEM!** 📈

Enquanto você pensa, nossos membros VIP estão lucrando.

**Placar de hoje (Apenas VIP):**
**{greens_vip} ✅ x {reds_vip} ❌** ({assertividade_vip:.1f}% de Assertividade)

Ainda dá tempo de participar dos próximos. A escolha é sua.
"""
            keyboard = [[InlineKeyboardButton("💎 QUERO FAZER PARTE DO TIME DE VENCEDORES", callback_data="oferta_vip")]]
            await self.app.bot.send_photo(
                chat_id=canal_id,
                photo=f"https://raw.githubusercontent.com/Bruno123456-del/Bacbo-Sinais-BotPro/main/imagens/prova{random.randint(1, 19 )}.png",
                caption=mensagem,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
