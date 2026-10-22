---
name: "playwrightcli"
description: "Playwright 命令行（CLI）自动化测试技能。当用户需要在 UI 自动化测试项目中执行浏览器自动化、生成/运行 Playwright 脚本、录制测试用例、安装浏览器驱动、生成测试报告或截图时调用。Invoke when user asks to run Playwright, record tests, install browsers, or do UI automation via the Playwright CLI."
---

# Playwright CLI 自动化测试技能

本技能封装 Playwright 命令行工具（已全局安装 `playwright@1.61.1`，Node v24.15.0），用于在本项目的 UI 自动化测试工作流中驱动浏览器完成端到端测试。

## 环境确认

- 全局 Playwright：`playwright@1.61.1`
- Node 版本：`v24.15.0`
- 浏览器驱动：执行前先确认已安装，未安装则运行 `playwright install chromium`（或 `playwright install --with-deps chromium` 以安装系统依赖）
- 项目根目录：`UI自动化测试_体验版`（含 `friends/`、`login/`、`Health_records/`、`Device_Management/`、`Room_management/`、`index/`、`report/` 等模块）

## 常用 CLI 命令

| 命令 | 作用 |
|------|------|
| `playwright install chromium` | 安装 Chromium 浏览器驱动 |
| `playwright install --with-deps chromium` | 安装驱动 + 系统依赖（需管理员） |
| `playwright codegen <url>` | 打开录制器，访问 URL 并生成测试脚本 |
| `playwright codegen --browser chromium --output tests/spec.py <url>` | 录制并直接输出到文件 |
| `playwright test` | 运行项目中的测试（需 pytest-playwright 或 @playwright/test） |
| `playwright show-report` | 打开本地 HTML 测试报告 |
| `playwright screenshot <url> out.png` | 对指定 URL 截图 |
| `playwright --version` | 查看版本 |

## 典型工作流

### 1. 首次部署 / 环境校验
```bash
playwright --version
playwright install chromium
```

### 2. 录制测试用例
```bash
# 进入对应模块目录后录制
cd friends
playwright codegen --browser chromium --output py_friends_test.spec.py https://目标地址
```
录制完成后，将生成的脚本与现有 `py_friends.py` 等模块逻辑对齐，补充断言与数据清理。

### 3. 运行与报告
```bash
# Python 项目（pytest + pytest-playwright）
pip install pytest-playwright
playwright install chromium
pytest --html=report/result.html --self-contained-html

# 或仅截图验证
playwright screenshot https://目标地址 report/login_check.png
```

### 4. 与现有批处理脚本协同
项目已存在 `全流程测试.bat`、`自动检查报告.bat`、`清理执行截图.bat`。可在这些脚本中追加 Playwright CLI 步骤，例如：
```bat
call playwright install chromium
playwright screenshot https://localhost:port/login report/login.png
```

## 注意事项
- 浏览器驱动需与 Playwright 版本匹配，升级后务必重新 `playwright install`。
- 截图/报告统一输出到 `report/` 或 `截图存储目录.txt` 指定的目录，避免散落。
- 涉及登录态、验证码等需人工介入的环节，先截图交人工确认，再继续自动化。
- 若执行报 `Executable doesn't exist`，运行 `playwright install` 补全驱动。
