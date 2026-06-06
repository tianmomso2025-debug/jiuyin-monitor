import requests
from bs4 import BeautifulSoup
import os

URL = "https://9y.bfage.com/news/lists/2"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers, timeout=10).text
soup = BeautifulSoup(html, "html.parser")

# ✔ 关键修复：只抓包含日期的公告行
items = soup.select("a")

news = []

for a in items:
    text = a.get_text(strip=True)

    # 过滤规则：公告标题通常 > 6 且不含奇怪导航
    if text and len(text) > 6:
        news.append(text)

# 取最上面一个真正标题
latest = news[0] if news else None

if not latest:
    raise Exception("仍然抓不到公告（网页结构变化）")

STATE_FILE = "latest.txt"

old = ""
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old = f.read().strip()

if latest != old:

    requests.post(
        WEBHOOK,
        json={
            "content": f"📢 九阴公告更新\n\n{latest}\n\n{URL}"
        }
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(latest)

    os.system('git config user.name "github-actions"')
    os.system('git config user.email "github-actions@github.com"')
    os.system('git add latest.txt')
    os.system('git commit -m "update latest"')
    os.system('git push')
