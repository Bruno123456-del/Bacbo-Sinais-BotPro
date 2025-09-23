from config import URL_CADASTRO_DEPOSITO, SUPORTE_TELEGRAM, URL_TELEGRAM_FREE
from telegram import InlineKeyboardButton

def get_start_message(nome_usuario: str) -> str:
    return f"""
Olá, {nome_usuario}! Sou o Júnior Moreira, especialista em análise de dados para jogos online. Seja muito bem-vindo(a).

Se você chegou até aqui, é porque busca uma forma consistente de lucrar. Eu desenvolvi um sistema que analisa 15 jogos 24h por dia para encontrar as melhores oportunidades para nós.

Preparei uma **condição especial para você começar a lucrar comigo hoje**:

1️⃣ **Faça seu cadastro e primeiro depósito** na plataforma que eu uso e confio. Use o código `GESTAO` para ganhar um bônus de até R$600.
2️⃣ **Me envie o comprovante** e eu vou te liberar **90 dias de acesso GRÁTIS** ao meu Grupo VIP de sinais.

Vamos começar a investir de forma inteligente.

Abraço,
**Júnior Moreira**
"""

def get_start_keyboard():
    return [
        [InlineKeyboardButton("1️⃣ CADASTRAR E PEGAR BÔNUS", url=URL_CADASTRO_DEPOSITO)],
        [InlineKeyboardButton("2️⃣ ENVIAR COMPROVANTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace(\'@\', \'\' )}")],
        [InlineKeyboardButton("🤔 Quero ver seu canal grátis primeiro", url=URL_TELEGRAM_FREE)]
    ]

def get_vip_signal_message(jogo: str, aposta_escolhida: str) -> str:
    return f"""
💎 **ENTRADA CONFIRMADA | {jogo}** 💎

Pessoal, podem entrar!\n\n🎯 **Aposta:** {aposta_escolhida}\n🔥 **Confiança da Análise:** Altíssima\n\n🔗 **JOGAR AGORA:**\n[**>> CLIQUE AQUI PARA ACESSAR A PLATAFORMA <<**]({URL_CADASTRO_DEPOSITO})\n\nVamos pra cima! 🚀
"""

def get_vip_win_message(jogo: str) -> str:
    return f"✅✅✅ GREEN! É dinheiro no bolso da galera! {jogo} 🤑"

def get_vip_gale_message(jogo: str) -> str:
    return f"✅ GREEN NO GALE! Quem seguiu a gestão, lucrou! {jogo} 💪"

def get_vip_loss_message(jogo: str) -> str:
    return f"❌ RED! Acontece, pessoal. Disciplina e gestão de banca que a gente recupera na próxima. {jogo} 🔄"

def get_free_opportunity_message(confianca: float, jogo: str) -> str:
    return f"""
🚨 **OPORTUNIDADE DE LUCRO IDENTIFICADA!** 🚨

Minha análise encontrou um padrão com **{confianca*100:.0f}% de confiança** no **{jogo}**.\n\n🔥 **ACABEI DE ENVIAR O SINAL PARA O GRUPO VIP!** 🔥\n\nO pessoal já está fazendo a entrada. Se você quer parar de só olhar e começar a lucrar comigo, a hora é agora.
"""

def get_free_opportunity_keyboard():
    return [[InlineKeyboardButton("💎 EU QUERO ENTRAR NO VIP, JÚNIOR!", callback_data="oferta_vip")]]

def get_free_result_message(jogo: str, aposta_escolhida: str, greens_vip: int, reds_vip: int, assertividade_vip: float) -> str:
    return f"""
✅✅ **GREEN NO VIP!** ✅✅\n\nComo eu disse, pessoal! O sinal que enviei no **{jogo}** bateu. A entrada foi: **{aposta_escolhida}**.\n\nMeu grupo VIP acabou de colocar mais dinheiro no bolso! 🤑\n\n📊 **Meu placar de hoje (VIP):**\n**{greens_vip} ✅ x {reds_vip} ❌** ({assertividade_vip:.1f}% de Assertividade)\n\nCansado de perder dinheiro? Vem lucrar com quem entende do assunto.
"""

def get_free_result_keyboard():
    return [[InlineKeyboardButton("🚀 QUERO LUCRAR COM VOCÊ, JÚNIOR!", callback_data="oferta_vip")]]

def get_vip_offer_message(user_first_name: str) -> str:
    return f"""
🚨 **Ótima decisão, {user_first_name}!** 🚨
Estou aqui para te ajudar a lucrar. Siga os passos:\n🔥 **Use o Código Promocional: `GESTAO`** 🔥\nCom ele, você garante:\n💰 **BÔNUS DE ATÉ R$ 600,00**\n💎 **90 DIAS DE ACESSO VIP GRÁTIS**\n📚 **MEU E-BOOK \
