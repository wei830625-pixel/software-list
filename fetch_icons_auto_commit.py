import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

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
        icon_path = os.path.join(ICONS_DIR, icon_name)

        # 如果檔案已存在，跳過下載
        if os.path.exists(icon_path):
            print(f"已存在，跳過 {app['name']}")
            continue

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

            with open(icon_path, "wb") as f_icon:
                f_icon.write(r_icon.content)

            print(f"成功下載 {icon_path}")

        except Exception as e:
            print(f"跳過 {app['name']}: {e}")