from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask 伺服器已啟動"

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    print("收到資料：", data)
    return jsonify({"status": "success", "received": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
