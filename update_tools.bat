@echo off
cd C:\Users\Hank\Desktop\software-list

echo === 抓圖示 ===
python fetch_icons_auto_commit.py

echo === 同步遠端（避免重灌問題）===
git pull --rebase

echo === 提交更新 ===
git add .
git commit -m "auto update %date% %time%"

echo === 推送到 GitHub ===
git push

pause
