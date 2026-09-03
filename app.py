import altair as alt
import streamlit as st
import json
import os
from datetime import date, timedelta
import pandas as pd


st.set_page_config(
    page_title="Short Video Tracker",
    page_icon="📱",
    layout="wide"
)

DATA_FILE = "data.json"


# =========================
# データ読み込み
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# =========================
# 時間を見やすくする
# =========================
def format_time(seconds):
    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours}時間{minutes}分{seconds}秒"

    if minutes > 0:
        return f"{minutes}分{seconds}秒"

    return f"{seconds}秒"


# =========================
# 1日のデータ
# =========================
def get_day_data(data, day):

    if day not in data:
        return {
            "videos": 0,
            "seconds": 0,
            "history": []
        }

    day_data = data[day]

    return {
        "videos": day_data.get("videos", 0),
        "seconds": day_data.get("seconds", 0),
        "history": day_data.get("history", [])
    }


# =========================
# データ
# =========================
data = load_data()

today = str(date.today())

today_data = get_day_data(data, today)


# =========================
# タイトル
# =========================
st.title("📱 Short Video Tracker")

st.caption("YouTube Shortsの視聴を自動記録しています")


# =========================
# 今日
# =========================
st.header("📅 今日")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "ショート動画",
        f"{today_data['videos']}本"
    )

with col2:
    st.metric(
        "視聴時間",
        format_time(today_data["seconds"])
    )

with col3:
    if today_data["videos"] > 0:
        average = today_data["seconds"] / today_data["videos"]
    else:
        average = 0

    st.metric(
        "1本あたり",
        format_time(average)
    )


# =========================
# 今週
# =========================
st.header("📊 今週")

today_date = date.today()

week_count = 0
week_seconds = 0

chart_data = []

for i in range(7):

    day = today_date - timedelta(days=6 - i)

    day_str = str(day)

    day_data = get_day_data(data, day_str)

    week_count += day_data["videos"]
    week_seconds += day_data["seconds"]

    chart_data.append({
        "日付": day_str,
        "視聴時間（分）": day_data["seconds"] / 60,
        "本数": day_data["videos"]
    })


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "今週の本数",
        f"{week_count}本"
    )

with col2:
    st.metric(
        "今週の視聴時間",
        format_time(week_seconds)
    )

with col3:
    if week_count > 0:
        average = week_seconds / week_count
    else:
        average = 0

    st.metric(
        "1本あたり",
        format_time(average)
    )


# =========================
# グラフ
# =========================
df = pd.DataFrame(chart_data)

st.subheader("⏱️ 1日ごとの視聴時間")

chart_time = alt.Chart(df).mark_bar().encode(
    x=alt.X("日付:N", title="日付"),
    y=alt.Y("視聴時間（分）:Q", title="視聴時間（分）"),
    tooltip=[
        alt.Tooltip("日付:N", title="日付"),
        alt.Tooltip("視聴時間（分）:Q", title="視聴時間（分）")
    ]
).properties(
    height=300
)

st.altair_chart(
    chart_time,
    use_container_width=True
)


st.subheader("📱 1日ごとの視聴本数")

chart_count = alt.Chart(df).mark_bar().encode(
    x=alt.X("日付:N", title="日付"),
    y=alt.Y("本数:Q", title="本数"),
    tooltip=[
        alt.Tooltip("日付:N", title="日付"),
        alt.Tooltip("本数:Q", title="本数")
    ]
).properties(
    height=300
)

st.altair_chart(
    chart_count,
    use_container_width=True
)


# =========================
# 自動更新
# =========================
st.divider()

st.caption("🔄 10秒ごとに自動更新")

st.markdown(
    """
    <script>
    setTimeout(function() {
        window.parent.location.reload();
    }, 10000);
    </script>
    """,
    unsafe_allow_html=True
)