import requests
from bs4 import BeautifulSoup
import os

URL = "https://9y.bfage.com/news/lists/2"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

html = requests.get(URL, timeout=10).text
soup = BeautifulSoup(html, "html.parser")

# ✅ 只抓公告列表里的链接（关键修复）
items = soup.select(".list a, .news a, .article a")

latest = None

for a in items:
    text = a.get_text(strip=True)

    # 过滤明显垃圾
    if text and len(text) > 4 and "http" not in text:
        latest = text
        break

if not latest:
    raise Exception("找不到公告标题（CSS选择器不匹配）")

STATE_FILE = "latest.txt"

old = ""
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old = f.read().strip()

if latest != old:

    requests.post(
        WEBHOOK,
        json={
            "content": f"📢 九阴官网新公告\n\n{latest}\n\n{URL}"
        }
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(latest)

    os.system('git config user.name "github-actions"')
    os.system('git config user.email "github-actions@github.com"')
    os.system('git add latest.txt')
    os.system('git commit -m "update latest"')
    os.system('git push')
