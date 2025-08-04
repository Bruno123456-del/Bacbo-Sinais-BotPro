import os
from telegram import Bot
from PIL import Image

# === CONFIGURAÇÕES DO TELEGRAM ===
BOT_TOKEN = "7975008855:AAGEc1_htKryQnZ0qPemvoWs0Mz3PG22Q3U"
CANAL_ID = -1002808626127  # ID numérico do canal
URL_CADASTRO = "https://lkwn.cc/f1c1c45a"

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
    bot = Bot(token=BOT_TOKEN)
    for imagem in imagens:
        try:
            with open(imagem, 'rb') as file:
                legenda = f"💬 Novo feedback de aluno!\n🔗 Faça parte também: {URL_CADASTRO}"
                bot.send_photo(chat_id=CANAL_ID, photo=file, caption=legenda)
                print(f"✅ Enviado: {os.path.basename(imagem)}")
        except Exception as e:
            print(f"❌ Erro ao enviar {imagem}: {e}")

if __name__ == "__main__":
    imagens = carregar_imagens()
    print(f"📦 Total de imagens encontradas: {len(imagens)}")
    enviar_para_telegram(imagens)
