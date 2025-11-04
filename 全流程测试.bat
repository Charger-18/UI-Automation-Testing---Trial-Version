@echo off

setlocal enabledelayedexpansion

:: 设置工作目录为当前脚本所在目录
cd /d "%~dp0"

:: 设置日志文件路径（确保日志保存在log目录）
set "LOG_DIR=C:\Users\74515\Desktop\UI自动化测试_体验版\log"
set "LOG_FILE=%LOG_DIR%\test_log_%date:/=%%time::=%.txt"
set "LOG_FILE=%LOG_FILE: =%"
set "MAIN_LOG=%LOG_FILE%"

:: 设置脚本目录路径（单独变量）
set "SCRIPT_DIR=C:\Users\74515\Desktop\UI自动化测试_体验版"

:: 创建日志目录（如果不存在）
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: 获取当前时间（优化格式）
set "datetime=%date% %time%"
set "datetime=%datetime:/=-%"
set "datetime=%datetime: =0%"

:: 开始记录日志
echo [%datetime%] 开始执行所有测试脚本...
echo [%datetime%] 开始执行所有测试脚本... > "%LOG_FILE%"
echo. >> "%LOG_FILE%"

:: 执行登录测试
echo ========== 开始执行登录测试 ==========
echo [%datetime%] ========== 开始执行登录测试 ========== >> "%LOG_FILE%"
call "%SCRIPT_DIR%\login\登录测试.bat" >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"

:: 执行亲友测试
echo ========== 开始执行亲友测试 ==========
echo [%datetime%] ========== 开始执行亲友测试 ========== >> "%LOG_FILE%"
call "%SCRIPT_DIR%\friends\亲友测试.bat" >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"


:: 执行房间管理测试
echo ========== 开始执行房间管理测试 ==========
echo [%datetime%] ========== 开始执行房间管理测试 ========== >> "%LOG_FILE%"
call "%SCRIPT_DIR%\Room_management\房间管理.bat" >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"



:: 执行健康档案测试
echo ========== 开始执行健康档案测试 ==========
echo [%datetime%] ========== 开始执行健康档案测试 ========== >> "%LOG_FILE%"
call "%SCRIPT_DIR%\Health_records\健康档案.bat" >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"




:: 完成
echo [%datetime%] 所有测试执行完成 >> "%LOG_FILE%"
echo 所有测试执行完成




:: 第二步：自动检查报告
echo ========== 第二步：自动检查测试报告 ==========
echo [%datetime%] ========== 第二步：自动检查测试报告 ========== >> "%MAIN_LOG%"
call "%SCRIPT_DIR%\自动检查报告.bat" >> "%MAIN_LOG%" 2>&1

set CHECK_RESULT=%errorlevel%
set "REPORT_DIR=C:\Users\74515\Desktop\UI自动化测试_体验版\report"

:SUMMARY
echo. >> "%MAIN_LOG%"
echo ========== 测试流程总结 ========== >> "%MAIN_LOG%"
echo 完成时间: %date% %time% >> "%MAIN_LOG%"
echo 日志文件: %MAIN_LOG% >> "%MAIN_LOG%"
echo 报告目录: %REPORT_DIR% >> "%MAIN_LOG%"

if %CHECK_RESULT% equ 0 (
    echo  完整测试流程执行成功！ >> "%MAIN_LOG%"
    echo  完整测试流程执行成功！
) else (
    echo  测试流程存在问题，请检查日志 >> "%MAIN_LOG%"
    echo  测试流程存在问题，请检查日志
)

echo.
echo 详细日志: %MAIN_LOG%
echo 报告目录: %REPORT_DIR%



rem ===== 1. 自动检测 =====
echo.
echo ========== 开始自动检测测试报告 ==========
call "%SCRIPT_DIR%\自动检查报告.bat"
set CHECK_RESULT=%errorlevel%

rem ===== 2. 自动提交 docs =====
echo.
echo ========== 自动提交 docs 到 GitHub ========== >> "%MAIN_LOG%"
cd /d "C:\Users\74515\Desktop\UI自动化测试_体验版\docs"

rem 拉取最新，避免冲突
git pull origin main --allow-unrelated-histories >> "%MAIN_LOG%" 2>&1

rem 添加全部变更
git add -A >> "%MAIN_LOG%" 2>&1

rem 生成带时间戳的提交信息
set "COMMIT_MSG=自动化测试完成 %date:/=-% %time:~0,2%:%time:~3,2%:%time:~6,2%"
git commit -m "%COMMIT_MSG%" >> "%MAIN_LOG%" 2>&1

rem 推送
git push origin main >> "%MAIN_LOG%" 2>&1
set GIT_RESULT=%errorlevel%

if %GIT_RESULT% equ 0 (
    echo  docs 已自动提交到 GitHub
    echo  docs 已自动提交到 GitHub >> "%MAIN_LOG%"
) else (
    echo  提交失败，请检查网络或仓库配置
    echo  提交失败，请检查网络或仓库配置 >> "%MAIN_LOG%"
)

rem 返回脚本目录，方便后续操作
cd /d "%SCRIPT_DIR%"


pause
exit /b 0