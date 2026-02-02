import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=20)
    return r.text

@app.route("/")
def home():
    return "Bot activo"

@app.route("/test")
def test():
    resp = send_telegram("✅ Bot Render OK. Funciona correctamente.")
    return f"Enviado. Telegram dice: {resp}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True) or {}

    simbolo = data.get("Simbolo", "MNQ")
    side = data.get("Side", "N/A")
    tf = data.get("Tf", "N/A")
    precio = data.get("Precio", "N/A")

    mensaje = (
        f"📢 SEÑAL\n"
        f"📌 {simbolo}\n"
        f"➡️ {side}\n"
        f"⏱ TF: {tf}\n"
        f"💰 Precio: {precio}"
    )

    send_telegram(mensaje)
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
