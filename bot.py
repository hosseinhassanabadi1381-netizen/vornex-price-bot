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
    chat_id = message.get("chat", {}).get("id")
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

🎧 پشتیبانی: @Hasanabadi1385
📢 کانال: @VORNEXNET"""
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


@app.route("/set-webhook", methods=["GET"])
def set_webhook():
    public_url = os.environ.get("RENDER_EXTERNAL_URL")

    if not public_url:
        return "RENDER_EXTERNAL_URL not found", 500

    webhook_url = f"{public_url}/webhook"

    result = requests.get(
        f"{API}/setWebhook",
        params={"url": webhook_url},
        timeout=10
    )

    return result.text


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
