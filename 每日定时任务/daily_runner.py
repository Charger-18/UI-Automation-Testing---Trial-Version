# -*- coding: utf-8 -*-
"""
固德来健康 APP - 每日 UI 自动化执行器
====================================
用途：按固定顺序执行各模块 airtest 脚本，实时在窗口打印执行详情，
      同时把全过程写入带日期的日志文件，并在结束时给出汇总表。

特点：
  1) 每一步都有 [开始]/[结束] 时间、耗时、返回码，失败不会中断后续步骤
  2) 窗口实时可见 + 日志同步落盘（两处内容一致，事后可回看）
  3) 执行前自动检查 adb 设备（MuMu 未启动会给出明确提示）
  4) 结束后输出汇总表，并指引 Airtest HTML 报告与截图目录

用法：
  python daily_runner.py              # 完整执行
  python daily_runner.py --dry-run    # 只打印计划，不执行
  python daily_runner.py --demo       # 用模拟步骤验证窗口/日志效果
  python daily_runner.py --only 登录测试
"""
import os
import sys
import time
import argparse
import datetime
import subprocess
import shutil

# ========================= 可配置区域 =========================
# 工程根目录自动推导：本脚本位于 <ROOT>\每日定时任务\ 下，换机器无需改路径
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
DEVICE_SERIAL = "127.0.0.1:16384"          # MuMu 模拟器 adb 地址
LOG_DIR = os.path.join(ROOT, "log", "每日执行")
DOCS_DIR = os.path.join(ROOT, "docs")
SUMMARY_LATEST = os.path.join(LOG_DIR, "最近一次执行.txt")

# 模块顺序：(显示名, 相对路径)  —— 文件名以磁盘实际情况为准
MODULES = [
    ("登出准备",   r"logout\登出测试.bat"),
    ("账号登录",   r"login\登录测试.bat"),
    ("亲友",       r"friends\亲友测试.bat"),
    ("房间管理",   r"Room_management\房间管理.bat"),
    ("健康档案",   r"Health_records\健康档案.bat"),
    ("登出收尾",   r"logout\登出测试.bat"),
]

# 执行完后是否跑一次报告检查（check_reports.py）
ENABLE_REPORT_CHECK = True
# =============================================================

SYS_PY = r"C:\Users\74515\AppData\Local\Programs\Python\Python311\python.exe"
SEP = "=" * 66
SUB = "-" * 66

ST_OK, ST_FAIL, ST_SKIP, ST_DRY, ST_WARN = "成功", "失败", "跳过", "干跑", "警告"


def dwidth(s):
    """按终端显示宽度计算字符串列宽（中文占两格）"""
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in s)


def pad(s, width):
    return s + " " * max(width - dwidth(s), 0)



def now():
    return datetime.datetime.now()


def ts():
    return now().strftime("%H:%M:%S")


class Tee:
    """同时输出到窗口与日志文件"""

    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.fh = open(path, "w", encoding="utf-8", errors="replace", newline="\n")

    def w(self, text=""):
        try:
            print(text)
        except UnicodeEncodeError:
            print(text.encode(sys.stdout.encoding or "gbk", "replace").decode(sys.stdout.encoding or "gbk"))
        try:
            sys.stdout.flush()
        except Exception:
            pass
        self.fh.write(text + "\n")
        self.fh.flush()

    def close(self):
        try:
            self.fh.close()
        except Exception:
            pass


def find_adb():
    p = shutil.which("adb")
    if p:
        return p
    candidate = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Android", "Sdk", "platform-tools", "adb.exe")
    return candidate if os.path.exists(candidate) else None


