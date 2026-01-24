import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 路徑設定
APPS_JSON = "apps.json"
ICONS_DIR = "icons"

# 建立 icons 資料夾（如果不存在）
os.makedirs(ICONS_DIR, exist_ok=True)

# 讀取 apps.json
with open(APPS_JSON, encoding="utf-8") as f:
    data = json.load(f)

for category, apps in data.items():
    for app in apps:
        url = app["url"]
        icon_name = app["icon"]
        icon_path = os.path.join(ICONS_DIR, icon_name)

        # 已存在圖示就跳過
        if os.path.exists(icon_path):
            print(f"已存在，跳過 {app['name']}")
            continue

        print(f"處理 {app['name']} ...")
        try:
            # 嘗試抓網站 icon
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
            if icon_link and icon_link.get("href"):
                icon_url = urljoin(url, icon_link["href"])
            else:
                icon_url = urljoin(url, "/favicon.ico")

            r_icon = requests.get(icon_url, timeout=5)
            if r_icon.status_code != 200:
                raise Exception("抓不到圖示，使用 fallback")

            # 儲存圖示
            with open(icon_path, "wb") as f_icon:
                f_icon.write(r_icon.content)

            print(f"成功下載 {icon_path}")

        except Exception as e:
            print(f"原始抓取失敗 {app['name']}: {e}")
            try:
                # fallback 使用 Google Favicon API
                fallback_url = f"https://www.google.com/s2/favicons?domain={url}"
                r_icon = requests.get(fallback_url, timeout=5)
                if r_icon.status_code == 200:
                    with open(icon_path, "wb") as f_icon:
                        f_icon.write(r_icon.content)
                    print(f"成功使用 fallback icon 下載 {icon_path}")
                else:
                    print(f"fallback 也抓不到 {app['name']}")
            except Exception as e2:
                print(f"完全失敗 {app['name']}: {e2}")
