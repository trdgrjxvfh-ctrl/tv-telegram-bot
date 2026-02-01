import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()

def send_telegram(text: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Faltan TELEGRAM_TOKEN o CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, json=payload, timeout=20)
    print("Telegram:", r.status_code, r.text)

@app.get("/")
def home():
    return "OK"

# ✅ Prueba rápida desde navegador: /test
@app.get("/test")
def test():
    send_telegram("✅ Bot Render OK. Si ves esto, ya funciona.")
    return "Sent"

# ✅ Webhook para TradingView
@app.post("/webhook")
def webhook():
    data = request.get_json(silent=True) or {}

    symbol = data.get("symbol", "N/A")
    side   = data.get("side", "N/A")
    tf     = data.get("tf", "N/A")
    price  = data.get("price", "N/A")
    note   = data.get("note", "")

    msg = (
        f"🔔 SEÑAL TradingView\n"
        f"📌 {symbol}\n"
        f"➡️ {side}\n"
        f"⏱ TF: {tf}\n"
        f"💰 Precio: {price}\n"
    )
    if note:
        msg += f"📝 {note}\n"

    send_telegram(msg)
    return "OK"
