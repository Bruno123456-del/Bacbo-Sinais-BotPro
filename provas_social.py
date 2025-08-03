import random
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime

# Carrega mensagens fakes
with open("mensagens.json", "r", encoding="utf-8") as f:
    mensagens = json.load(f)

# Configuração das fontes (use Arial do sistema)
fonte_nome = ImageFont.truetype("arialbd.ttf", 22)
fonte_mensagem = ImageFont.truetype("arial.ttf", 20)
fonte_hora = ImageFont.truetype("arial.ttf", 14)

def gerar_imagem_prova_social(index):
    dados = random.choice(mensagens)

    bg = Image.open("imagens/bg.png").convert("RGBA")
    draw = ImageDraw.Draw(bg)

    draw.text((85, 40), dados["nome"], fill="white", font=fonte_nome)
    draw.text((80, 120), dados["msg"], fill="black", font=fonte_mensagem)
    draw.text((350, 180), "11h20", fill="gray", font=fonte_hora)

    draw.rectangle((70, 220, 470, 280), fill=(220, 255, 220))
    draw.text((80, 230), dados["resposta"], fill="black", font=fonte_mensagem)
    draw.text((400, 270), "11h30", fill="gray", font=fonte_hora)

    nome_arquivo = f"prova_social_{index}.png"
    bg.save(f"imagens/{nome_arquivo}")
    print(f"✅ Imagem gerada: imagens/{nome_arquivo}")

# Gera 3 imagens
for i in range(1, 4):
    gerar_imagem_prova_social(i)
