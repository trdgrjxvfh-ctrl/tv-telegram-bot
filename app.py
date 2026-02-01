import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })

@app.route("/")
def home():
    return "Bot activo"

@app.route("/test")
def test():
    send_telegram("✅ Bot Render OK. Funciona correctamente.")
    return "Sent"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    symbol = data.get("symbol", "MNQ")
    side = data.get("side", "N/A")
    tf = data.get("tf", "N/A")
    price = data.get("price", "N/A")

    message = (
        "📢 SEÑAL MNQ\n"
        f"📌 {symbol}\n"
        f"➡️ {side}\n"
        f"⏱ TF: {tf}\n"
        f"💰 Precio: {price}"
    )

    send_telegram(message)
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
