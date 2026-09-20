import os
import requests

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

offset = 0

while True:
    response = requests.get(
        f"{API}/getUpdates",
        params={"offset": offset, "timeout": 30}
    ).json()

    for update in response.get("result", []):
        offset = update["update_id"] + 1

        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").lower().strip()

        if not chat_id:
            continue

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
