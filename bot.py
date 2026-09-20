import os
import threading
import requests
from flask import Flask, request

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=10
    )

def handle_update(update):
    message = update.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "").strip().lower()

    if not chat_id:
        return

    if text in ["/price", "قیمت"]:
        send_message(
            chat_id,
            """⚡️ قیمت محصولات VORNEX

🤖 Gemini
💰 ۷۵۰ هزار تومان

🌐 کانفیگ نامحدود
▫️ ۱ ماهه: ۲۵۰ هزار تومان
▫️ ۲ ماهه: ۳۵۰ هزار تومان
▫️ ۳ ماهه: ۴۵۰ هزار تومان

🎨 خدمات ادیت و افزایش کیفیت عکس
💬 برای قیمت: @Hasanabadi1385

🛒 سفارش: @VORNEXNET
🎧 پشتیبانی: @Hasanabadi1385"""
        )

@app.route("/", methods=["GET"])
def home():
    return "VORNEX Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True)

    if update:
        threading.Thread(
            target=handle_update,
            args=(update,)
        ).start()

    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
