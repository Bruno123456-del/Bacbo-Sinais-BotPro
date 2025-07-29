class Messages:
    def __init__(self, url_cadastro):
        self.url_cadastro = url_cadastro
        
    def get_mensagem_fixada(self):
        return f"""
💎 *BEM-VINDO À SALA VIP - BAC BO DE ELITE* 💎

Prezado(a) investidor(a),

Para garantir uma experiência de alta performance e resultados sincronizados com nossos analistas, é *essencial* que você opere na mesma plataforma que utilizamos.

Nossos algoritmos são calibrados para a **1WIN**.

1️⃣ **PASSO 1: CADASTRO ESTRATÉGICO**
   Clique no link abaixo para criar sua conta e alinhar-se à nossa frequência operacional.
   👉 {self.url_cadastro}

2️⃣ **PASSO 2: ATIVAÇÃO DE BÔNUS**
   Realize um depósito inicial para ativar os bônus de boas-vindas e estar pronto para as operações.

⚠️ *Operar em outra plataforma resultará em divergência de resultados.*

*Invista com inteligência. Jogue junto, ganhe junto.*
"""

    def get_reforco_pos_win(self):
        return [
            f"✅ Sincronia perfeita! É por isso que operamos na **1WIN**. Se você ainda não está lá, a hora é agora 👉 {self.url_cadastro}",
            f"🚀 Mais um resultado positivo! Nossos sinais são otimizados para a plataforma certa. Cadastre-se e comprove 👉 {self.url_cadastro}"
        ]

    def get_mensagem_automatica_recorrente(self):
        return f"""
🔔 *LEMBRETE DE PERFORMANCE* 🔔

Resultados consistentes exigem as ferramentas certas. Nossa estratégia é 100% compatível com a **1WIN**.

Não perca mais tempo com plataformas não sincronizadas.

🔗 **Garanta sua vaga e bônus:** {self.url_cadastro}

*A sorte favorece os bem preparados.*
"""

    def get_mensagem_sinal(self, sinal):
        return (
            f"🔥 OPORTUNIDADE DE ENTRADA DETECTADA 🔥\n\n"
            f"▪️ Ativo: BAC BO\n"
            f"▪️ Direção: {sinal['direcao']} {sinal['cor_direcao']}\n"
            f"▪️ Cobertura: {sinal['cobertura']} {sinal['cor_cobertura']}\n"
            f"▪️ Estratégia: Escada Asiática com Cobertura\n\n"
            f"PLANO DE AÇÃO:\n"
            f"1️⃣ Entrada Principal: Meta de +4%\n"
            f"2️⃣ Proteção 1 (Gale): Se necessário\n"
            f"3️⃣ Proteção 2 (Gale): Se necessário\n\n"
            f"⚠️ Opere com precisão. Siga a gestão."
        )

    def get_mensagem_placar(self, greens, reds):
        return f"📊 PLACAR\n✅ Greens: {greens}\n❌ Reds: {reds}"

    def get_textos_prova_social(self):
        return [
            "🔥 Veja esse resultado incrível!",
            "🚀 Nossa comunidade está lucrando pesado!",
            "💰 Resultado que fala por si só!"
        ]

    def get_captions_win(self):
        return {
            "entrada": "✅ WIN NA ENTRADA PRINCIPAL!\n💰 LUCRO ALCANÇADO: +4%",
            "gale1": "✅ WIN NO GALE 1!\n💰 LUCRO TOTAL: +8%",
            "gale2": "✅ WIN NO GALE 2!\n💰 LUCRO TOTAL: +16%",
            "stop_loss": "❌ STOP LOSS\n\nEncerramos para proteger o capital."
        }

