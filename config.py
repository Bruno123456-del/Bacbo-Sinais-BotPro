import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        # Configurações do Bot
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.CHAT_ID = os.getenv("CHAT_ID")
        
        # URLs e Links
        self.URL_CADASTRO = "https://lkwn.cc/f1c1c45a"
        
        # Mídia - GIFs
        self.GIF_ANALISE = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG05Z3N5dG52ZGJ6eXNocjVqaXJzZzZkaDR2Y2l2N2dka2ZzZzBqZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJxaUHe3w2n84/giphy.gif"
        self.GIF_RED = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNzdmk5MHY2Z2k3c3A5dGJqZ2x2b2l6d2g4M3BqM3E0d2Z3a3ZqZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO5iQ1m8g49A2gU/giphy.gif"
        self.GIF_WIN = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21oZzZ5N3JzcjUwYmh6d3J4N2djaWtqZGN0aWd6dGRxY2V2c2o5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOyjZ7io5Msw/giphy.gif"
        
        # Mídia - Imagens
        self.IMG_WIN_ENTRADA = "imagens/win_entrada.png"
        self.IMG_WIN_GALE1 = "imagens/win_gale1.png"
        self.IMG_WIN_GALE2 = "imagens/win_gale2.png"
        
        # Provas Sociais
        self.PROVAS_SOCIAIS = [
            "imagens/print_win_1.png", 
            "imagens/print_win_2.png", 
            "imagens/print_win_3.png"
        ]
        
        # Probabilidades de Win
        self.CHANCE_WIN_ENTRADA_INICIAL = 0.70
        self.CHANCE_WIN_GALE_1 = 0.80
        self.CHANCE_WIN_GALE_2 = 0.90
        
        # Intervalos de Tempo (em segundos)
        self.TEMPO_ANALISE = 10
        self.TEMPO_ENTRADA = 120
        self.TEMPO_GALE = 120
        self.INTERVALO_SINAIS = 15 * 60  # 15 minutos
        self.INTERVALO_MENSAGEM_RECORRENTE = 6 * 60 * 60  # 6 horas
        
    def validate(self):
        """Valida se as configurações essenciais estão presentes"""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN não encontrado nas variáveis de ambiente")
        if not self.CHAT_ID:
            raise ValueError("CHAT_ID não encontrado nas variáveis de ambiente")
        return True

