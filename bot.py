import os
import json
import threading
import requests
from functools import wraps
from flask import Flask, request, render_template_string, Response

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

PRICES_FILE = "prices.json"


def load_prices():
    with open(PRICES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


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

    prices = load_prices()

    if text in ["/price", "قیمت"]:
        reply = f"""⚡️ قیمت محصولات VORNEX

🤖 Gemini
💰 {prices["gemini"]}

💬 ChatGPT
💰 {prices["chatgpt"]}

🌐 کانفیگ نامحدود
▫️ ۱ ماهه: {prices["config_unlimited_1"]}
▫️ ۲ ماهه: {prices["config_unlimited_2"]}
▫️ ۳ ماهه: {prices["config_unlimited_3"]}

📦 کانفیگ حجمی
💰 {prices["config_gb"]}

🎮 کانفیگ گیم
💰 {prices["gaming"]}

🎨 ادیت و افزایش کیفیت عکس
💰 {prices["edit"]}

🎧 پشتیبانی: @Hasanabadi1385
📢 کانال: @VORNEXNET"""

        send_message(chat_id, reply)


def check_auth(auth):
    if not auth:
        return False

    admin_user = os.environ.get("ADMIN_USER")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    return (
        auth.username == admin_user
        and auth.password == admin_password
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not check_auth(auth):
            return Response(
                "🔐 ورود به پنل مدیریت VORNEX",
                401,
                {
                    "WWW-Authenticate":
                    'Basic realm="VORNEX Admin"'
                }
            )

        return f(*args, **kwargs)

    return decorated


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


@app.route("/admin", methods=["GET", "POST"])
@requires_auth
def admin():
    prices = load_prices()

    if request.method == "POST":
        prices["gemini"] = request.form.get(
            "gemini", prices["gemini"]
        )

        prices["chatgpt"] = request.form.get(
            "chatgpt", prices["chatgpt"]
        )

        prices["config_unlimited_1"] = request.form.get(
            "config_unlimited_1",
            prices["config_unlimited_1"]
        )

        prices["config_unlimited_2"] = request.form.get(
            "config_unlimited_2",
            prices["config_unlimited_2"]
        )

        prices["config_unlimited_3"] = request.form.get(
            "config_unlimited_3",
            prices["config_unlimited_3"]
        )

        prices["config_gb"] = request.form.get(
            "config_gb",
            prices["config_gb"]
        )

        prices["gaming"] = request.form.get(
            "gaming",
            prices["gaming"]
        )

        prices["edit"] = request.form.get(
            "edit",
            prices["edit"]
        )

        with open(PRICES_FILE, "w", encoding="utf-8") as f:
            json.dump(
                prices,
                f,
                ensure_ascii=False,
                indent=2
            )

        return """
        <div dir="rtl"
             style="font-family:Arial;text-align:center;margin-top:50px">
            <h2>✅ قیمت‌ها با موفقیت ذخیره شدند</h2>
            <a href="/admin">بازگشت به پنل مدیریت</a>
        </div>
        """

    return render_template_string("""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>پنل مدیریت VORNEX</title>

<style>
body {
    font-family: Arial, sans-serif;
    max-width: 600px;
    margin: 30px auto;
    padding: 20px;
    background: #f4f4f4;
}

.box {
    background: white;
    padding: 20px;
    border-radius: 15px;
}

h2 {
    text-align: center;
}

label {
    display: block;
    margin-top: 15px;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 8px;
}

button {
    width: 100%;
    padding: 14px;
    margin-top: 25px;
    border: 0;
    border-radius: 10px;
    background: #111;
    color: white;
    font-size: 16px;
}
</style>
</head>

<body>

<div class="box">

<h2>⚡️ پنل مدیریت VORNEX</h2>

<form method="POST">

<label>Gemini</label>
<input name="gemini" value="{{ prices['gemini'] }}">

<label>ChatGPT</label>
<input name="chatgpt" value="{{ prices['chatgpt'] }}">

<label>کانفیگ نامحدود ۱ ماهه</label>
<input name="config_unlimited_1"
       value="{{ prices['config_unlimited_1'] }}">

<label>کانفیگ نامحدود ۲ ماهه</label>
<input name="config_unlimited_2"
       value="{{ prices['config_unlimited_2'] }}">

<label>کانفیگ نامحدود ۳ ماهه</label>
<input name="config_unlimited_3"
       value="{{ prices['config_unlimited_3'] }}">

<label>کانفیگ حجمی</label>
<input name="config_gb"
       value="{{ prices['config_gb'] }}">

<label>کانفیگ گیم</label>
<input name="gaming"
       value="{{ prices['gaming'] }}">

<label>ادیت و افزایش کیفیت عکس</label>
<input name="edit"
       value="{{ prices['edit'] }}">

<button type="submit">
💾 ذخیره قیمت‌ها
</button>

</form>

</div>

</body>
</html>
""", prices=prices)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )
