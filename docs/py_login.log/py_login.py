# -*- encoding=utf8 -*-
__author__ = "体验版"
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.error import TargetNotFoundError, AirtestError
from airtest.core.settings import Settings as ST
from airtest.report.report import simple_report, LogToHtml
import subprocess
import time
import os
import shutil
import stat


# 设置全局阙值为0.8
ST.THRESHOLD = 0.8
# 设置全局的超时时长为60s
ST.FIND_TIMEOUT = 10
ST.FIND_TIMEOUT_TMP = 3

class LoginAutomation:
    def __init__(self):
        self.setup_device()
    
    def get_adb_device_url(self):
        result = subprocess.run(
            ["adb", "devices"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True         
        )
        devices = [line.split("\t")[0]
                   for line in result.stdout.splitlines()
                   if "\tdevice" in line]

        if not devices:
            raise RuntimeError("未检测到任何已连接的ADB设备")

        if len(devices) == 1:
            selected = devices[0]
        else:
            print("\n检测到多个设备，请选择:")
            for idx, dev in enumerate(devices, 1):
                print(f"  [{idx}] {dev}")
            try:
                choice = int(input("请输入设备序号: ")) - 1
                selected = devices[choice]
            except (ValueError, IndexError):
                raise ValueError("选择无效，程序退出")

        return f"android://127.0.0.1:5037/{selected}?cap_method=ADBCAP&touch_method=MAXTOUCH&"
    
    def setup_device(self):
        if not cli_setup():
            device_url = self.get_adb_device_url()
            auto_setup(
                __file__,
                logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/login/log",
                devices=[device_url],
                project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/login"
            )

    def safe_touch(self, template):
        """安全点击：尝试点击一次，失败时打印日志并返回 False，不中断后续步骤"""
        try:
            touch(template)
            return True
        except (TargetNotFoundError, AirtestError) as e:
            print(f"[safe_touch] 点击失败：{e}")
            return False
    
    def safe_assert_exists(self, template, msg=None):
        """安全断言（仅执行一次，失败不影响测试报告）"""
        try:
            assert_exists(template, msg)
            return True
        except AssertionError as e:
            print(f"[safe_assert_exists] 断言失败: {str(e)}")
            return False

    # ----------- 快捷登录-------------
    def quick_login(self):
        self.safe_touch(Template(r"tpl1754463699535.png", record_pos=(0.028, -0.973), resolution=(1440, 3200)))
        touch(Template(r"tpl1754461674210.png", target_pos=4, record_pos=(0.001, 0.042), resolution=(1440, 3200)))
        touch(Template(r"tpl1754461692338.png", record_pos=(0.0, -0.077), resolution=(1440, 3200)))
        self.safe_touch(Template(r"tpl1761637161166.png", record_pos=(-0.014, 0.179), resolution=(1176, 2480)))
        sleep(2.0)
        assert_exists(Template(r"tpl1754461722176.png", threshold=0.9, record_pos=(-0.308, -0.976), resolution=(1440, 3200)), "登录成功")

    # ----------- 退出登录-------------
    def log_out(self):
        touch(Template(r"tpl1754469208242.png", record_pos=(0.369, 1.006), resolution=(1440, 3200)))
        touch(Template(r"tpl1761637806363.png", threshold=0.9000000000000001, record_pos=(0.434, -0.748), resolution=(1176, 2480)))
        touch(Template(r"tpl1754469240202.png", record_pos=(-0.008, 0.989), resolution=(1440, 3200)))
        touch(Template(r"tpl1754469252935.png", record_pos=(0.169, 0.075), resolution=(1440, 3200)))
        sleep(1.0)

        assert_exists(Template(r"tpl1754469264876.png", threshold=0.9500000000000002, record_pos=(0.025, -0.978), resolution=(1440, 3200)), "退出登录成功")

    # ----------- 账号登录-------------
    def account_login(self):
        self.safe_touch(Template(r"tpl1754463699535.png", record_pos=(0.028, -0.973), resolution=(1440, 3200)))
        sleep(1.0)
        touch(Template(r"tpl1761637405710.png", record_pos=(-0.005, 0.777), resolution=(1176, 2480)))
        touch(Template(r"tpl1754474063060.png", record_pos=(-0.242, -0.226), resolution=(1440, 3200)))
        text("17660700727")
        touch(Template(r"tpl1754474086904.png", record_pos=(-0.224, -0.085), resolution=(1440, 3200)))
        text("123456")
        touch(Template(r"tpl1754474149149.png", target_pos=4, record_pos=(0.004, 0.205), resolution=(1440, 3200)))
        touch(Template(r"tpl1754545318031.png", record_pos=(-0.002, 0.085), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1754461722176.png", threshold=0.9, record_pos=(-0.308, -0.976), resolution=(1440, 3200)), "登录成功")
    
    def run_all_tests(self):
        """运行所有测试流程"""
        try:
            print("开始执行快捷登录测试...")
#             self.quick_login()
        
            print("开始执行退出登录测试...")
#             self.log_out()
        
            print("开始执行账号登录测试...")
            self.account_login()
        
            print("所有测试执行完成！")
              
        finally:
        # 生成报告
             self.generate_report()


    def generate_report(self):

        old_report = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs\py_login.log'
        export_dir = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs'

    # ---- 1. 强制删除旧报告目录 ----
        if os.path.exists(old_report):
        # 先把只读属性去掉，再删
            def readonly_handler(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(old_report, onerror=readonly_handler)
        os.makedirs(export_dir, exist_ok=True)
        h1 = LogToHtml(script_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\login\py_login.py', log_root=r"C:\Users\74515\Desktop\UI自动化测试_体验版\login\log", export_dir=r"C:\Users\74515\Desktop\UI自动化测试_体验版\docs" ,logfile=r'C:\Users\74515\Desktop\UI自动化测试_体验版\login\log\log.txt', lang='zh', plugins=None)
        h1.report()


            

# 主程序入口
if __name__ == "__main__":
    automation = LoginAutomation()
    automation.run_all_tests()


