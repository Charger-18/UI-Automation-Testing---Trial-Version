@echo off
cd /d "C:\Users\74515\Desktop\UI自动化测试_体验版\friends"

title 正在执行Python登录脚本
python py_friends.py

airtest report py_friends.py --log_root "C:\Users\74515\Desktop\UI自动化测试_体验版\friends\log" --lang zh --outfile "C:\Users\74515\Desktop\UI自动化测试_体验版\report\py_friends_report.html"  

