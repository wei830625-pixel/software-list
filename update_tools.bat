@echo off
cd C:\Users\hank\Desktop\software-list

REM 抓圖
python fetch_icons_auto_commit.py

REM Git 提交 & 推送
git add .
git commit -m "auto update %date% %time%"
git push

pause
