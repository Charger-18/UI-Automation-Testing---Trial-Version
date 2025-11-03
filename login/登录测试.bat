@echo off
cd /d "C:\Users\74515\Desktop\UI自动化测试_体验版\login"

title 正在执行Python登录脚本
python py_login.py

airtest report py_login.py --log_root "C:\Users\74515\Desktop\UI自动化测试_体验版\login\log" --lang zh --outfile "C:\Users\74515\Desktop\UI自动化测试_体验版\report\py_login_report.html"  



