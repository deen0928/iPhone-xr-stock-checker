import os
import requests

PRODUCT_URL = "https://mvno.geo-mobile.jp/uqmobile/smartphone/iPhoneXR_simfree"

LINE_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]


def check_stock():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://mvno.geo-mobile.jp/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    response = requests.get(
        PRODUCT_URL,
        headers=headers,
        timeout=20
    )

    print("HTTP status:", response.status_code)

    response.raise_for_status()

    html = response.text

    return "在庫切れ" not in html


def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=15
    )

    response.raise_for_status()


if __name__ == "__main__":
    if check_stock():
        send_line(
            "🔥 iPhone XRの在庫が復活した可能性があります！\n"
            + PRODUCT_URL
        )
        print("在庫あり → LINE通知しました")
    else:
        print("在庫なし")
