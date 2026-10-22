@echo off
chcp 936 >nul
setlocal
title 查看最近一次执行详情
set "LOGDIR=%~dp0..\log\每日执行"
set "SRC=%~dp0..\docs"

if not exist "%LOGDIR%" (
    echo 还没有任何执行记录。
    pause
    exit /b 1
)

if exist "%LOGDIR%\最近一次执行.txt" (
    start "" notepad "%LOGDIR%\最近一次执行.txt"
)

for /f "delims=" %%f in ('dir /b /a-d /o-d "%LOGDIR%\*.log" 2^>nul') do (
    start "" notepad "%LOGDIR%\%%f"
    goto :opened
)
:opened

if exist "%SRC%\index.html" (
    start "" "%SRC%\index.html"
) else (
    echo 尚未生成 Airtest HTML 报告。
)

echo 已打开最近一次的日志与报告。
timeout /t 2 >nul
exit /b 0
