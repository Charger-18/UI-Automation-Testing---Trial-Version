@echo off
setlocal enabledelayedexpansion

:: 设置工作目录为脚本所在目录
cd /d "%~dp0"

:: 设置目录路径
set "REPORT_DIR=%~dp0report"
set "LOG_DIR=%~dp0log"
set "SCRIPT_DIR=%~dp0"

:: 创建日志目录
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: 设置时间戳（仅用于日志文件）
set "date_str=%date:~0,4%%date:~5,2%%date:~8,2%"
set "time_str=%time:~0,2%%time:~3,2%%time:~6,2%"
set "datetime=%date_str%_%time_str%"
set "datetime=%datetime: =0%"

:: 设置日志文件和汇总文件
set "CHECK_LOG=%LOG_DIR%\report_check_%datetime%.log"
set "SUMMARY_FILE=%REPORT_DIR%\report_summary.txt"  :: 固定文件名

echo [%date% %time%] 开始自动检查测试报告...
echo [%date% %time%] 开始自动检查测试报告... > "%CHECK_LOG%"

:: 检查Python脚本是否存在
if not exist "check_reports.py" (
    echo  错误: 找不到 check_reports.py 文件 >> "%CHECK_LOG%"
    echo  错误: 找不到 check_reports.py 文件
    pause
    exit /b 1
)

:: 检查报告目录是否存在
if not exist "%REPORT_DIR%" (
    echo  错误: 找不到报告目录 %REPORT_DIR% >> "%CHECK_LOG%"
    echo  错误: 找不到报告目录 %REPORT_DIR%
    pause
    exit /b 1
)

echo 正在检查报告目录: %REPORT_DIR% >> "%CHECK_LOG%"
echo 正在检查报告目录: %REPORT_DIR%

:: 运行报告检查脚本
python "check_reports.py" "%REPORT_DIR%" "%SUMMARY_FILE%" >> "%CHECK_LOG%" 2>&1

set CHECK_RESULT=%errorlevel%

echo. >> "%CHECK_LOG%"
echo 检查完成时间: %date% %time% >> "%CHECK_LOG%"

:: 显示结果
if %CHECK_RESULT% equ 0 (
    echo  所有测试报告检查通过！
    echo  所有测试报告检查通过！ >> "%CHECK_LOG%"
) else (
    echo  存在失败的测试报告，请查看详细日志
    echo  存在失败的测试报告 >> "%CHECK_LOG%"
)

echo.
echo 详细日志文件: %CHECK_LOG%
if exist "%SUMMARY_FILE%" echo 汇总报告: %SUMMARY_FILE%
echo.

exit /b %CHECK_RESULT%