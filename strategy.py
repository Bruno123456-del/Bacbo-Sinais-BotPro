import random

class Estrategia:
    def __init__(self, config):
        self.config = config
        self.opcoes = [
            {"direcao": "🔵 BANKER", "cor_direcao": "🔵", "cobertura": "⚫ TIE", "cor_cobertura": "⚫"},
            {"direcao": "🔴 PLAYER", "cor_direcao": "🔴", "cobertura": "⚫ TIE", "cor_cobertura": "⚫"}
        ]

    def gerar_sinal(self):
        """Gera um novo sinal de aposta aleatoriamente."""
        return random.choice(self.opcoes)

    def simular_resultado(self):
        """Simula o resultado de uma aposta com base nas chances configuradas."""
        chance = random.random()
        if chance < self.config.CHANCE_WIN_ENTRADA_INICIAL:
            return "entrada"
        elif chance < self.config.CHANCE_WIN_GALE_1:
            return "gale1"
        elif chance < self.config.CHANCE_WIN_GALE_2:
            return "gale2"
        else:
            return "stop_loss"
