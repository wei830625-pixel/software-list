@echo off
chcp 65001 > nul

cd C:\Users\Hank\Desktop\software-list

echo === 抓圖示 ===
python fetch_icons_auto_commit.py

echo === 暫存本機變更（避免 rebase 失敗）===
git stash push -m "auto stash before pull" > nul

echo === 同步遠端 ===
git pull --rebase

echo === 還原暫存變更 ===
git stash pop > nul

echo === 提交更新 ===
git add .
git commit -m "auto update %date% %time%"

echo === 推送到 GitHub ===
git push

pause
