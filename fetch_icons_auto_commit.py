import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

APPS_JSON = "apps.json"
ICONS_DIR = "icons"

os.makedirs(ICONS_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def save_icon(icon_url, icon_path):
    r = requests.get(icon_url, headers=HEADERS, timeout=6)
    if r.status_code == 200 and len(r.content) > 100:
        with open(icon_path, "wb") as f:
            f.write(r.content)
        return True
    return False

with open(APPS_JSON, encoding="utf-8") as f:
    data = json.load(f)

for category, apps in data.items():
    for app in apps:
        url = app["url"]
        icon_name = app.get("icon")
        if not icon_name:
            print(f"使用線上圖示，跳過 {app['name']}")
            continue
        icon_path = os.path.join(ICONS_DIR, icon_name)

        if os.path.exists(icon_path):
            print(f"已存在，跳過 {app['name']}")
            continue

        print(f"\n處理 {app['name']}")

        parsed = urlparse(url)
        domain = parsed.netloc

        success = False

        # 1️⃣ 嘗試抓 HTML <link rel="icon">
        try:
            r = requests.get(url, headers=HEADERS, timeout=6)
            soup = BeautifulSoup(r.text, "html.parser")
            icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())

            if icon_link and icon_link.get("href"):
                icon_url = urljoin(url, icon_link["href"])
                if save_icon(icon_url, icon_path):
                    print("✔ 來自 <link rel=icon>")
                    success = True
        except:
            pass

        # 2️⃣ /favicon.ico
        if not success:
            favicon_url = f"{parsed.scheme}://{domain}/favicon.ico"
            if save_icon(favicon_url, icon_path):
                print("✔ 來自 /favicon.ico")
                success = True

        # 3️⃣ Google Favicon API
        if not success:
            google_url = f"https://www.google.com/s2/favicons?sz=128&domain={domain}"
            if save_icon(google_url, icon_path):
                print("✔ 來自 Google Favicon API")
                success = True

        # 4️⃣ DuckDuckGo Icons
        if not success:
            ddg_url = f"https://icons.duckduckgo.com/ip3/{domain}.ico"
            if save_icon(ddg_url, icon_path):
                print("✔ 來自 DuckDuckGo Icons")
                success = True

        # 5️⃣ Icon Horse（最後保底）
        if not success:
            iconhorse_url = f"https://icon.horse/icon/{domain}"
            if save_icon(iconhorse_url, icon_path):
                print("✔ 來自 Icon Horse")
                success = True

        if not success:
            print("✘ 所有方式都失敗，請手動補")
