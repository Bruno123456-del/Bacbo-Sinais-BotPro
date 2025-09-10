import requests
import os

CONTROLLER_BOT_TOKEN = os.getenv("CONTROLLER_BOT_TOKEN")
CHAT_ID = os.getenv("FREE_CHAT_ID")  # ID do canal FREE

def enviar_sinal(texto):
    url = f"https://api.telegram.org/bot{CONTROLLER_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    }
    r = requests.post(url, data=data)
    return r.json()
