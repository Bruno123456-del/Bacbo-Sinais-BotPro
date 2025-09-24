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
        [InlineKeyboardButton("2️⃣ ENVIAR COMPROVANTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace(\'@\', \'\')}")],
        [InlineKeyboardButton("🤔 Quero ver seu canal grátis primeiro", url=URL_TELEGRAM_FREE)]
    ]

def get_vip_signal_message(jogo: str, aposta_escolhida: str) -> str:
    return f"""
💎 **ENTRADA CONFIRMADA | {jogo}** 💎

Pessoal, podem entrar!

🎯 **Aposta:** {aposta_escolhida}
🔥 **Confiança da Análise:** Altíssima

🔗 **JOGAR AGORA:**
[**>> CLIQUE AQUI PARA ACESSAR A PLATAFORMA <<**]({URL_CADASTRO_DEPOSITO})

Vamos pra cima! 🚀
"""

def get_vip_win_message(jogo: str) -> str:
    return f"✅✅✅ GREEN! É dinheiro no bolso da galera! {jogo} 🤑"

def get_vip_gale_message(jogo: str) -> str:
    return f"✅ GREEN NO GALE! Quem seguiu a gestão, lucrou! {jogo} 💪"

def get_vip_loss_message(jogo: str) -> str:
    return f"❌ RED! Acontece, pessoal. Disciplina e gestão de banca que a gente recupera na próxima. {jogo} 🔄"

def get_free_opportunity_message(confianca: float, jogo: str) -> str:
    return f"""
🚨 **Júnior Moreira na área!** 🚨

Acabei de identificar uma **OPORTUNIDADE DE LUCRO GIGANTESCA** com **{confianca*100:.0f}% de confiança** no **{jogo}**!

🔥 **O SINAL COMPLETO FOI ENVIADO AGORA MESMO PARA O GRUPO VIP!** 🔥

Lá, a galera já está operando com nossa estratégia exclusiva:
✅ **Sem GALE:** Focamos em entradas cirúrgicas, sem recuperação forçada.
🎯 **Alvo de Ganho:** Definimos metas claras para maximizar lucros.
🛡️ **Proteção Contra Perdas:** Usamos Juros Compostos para proteger sua banca e acelerar seus resultados.

Não perca mais tempo apenas observando! A hora de lucrar de verdade é AGORA.
"""

def get_free_opportunity_keyboard():
    return [[InlineKeyboardButton("💎 QUERO LUCRAR NO VIP COM O JÚNIOR!", callback_data="oferta_vip")]]

def get_free_result_message(jogo: str, aposta_escolhida: str, greens_vip: int, reds_vip: int, assertividade_vip: float) -> str:
    return f"""
✅✅ **GREEN NO VIP CONFIRMADO!** ✅✅

Eu avisei, pessoal! O sinal que enviei no **{jogo}** bateu em cheio! A entrada foi: **{aposta_escolhida}**.

Meu grupo VIP acabou de colocar mais dinheiro no bolso, seguindo nossa metodologia:
✅ **Sem GALE:** Entradas precisas, sem riscos desnecessários.
🎯 **Alvo de Ganho:** Foco total em resultados consistentes.
🛡️ **Proteção de Banca:** Juros Compostos para crescimento seguro e exponencial.

📊 **Nosso placar de hoje (VIP):**
**{greens_vip} ✅ x {reds_vip} ❌** ({assertividade_vip:.1f}% de Assertividade)

Cansado de ver a gente lucrar e ficar de fora? Vem para o time que sabe o que faz!
"""

def get_free_result_keyboard():
    return [[InlineKeyboardButton("🚀 QUERO LUCRAR COM VOCÊ, JÚNIOR!", callback_data="oferta_vip")]]

def get_vip_offer_message(user_first_name: str) -> str:
    return f"""
🚨 **Ótima decisão, {user_first_name}!** 🚨
Júnior Moreira aqui para te guiar rumo aos lucros. Siga os passos e garanta sua vaga:

🔥 **Use o Código Promocional: `GESTAO`** 🔥

Com ele, você garante acesso a um mundo de vantagens exclusivas:
💰 **BÔNUS DE ATÉ R$ 600,00** para começar com o pé direito!
💎 **90 DIAS DE ACESSO VIP GRÁTIS** aos meus sinais mais quentes!
✈️ **SORTEIOS DE VIAGENS INCRÍVEIS** para destinos paradisíacos!
💸 **MALAS DE DINHEIRO** (metáfora para grandes prêmios em eventos exclusivos)!
🎁 **BÔNUS E GIROS GRÁTIS** nas melhores plataformas!
🚗 **SORTEIO DE CARRO DE LUXO** para os membros mais engajados!
📚 **2 E-BOOKS PROFISSIONAIS:** "Juros Compostos na Prática" e "Gestão de Banca Vencedora"!

⚠️ **ATENÇÃO: ESTOU LIBERANDO POUQUÍSSIMAS VAGAS!** Essa é a sua chance de mudar de vida.
"""

def get_vip_offer_keyboard():
    return [
        [InlineKeyboardButton("1️⃣ ATIVAR OFERTA E USAR CÓDIGO", url=URL_CADASTRO_DEPOSITO)],
        [InlineKeyboardButton("2️⃣ ENVIAR COMPROVANTE", url=f"https://t.me/{SUPORTE_TELEGRAM.replace(\'@\', \'\')}")],
    ]

def get_photo_received_message() -> str:
    return "✅ Comprovante recebido! Minha equipe já vai analisar e te dar o acesso VIP."


