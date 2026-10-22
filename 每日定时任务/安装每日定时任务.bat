@echo off
chcp 936 >nul
setlocal
title 安装 / 更新每日定时任务

set "RUN_TIME=09:00"
if not "%~1"=="" set "RUN_TIME=%~1"
set "TASK_NAME=固德来健康-每日UI自动化"
set "TARGET=%~dp0启动每日测试.bat"

echo ============================================================
echo   计划任务设置
echo     任务名   : %TASK_NAME%
echo     执行时间 : 每天 %RUN_TIME%
echo     执行对象 : %TARGET%
echo     运行方式 : 仅在你登录 Windows 时运行（这样才会弹出窗口）
echo ============================================================
echo.

schtasks /Create /TN "%TASK_NAME%" /TR "\"%TARGET%\"" /SC DAILY /ST %RUN_TIME% /IT /RL LIMITED /F
if errorlevel 1 (
    echo.
    echo [失败] 创建计划任务失败，请右键“以管理员身份运行”本文件后重试。
    goto :end
)

echo.
echo [成功] 已设置为每天 %RUN_TIME% 自动执行。
echo        到时会自动弹出一个独立窗口，实时显示每一步执行详情；
echo        执行结束后窗口保持打开，并同时写入日志文件。
echo.
choice /C YN /M "现在马上试跑一次，看看窗口效果"
if errorlevel 2 goto :end
schtasks /Run /TN "%TASK_NAME%"

:end
echo.
pause
exit /b 0
