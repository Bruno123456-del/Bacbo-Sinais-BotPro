import os
from PIL import Image

# Caminho para a pasta onde estão as imagens
PASTA_IMAGENS = os.path.join(os.path.dirname(__file__), "imagens")

def carregar_imagens():
    imagens = []
    for arquivo in os.listdir(PASTA_IMAGENS):
        # Pega somente arquivos de imagem
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
            caminho = os.path.join(PASTA_IMAGENS, arquivo)
            try:
                img = Image.open(caminho)
                imagens.append((arquivo, img))
            except Exception as e:
                print(f"Erro ao abrir {arquivo}: {e}")
    return imagens

if __name__ == "__main__":
    imagens_carregadas = carregar_imagens()
    print(f"Total de imagens encontradas: {len(imagens_carregadas)}")
    for nome, _ in imagens_carregadas:
        print(f" - {nome}")
