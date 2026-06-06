import requests
from bs4 import BeautifulSoup
import os

URL = "https://9y.bfage.com/news/lists/2"

html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")

title = soup.title.text.strip()

requests.post(
    os.environ["DISCORD_WEBHOOK"],
    json={
        "content": f"测试成功！\n网页标题：{title}\n{URL}"
    }
)
