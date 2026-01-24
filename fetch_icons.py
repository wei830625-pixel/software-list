import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

# 路徑
APPS_JSON = "apps.json"
ICONS_DIR = "icons"

os.makedirs(ICONS_DIR, exist_ok=True)

# 讀 apps.json
with open(APPS_JSON, encoding="utf-8") as f:
    data = json.load(f)

for category, apps in data.items():
    for app in apps:
        url = app["url"]
        icon_name = app["icon"]
        print(f"處理 {app['name']} ...")

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
            if icon_link and icon_link.get("href"):
                icon_url = urljoin(url, icon_link["href"])
            else:
                icon_url = urljoin(url, "/favicon.ico")

            r_icon = requests.get(icon_url, timeout=5)
            if r_icon.status_code != 200:
                raise Exception("抓不到圖示，跳過")

            filename = os.path.join(ICONS_DIR, icon_name)
            with open(filename, "wb") as f_icon:
                f_icon.write(r_icon.content)

            print(f"成功下載 {filename}")

        except Exception as e:
            print(f"跳過 {app['name']}: {e}")
