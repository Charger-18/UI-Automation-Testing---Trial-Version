@echo off
chcp 936 >nul
setlocal
title 卸载每日定时任务
set "TASK_NAME=固德来健康-每日UI自动化"

echo 正在删除计划任务: %TASK_NAME%
schtasks /Delete /TN "%TASK_NAME%" /F
if errorlevel 1 (
    echo [提示] 删除失败或任务不存在。
) else (
    echo [成功] 已取消每天自动执行。
)
echo.
pause
exit /b 0
