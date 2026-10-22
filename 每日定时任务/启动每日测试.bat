@echo off
chcp 936 >nul
setlocal
cd /d "%~dp0"
title 固德来健康 - 每日UI自动化测试

set "PYEXE=python"
"%PYEXE%" --version >nul 2>&1
if errorlevel 1 set "PYEXE=C:\Users\74515\AppData\Local\Programs\Python\Python311\python.exe"

echo 使用解释器: %PYEXE%
echo.
"%PYEXE%" "%~dp0daily_runner.py" %*
set "RC=%errorlevel%"

echo.
echo ============================================================
echo  执行结束（返回码 %RC%）。窗口保持打开，可向上滚动查看详情。
echo  日志目录: C:\Users\74515\Desktop\UI自动化测试_体验版\log\每日执行
echo ============================================================
echo 按任意键关闭窗口...
pause >nul
exit /b %RC%
