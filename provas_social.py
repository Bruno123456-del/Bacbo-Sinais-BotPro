import os
from telegram import Bot
from PIL import Image

# === CONFIGURAÇÕES DO TELEGRAM ===
TOKEN = "SEU_TOKEN_AQUI"  # 👉 Substitua pelo token do seu bot do Telegram
CANAL = "@seu_canal_aqui"  # 👉 Substitua pelo @ do seu canal (bot precisa ser admin)

# === CAMINHO PARA A PASTA DAS IMAGENS ===
PASTA_IMAGENS = os.path.join(os.path.dirname(__file__), "imagens")

def carregar_imagens():
    imagens = []
    for arquivo in os.listdir(PASTA_IMAGENS):
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
            caminho = os.path.join(PASTA_IMAGENS, arquivo)
            try:
                # Verifica se a imagem é válida
                Image.open(caminho)
                imagens.append(caminho)
            except Exception as e:
                print(f"Erro ao abrir {arquivo}: {e}")
    return imagens

def enviar_para_telegram(imagens):
    bot = Bot(token=TOKEN)
    for imagem in imagens:
        try:
            with open(imagem, 'rb') as file:
                bot.send_photo(chat_id=CANAL, photo=file, caption="💬 Novo feedback de aluno!")
                print(f"✅ Enviado: {os.path.basename(imagem)}")
        except Exception as e:
            print(f"❌ Erro ao enviar {imagem}: {e}")

if __name__ == "__main__":
    imagens = carregar_imagens()
    print(f"📦 Total de imagens encontradas: {len(imagens)}")
    enviar_para_telegram(imagens)
