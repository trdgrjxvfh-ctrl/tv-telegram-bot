import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })

@app.route("/")
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    symbol = data.get("symbol", "N/A")
    side   = data.get("side", "N/A")
    tf     = data.get("tf", "N/A")
    price  = data.get("price", "N/A")

    message = (
        f"📣 SEÑAL MNQ\n"
        f"📌 {symbol}\n"
        f"➡️ {side}\n"
        f"⏱ TF: {tf}\n"
        f"💰 Precio: {price}"
    )

    send_telegram(message)
    return "ok"
