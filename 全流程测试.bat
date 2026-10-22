@echo off
chcp 936 >nul
setlocal
cd /d "%~dp0"
title 固德来健康 - 全流程测试

echo ============================================================
echo  全流程测试已统一由 daily_runner.py 驱动
echo  窗口会实时显示每一步的执行详情，并与日志同步落盘
echo ============================================================
echo.

call "%~dp0每日定时任务\启动每日测试.bat" %*
exit /b %errorlevel%
