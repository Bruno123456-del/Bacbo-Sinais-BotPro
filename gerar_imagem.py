from PIL import Image, ImageDraw, ImageFont
import random
import os
from datetime import datetime

CAMINHO_BG = "imagens/bg.png"

frases = [
    "Ganhei R$280 hoje com seus sinais, valeu mano 🔥🔥🔥",
    "Tamo junto irmão! Só bora que hoje tem mais 💸",
    "Você é brabo! Bati minha meta em 2 horas 🔥💰",
    "Nunca ganhei tanto assim em um dia 😱",
    "Top demais mano, acertei todas 👊🏼",
]

def gerar():
    mensagem = random.choice(frases)
    hora_atual = datetime.now().strftime("%H:%M")

    img = Image.open(CAMINHO_BG).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", size=28)
    except:
        font = ImageFont.load_default()

    draw.text((60, 420), mensagem, font=font, fill=(0, 0, 0))
    draw.text((500, 510), hora_atual, font=font, fill=(128, 128, 128))

    # Define nome fixo para facilitar envio
    nome_arquivo = "imagens/print_simulado.png"

    # Cria pasta se não existir
    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)

    img.save(nome_arquivo)

    print(f"[✅] Imagem gerada com sucesso: {nome_arquivo}")

    return nome_arquivo
