import random
from typing import List, Dict, Optional

class EscadaAsiaticaStrategy:
    """
    Implementa a estratégia Escada Asiática com Cobertura para Bac Bo.
    """
    
    def __init__(self):
        self.historico_simulado = ["Player", "Player", "Banker", "Player"]
    
    def analisar_historico(self, historico: List[str]) -> Optional[Dict]:
        """
        Analisa o histórico e retorna um sinal se houver oportunidade.
        
        Args:
            historico: Lista com o histórico de resultados
            
        Returns:
            Dict com informações do sinal ou None se não houver oportunidade
        """
        if len(historico) < 4:
            return None
            
        ultimos = historico[-4:]
        
        # Lógica da Escada Asiática: se os dois primeiros são iguais 
        # e o terceiro é diferente, apostar no segundo resultado
        if ultimos[0] == ultimos[1] and ultimos[2] != ultimos[1]:
            return {
                "direcao": ultimos[1],
                "cobertura": "Empate",
                "cor_direcao": "🔴" if ultimos[1] == "Player" else "🔵",
                "cor_cobertura": "🟡",
                "confianca": self._calcular_confianca(historico)
            }
        
        return None
    
    def _calcular_confianca(self, historico: List[str]) -> float:
        """
        Calcula o nível de confiança do sinal baseado no histórico.
        
        Args:
            historico: Lista com o histórico de resultados
            
        Returns:
            Float entre 0 e 1 representando a confiança
        """
        if len(historico) < 10:
            return 0.7
        
        # Análise simples: verifica padrões nos últimos 10 resultados
        ultimos_10 = historico[-10:]
        player_count = ultimos_10.count("Player")
        banker_count = ultimos_10.count("Banker")
        
        # Se há desequilíbrio, aumenta a confiança
        desequilibrio = abs(player_count - banker_count) / 10
        confianca_base = 0.7
        
        return min(0.95, confianca_base + (desequilibrio * 0.2))
    
    def simular_historico_real(self) -> List[str]:
        """
        Simula um histórico mais realista para testes.
        Em produção, isso seria substituído por dados reais da API.
        
        Returns:
            Lista simulada de resultados
        """
        opcoes = ["Player", "Banker", "Tie"]
        pesos = [0.45, 0.45, 0.1]  # Probabilidades mais realistas
        
        historico = []
        for _ in range(20):
            resultado = random.choices(opcoes, weights=pesos)[0]
            historico.append(resultado)
        
        return historico
    
    def get_historico_para_teste(self) -> List[str]:
        """
        Retorna o histórico simulado para testes.
        
        Returns:
            Lista com histórico simulado
        """
        return self.historico_simulado.copy()

class GestaoRisco:
    """
    Classe para gerenciar riscos e probabilidades de win.
    """
    
    def __init__(self, chance_entrada=0.70, chance_gale1=0.80, chance_gale2=0.90):
        self.chance_entrada = chance_entrada
        self.chance_gale1 = chance_gale1
        self.chance_gale2 = chance_gale2
        
    def simular_resultado_entrada(self) -> bool:
        """Simula o resultado da entrada principal."""
        return random.random() < self.chance_entrada
    
    def simular_resultado_gale1(self) -> bool:
        """Simula o resultado do primeiro gale."""
        return random.random() < self.chance_gale1
    
    def simular_resultado_gale2(self) -> bool:
        """Simula o resultado do segundo gale."""
        return random.random() < self.chance_gale2
    
    def ajustar_probabilidades(self, historico_recente: List[bool]):
        """
        Ajusta as probabilidades baseado no histórico recente de wins/losses.
        
        Args:
            historico_recente: Lista de booleans indicando wins (True) ou losses (False)
        """
        if len(historico_recente) < 5:
            return
        
        taxa_win = sum(historico_recente) / len(historico_recente)
        
        # Se a taxa de win está muito alta, reduz um pouco as chances
        if taxa_win > 0.85:
            self.chance_entrada = max(0.60, self.chance_entrada - 0.05)
            self.chance_gale1 = max(0.70, self.chance_gale1 - 0.05)
            self.chance_gale2 = max(0.80, self.chance_gale2 - 0.05)
        
        # Se a taxa de win está muito baixa, aumenta um pouco as chances
        elif taxa_win < 0.60:
            self.chance_entrada = min(0.80, self.chance_entrada + 0.05)
            self.chance_gale1 = min(0.90, self.chance_gale1 + 0.05)
            self.chance_gale2 = min(0.95, self.chance_gale2 + 0.05)

