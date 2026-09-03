let currentVideoId = null;
let watchTime = 0;
let counted = false;


// 今日の日付
function getToday() {
    const date = new Date();

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}


// URLから動画IDを取得
function getVideoId() {
    const match = location.pathname.match(/^\/shorts\/([^/?]+)/);
    return match ? match[1] : null;
}


// video要素を取得
function getVideo() {
    return document.querySelector("video");
}


// 動画タイトルを取得
function getVideoTitle() {

    // YouTube Shortsのタイトル
    const titleElement = document.querySelector(
        "h1.ytd-watch-metadata"
    );

    if (titleElement) {
        return titleElement.innerText.trim();
    }

    // 別の場所にある場合
    const metaTitle = document.querySelector(
        'meta[name="title"]'
    );

    if (metaTitle) {
        return metaTitle.content;
    }

    // 最終手段
    return document.title
        .replace(" - YouTube", "")
        .trim();
}


// Pythonへ視聴データを送信
function sendData() {

    if (!currentVideoId || watchTime <= 0) {
        return;
    }

    const today = getToday();
    const title = getVideoTitle();

    console.log("📤 送信する動画タイトル:", title);

    fetch("http://127.0.0.1:5000/track", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            date: today,
            video_id: currentVideoId,
            title: title,
            watch_time: watchTime
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(
            "🐍 Pythonへ送信:",
            watchTime,
            "秒"
        );
    })
    .catch(error => {
        console.error(
            "❌ Pythonへの送信に失敗:",
            error
        );
    });
}


// 新しい動画を検知
function checkVideo() {

    const videoId = getVideoId();

    if (
        videoId &&
        videoId !== currentVideoId
    ) {

        // 前の動画を保存
        if (
            currentVideoId &&
            watchTime > 0
        ) {
            sendData();
        }

        currentVideoId = videoId;
        watchTime = 0;
        counted = false;

        console.log(
            "🎬 新しいShorts！",
            videoId
        );
    }
}


// 視聴時間を計測
function trackTime() {

    const video = getVideo();

    if (
        !video ||
        !currentVideoId
    ) {
        return;
    }

    if (
        document.visibilityState === "visible" &&
        !video.paused
    ) {

        watchTime++;

        console.log(
            "⏱️ 視聴時間:",
            watchTime,
            "秒"
        );

        // 2秒以上見たら1本として扱う
        if (
            watchTime >= 2 &&
            !counted
        ) {

            counted = true;

            console.log(
                "🎉 1本視聴しました！"
            );
        }
    }
}


// タブを離れたとき
document.addEventListener(
    "visibilitychange",
    () => {

        if (
            document.visibilityState === "hidden"
        ) {
            sendData();
        }

    }
);


setInterval(checkVideo, 500);

setInterval(trackTime, 1000);

checkVideo();