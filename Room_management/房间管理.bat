@echo off
cd /d "C:\Users\74515\Desktop\UI自动化测试_体验版\Room_management"

title 房间管理测试
python py_room.py

airtest report py_room.py --log_root "C:\Users\74515\Desktop\UI自动化测试_体验版\Room_management\log" --lang zh --outfile "C:\Users\74515\Desktop\UI自动化测试_体验版\report\py_room_report.html"  

