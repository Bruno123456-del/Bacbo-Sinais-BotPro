from PIL import Image, ImageDraw, ImageFont
import random
import os
from datetime import datetime

# Caminho para a imagem de fundo (estilo WhatsApp limpo)
CAMINHO_BG = "imagens/bg.png"

# Frases simuladas (você pode adicionar mais)
frases = [
    "Ganhei R$280 hoje com seus sinais, valeu mano 🔥🔥🔥",
    "Tamo junto irmão! Só bora que hoje tem mais 💸",
    "Você é brabo! Bati minha meta em 2 horas 🔥💰",
    "Nunca ganhei tanto assim em um dia 😱",
    "Top demais mano, acertei todas 👊🏼",
]

# Escolhe frase aleatória
mensagem = random.choice(frases)

# Gera horário simulado no estilo WhatsApp
hora_atual = datetime.now().strftime("%H:%M")

# Abre imagem de fundo
img = Image.open(CAMINHO_BG).convert("RGB")
draw = ImageDraw.Draw(img)

# Fonte (use uma fonte TTF que você tenha, ex: Arial)
try:
    font = ImageFont.truetype("arial.ttf", size=28)
except:
    font = ImageFont.load_default()

# Desenha a mensagem simulada
draw.text((60, 420), mensagem, font=font, fill=(0, 0, 0))  # texto escuro
draw.text((500, 510), hora_atual, font=font, fill=(128, 128, 128))  # hora no canto

# Salva imagem gerada
nome_arquivo = f"imagens/print_simulado_{random.randint(1000,9999)}.png"
img.save(nome_arquivo)

print(f"[✅] Imagem gerada com sucesso: {nome_arquivo}")
