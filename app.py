from flask import Flask, request, jsonify, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import datetime

app = Flask(__name__)

# ✅ 請換成你的實際 Token 和 Secret
LINE_CHANNEL_ACCESS_TOKEN = " PX7Y3/X7NPN9P0FMXOzPAF6HVT9y9TCtPzqGgTSM9uLOrrlFmvOZF42gQamdD9kqnMsZzCnh8k5ugMWeVyGtuRLw8e90tc++OqcJ/zjnZo6pTs1igEYbYh2N4XsGhJb1tRaSgqREIwDidqEUYu0SRgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "8522fdb8afa545b5df340b00b77bacc8"
USER_ID = "0966145283"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ✅ Webhook 路由：LINE 發送事件時會呼叫
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# ✅ 處理使用者傳來的文字
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    print("✅ 收到來自用戶 ID：", user_id)
    reply_text = f"你傳了：{event.message.text}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# ✅ 本機 YOLO 傳送警示的 /report 路由
@app.route("/report", methods=["POST"])
def report():
    data = request.get_json()
    labels = data.get("labels", [])
    warnings = data.get("warnings", [])
    abnormal = data.get("abnormal", False)
    timestamp = data.get("timestamp", datetime.datetime.now().isoformat())

    print(f"[{timestamp}] 收到異常：{warnings}")

    if abnormal:
        for w in warnings:
            msg = f"⚠️ {w}（時間：{timestamp}）"
            push_line_message(msg)

    return jsonify({"status": "received", "warnings": warnings})

# ✅ LINE 推播函式
def push_line_message(msg):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": msg}]
    }
    res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=body)
    print("📲 LINE 推播結果：", res.status_code)

@app.route("/")
def home():
    return "Flask 平台已啟動，支援 /callback + /report"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
