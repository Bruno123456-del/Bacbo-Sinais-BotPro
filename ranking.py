from db import pegar_ranking

def gerar_texto_ranking():
    top = pegar_ranking()
    if not top:
        return "🏆 Ainda não temos jogadores no ranking."

    texto = "🏆 Ranking dos maiores ganhadores:\n\n"
    for i, (nome, pontos) in enumerate(top, start=1):
        texto += f"{i}. {nome} — {pontos} pts\n"
    return texto