def adb_devices(adb):
    try:
        out = subprocess.run([adb, "devices"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True, encoding="gbk", errors="replace", timeout=30).stdout
    except Exception as e:
        return [], str(e)
    devs = [ln.split("\t")[0].strip() for ln in out.splitlines() if "\tdevice" in ln]
    return devs, out


def preflight(tee, dry=False):
    """返回 (是否通过, 说明)"""
    tee.w("[预检] 执行环境")
    py = sys.executable
    tee.w("        Python : %s" % py)
    try:
        import airtest  # noqa: F401
        tee.w("        airtest: %s" % getattr(__import__("airtest"), "__version__", "已安装"))
    except Exception:
        return False, "当前 Python 未安装 airtest，请用系统 Python 3.11 运行（启动脚本已自动处理）"

    adb = find_adb()
    if not adb:
        return False, "未找到 adb，请确认 Android SDK platform-tools 已配置"
    tee.w("        adb    : %s" % adb)

    devs, raw = adb_devices(adb)
    if not devs:
        tee.w("        设备   : 未检测到，尝试连接 %s ..." % DEVICE_SERIAL)
        if not dry:
            subprocess.run([adb, "connect", DEVICE_SERIAL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            devs, raw = adb_devices(adb)
    if not devs:
        return False, "没有在线的 adb 设备。请先启动 MuMu 模拟器，等桌面出现后再重试。"
    tee.w("        设备   : %s" % ", ".join(devs))
    if DEVICE_SERIAL.split(":")[0] == "127.0.0.1" and DEVICE_SERIAL not in devs:
        tee.w("        [提醒] 目标设备 %s 不在列表中，脚本可能连到其它设备" % DEVICE_SERIAL)
    return True, "ok"


def run_step(tee, label, bat_rel, dry=False):
    """执行一个模块，实时输出并返回 (状态, 耗时秒, 尾部输出)"""
    bat_abs = os.path.join(ROOT, bat_rel)
    if not os.path.exists(bat_abs):
        tee.w("  [跳过] 找不到脚本：%s" % bat_abs)
        return ST_SKIP, 0.0, ["file not found: %s" % bat_rel]
    if dry:
        tee.w("  [干跑] 将执行：%s" % bat_abs)
        return ST_DRY, 0.0, []

    tee.w("  [开始] %s  %s" % (ts(), bat_abs))
    t0 = time.time()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "gbk"
    tail = []
    try:
        proc = subprocess.Popen(
            ["cmd", "/c", bat_abs],
            cwd=os.path.dirname(bat_abs),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="gbk",
            errors="replace",
            bufsize=1,
            env=env,
        )
        for line in proc.stdout:
            line = line.rstrip("\r\n")
            if not line.strip():
                continue
            tee.w("        | " + line)
            tail.append(line)
            if len(tail) > 25:
                tail.pop(0)
        rc = proc.wait()
    except KeyboardInterrupt:
        raise
    except Exception as e:
        tee.w("        !! 调用异常：%s" % e)
        return ST_FAIL, time.time() - t0, [str(e)]

    cost = time.time() - t0
    status = ST_OK if rc == 0 else ST_FAIL
    tee.w("  [%s] %s  返回码=%s  耗时=%s" % (status, ts(), rc, fmt_dur(cost)))
    return status, cost, tail


def fmt_dur(sec):
    sec = int(round(sec))
    return "%02d:%02d" % (sec // 60, sec % 60)


def ensure_runtime():
    """确保当前解释器带 airtest，否则自动切到系统 Python 3.11 重新执行"""
    try:
        import airtest  # noqa: F401
        return
    except Exception:
        pass
    if os.path.exists(SYS_PY) and os.path.normcase(os.path.abspath(sys.executable)) != os.path.normcase(SYS_PY):
        print("[环境] 当前解释器缺少 airtest，自动切换到：%s" % SYS_PY)
        sys.stdout.flush()
        os.execv(SYS_PY, [SYS_PY, os.path.abspath(__file__)] + sys.argv[1:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只打印执行计划")
    ap.add_argument("--demo", action="store_true", help="用模拟步骤验证输出效果")
    ap.add_argument("--only", default="", help="只执行某个模块（按显示名模糊匹配）")
    ap.add_argument("--no-report", action="store_true", help="跳过报告检查")
    args = ap.parse_args()

    ensure_runtime()

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, now().strftime("%Y-%m-%d_%H%M%S") + ".log")
    tee = Tee(log_path)

    started = now()
    tee.w(SEP)
    tee.w("  固德来健康 APP · 每日 UI 自动化测试")
    tee.w("  开始时间：%s" % started.strftime("%Y-%m-%d %H:%M:%S"))
    tee.w("  工程目录：%s" % ROOT)
    tee.w("  运行日志：%s" % log_path)
    tee.w(SEP)
    tee.w("")

    results = []

    if args.demo:
        tee.w("[演示模式] 不操作模拟器，只用模拟步骤验证窗口显示与日志落盘")
        demo_steps = [(u"演示步骤A", ST_OK), (u"演示步骤B", ST_OK), (u"演示步骤C", ST_FAIL)]
        for i, (name, expect) in enumerate(demo_steps, 1):
            tee.w(SUB)
            tee.w("(%d/%d) %s" % (i, len(demo_steps), name))
            tee.w("  [开始] %s" % ts())
            time.sleep(0.6)
            tee.w("         | 模拟输出：正在定位模板 tpl1754461722176.png")
            time.sleep(0.4)
            tee.w("         | 模拟输出：断言结果 = 期望命中")
            tee.w("  [%s] %s  耗时=00:01" % (expect, ts()))
            results.append((name, expect, 1.0, []))
    else:
        ok, msg = preflight(tee, dry=args.dry_run)
        if not ok:
            tee.w("")
            tee.w("[中止] " + msg)
            tee.w(SEP)
            tee.close()
            return 2

        steps = MODULES
        if args.only:
            steps = [m for m in MODULES if args.only in m[0]]
            if not steps:
                tee.w("[中止] 没有匹配 '%s' 的模块" % args.only)
                tee.close()
                return 2

        tee.w("共 %d 个模块，按顺序执行（单步失败不影响后续）" % len(steps))
        for i, (label, rel) in enumerate(steps, 1):
            tee.w("")
            tee.w(SUB)
            tee.w("(%d/%d) %s" % (i, len(steps), label))
            status, cost, tail = run_step(tee, label, rel, dry=args.dry_run)
            results.append((label, status, cost, tail))

        if ENABLE_REPORT_CHECK and not args.dry_run and not args.no_report:
            chk = os.path.join(ROOT, "check_reports.py")
            if os.path.exists(chk):
                tee.w("")
                tee.w(SUB)
                tee.w("报告检查")
                tee.w("  [开始] %s" % ts())
                t0 = time.time()
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "gbk"
                try:
                    proc = subprocess.Popen(
                        [sys.executable, chk, DOCS_DIR, os.path.join(DOCS_DIR, "report_summary.txt")],
                        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        universal_newlines=True, encoding="gbk", errors="replace", env=env)
                    tail = []
                    for line in proc.stdout:
                        line = line.rstrip("\r\n")
                        if line.strip():
                            tee.w("        | " + line)
                            tail.append(line)
                    rc = proc.wait()
                    st = ST_OK if rc == 0 else ST_WARN
                except Exception as e:
                    rc, st, tail = -1, ST_WARN, [str(e)]
                tee.w("  [%s] %s  返回码=%s  耗时=%s" % (st, ts(), rc, fmt_dur(time.time() - t0)))
                results.append(("报告检查", st, time.time() - t0, tail))

    # ---------------- 汇总 ----------------
    ok_n = sum(1 for r in results if r[1] == ST_OK)
    fail_n = sum(1 for r in results if r[1] == ST_FAIL)
    skip_n = sum(1 for r in results if r[1] == ST_SKIP)
    other = len(results) - ok_n - fail_n - skip_n
    total = (now() - started).total_seconds()

    lines = []
    lines.append("")
    lines.append(SEP)
    lines.append("  执行汇总   %s" % started.strftime("%Y-%m-%d %H:%M:%S"))
    lines.append(SEP)
    lines.append("  %s %s %s" % (pad(u"步骤", 14), pad(u"结果", 8), u"耗时"))
    lines.append("  " + "-" * 40)
    for label, status, cost, _tail in results:
        lines.append("  %s %s %s" % (pad(label, 14), pad(status, 8), fmt_dur(cost)))
    lines.append("  " + "-" * 40)
    lines.append("  合计 %d 步：成功 %d / 失败 %d / 跳过 %d%s   总耗时 %s"
                 % (len(results), ok_n, fail_n, skip_n, (" / 其它 %d" % other) if other else "", fmt_dur(total)))
    lines.append("")
    lines.append("  Airtest 报告 : %s" % os.path.join(DOCS_DIR, "index.html"))
    lines.append("  报告检查汇总 : %s" % os.path.join(DOCS_DIR, "report_summary.txt"))
    lines.append("  本次执行日志 : %s" % log_path)
    lines.append(SEP)

    failed = [r for r in results if r[1] == ST_FAIL and r[3]]
    if failed:
        lines.append("")
        lines.append("  失败步骤尾部输出（便于快速定位）：")
        for label, _s, _c, tail in failed:
            lines.append("  --- %s ---" % label)
            for ln in tail[-10:]:
                lines.append("      " + ln)
        lines.append(SEP)

    for ln in lines:
        tee.w(ln)

    # 固定名字的“最近一次执行”摘要，方便随时打开
    try:
        with open(SUMMARY_LATEST, "w", encoding="utf-8", errors="replace", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
    except Exception:
        pass

    tee.close()
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[中断] 用户取消执行")
        sys.exit(130)
