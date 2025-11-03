@echo off
rem === 手动清理日志目录 ===
setlocal enabledelayedexpansion
set "LIST_FILE=%~dp0截图存储目录.txt"

if not exist "%LIST_FILE%" (
    echo 找不到目录清单：%LIST_FILE%
    pause
    exit /b
)

echo.
echo 准备清理以下目录（按任意键继续，Ctrl+C 取消）：
echo ============================================
for /f "usebackq delims=" %%D in ("%LIST_FILE%") do echo %%D
echo ============================================
pause >nul

for /f "usebackq delims=" %%D in ("%LIST_FILE%") do (
    if exist "%%~D" (
        echo 【清理】 %%D
        rem 先删子目录，再删文件
        for /f "delims=" %%F in ('dir /b /ad "%%D\*" 2^>nul') do rd /s /q "%%D\%%F"
        for /f "delims=" %%F in ('dir /b /a-d "%%D\*" 2^>nul') do del /f /q "%%D\%%F"
    ) else (
        echo 【跳过】 %%D  目录不存在
    )
)

echo.
echo 全部处理完成！
pause