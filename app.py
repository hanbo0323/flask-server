from flask import Flask, request, jsonify
import datetime
import requests

app = Flask(__name__)

# LINE 設定
LINE_CHANNEL_ACCESS_TOKEN = "你的 Channel Access Token"
USER_ID = "你的 LINE User ID"

def push_line_message(msg):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "to": USER_ID,
        "messages": [{
            "type": "text",
            "text": msg
        }]
    }
    res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=body)
    print("📲 LINE 推播結果：", res.status_code)

@app.route("/report", methods=["POST"])
def report():
    try:
        data = request.get_json()
        timestamp = data.get("timestamp", datetime.datetime.now().isoformat())
        labels = data.get("labels", [])
        abnormal = data.get("abnormal", False)
        warnings = data.get("warnings", [])

        print(f"[{timestamp}] 🚨 報告收到：{labels} 異常={abnormal}")

        if abnormal:
            for w in warnings:
                push_line_message(f"⚠️ {w} - 時間：{timestamp}")

        return jsonify({"status": "received", "abnormal": abnormal, "warnings": warnings})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/")
def home():
    return "Flask 伺服器已啟動（/report）"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
