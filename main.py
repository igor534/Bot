import feedparser
import requests
import os
import time

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")  # додамо через Render

rss_feeds = [
    "https://rss.unian.net/site/news_ukr.rss",
    "https://www.ukrinform.ua/rss",
    "https://www.bbc.com/ukrainian/index.xml",
    "https://24tv.ua/rss/all.xml"
]

sent_links = set()

def send_telegram_message(title, link, source):
    message = f"📰 <b>{title}</b>\n📍 Джерело: {source}\n🔗 {link}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        resp = requests.post(url, data=payload)
        print("Posted:", title, "| status:", resp.status_code)
    except Exception as e:
        print("Error sending:", e)

if __name__ == "__main__":
    while True:
        for feed_url in rss_feeds:
            data = feedparser.parse(feed_url)
            source_title = data.feed.get("title", "News")
            for entry in data.entries:
                if entry.link not in sent_links:
                    send_telegram_message(entry.title, entry.link, source_title)
                    sent_links.add(entry.link)
        time.sleep(300)  # 5 хвилин
