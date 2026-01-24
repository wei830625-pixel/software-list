import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# apps.json 路徑
APPS_JSON = "apps.json"
# icons 資料夾
ICONS_DIR = "icons"

# 建立 icons 資料夾
os.makedirs(ICONS_DIR, exist_ok=True)

# 讀 apps.json
with open(APPS_JSON, encoding="utf-8") as f:
    data = json.load(f)

for category, apps in data.items():
    for app in apps:
        url = app["url"]
        icon_name = app["icon"]  # 直接用 JSON 裡指定的檔名
        print(f"處理 {app['name']} ...")

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")

            # 找 <link rel="icon">
            icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
            if icon_link and icon_link.get("href"):
                icon_url = urljoin(url, icon_link["href"])
            else:
                # fallback: 網站根目錄 /favicon.ico
                icon_url = urljoin(url, "/favicon.ico")

            # 下載圖示
            r_icon = requests.get(icon_url, timeout=5)

            # 取得副檔名
            ext = os.path.splitext(icon_url)[1]
            if ext.lower() not in [".png", ".ico", ".jpg", ".svg"]:
                ext = ".png"  # fallback

            # 完整檔案路徑（使用 JSON 指定的檔名）
            filename = os.path.join(ICONS_DIR, icon_name)

            # 儲存圖示
            with open(filename, "wb") as f_icon:
                f_icon.write(r_icon.content)

            print(f"成功下載 {filename}")
        except Exception as e:
            print(f"失敗 {app['name']}: {e}")
