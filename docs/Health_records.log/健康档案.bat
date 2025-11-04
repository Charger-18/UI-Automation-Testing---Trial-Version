@echo off
cd /d "C:\Users\74515\Desktop\UI自动化测试_体验版\Health_records"

title 健康档案测试---体验版
python Health_records.py



airtest report Health_records.py --log_root "C:\Users\74515\Desktop\UI自动化测试_体验版\Health_records\log" --export "C:\Users\74515\Desktop\UI自动化测试_体验版\report" --lang zh
