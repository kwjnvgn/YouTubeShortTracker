from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


@app.route("/track", methods=["POST"])
def track():

    received = request.json

    print("受信しました！")
    print(received)

    data = load_data()

    date = received["date"]
    video_id = received["video_id"]
    title = received.get("title", "タイトル不明")
    watch_time = received["watch_time"]

    # 日付がなければ作成
    if date not in data:
        data[date] = {
            "videos": 0,
            "seconds": 0,
            "history": []
        }

    data[date].setdefault("videos", 0)
    data[date].setdefault("seconds", 0)
    data[date].setdefault("history", [])

    history = data[date]["history"]

    # 同じ動画を探す
    existing = None

    for video in history:

        if video["video_id"] == video_id:
            existing = video
            break

    if existing:

        # 古い視聴時間
        old_seconds = existing["seconds"]

        # 視聴時間を更新
        existing["seconds"] = watch_time

        # タイトルも更新
        existing["title"] = title

        # 合計時間を差分更新
        data[date]["seconds"] += (
            watch_time - old_seconds
        )

        print(
            f"🔄 {video_id} 更新"
        )

    else:

        # 新しい動画
        history.append({
            "video_id": video_id,
            "title": title,
            "seconds": watch_time
        })

        data[date]["videos"] += 1

        data[date]["seconds"] += watch_time

        print(
            "🆕 新しい動画を追加しました！"
        )

    save_data(data)

    print("💾 保存しました！")
    print(data[date])

    return jsonify({
        "status": "ok"
    })


app.run(
    host="127.0.0.1",
    port=5000
)