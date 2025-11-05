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
                logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/logout/log",
                devices=[device_url],
                project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/logout"
            )


    # ----------- 退出登录-------------
    def log_out(self):
        touch(Template(r"tpl1754469208242.png", record_pos=(0.369, 1.006), resolution=(1440, 3200)))
        touch(Template(r"tpl1761637806363.png", threshold=0.9000000000000001, record_pos=(0.434, -0.748), resolution=(1176, 2480)))
        touch(Template(r"tpl1754469240202.png", record_pos=(-0.008, 0.989), resolution=(1440, 3200)))
        touch(Template(r"tpl1754469252935.png", record_pos=(0.169, 0.075), resolution=(1440, 3200)))
        sleep(1.0)

        assert_exists(Template(r"tpl1754469264876.png", threshold=0.9500000000000002, record_pos=(0.025, -0.978), resolution=(1440, 3200)), "退出登录成功")
    
    def run_all_tests(self):
        """运行所有测试流程"""
        try:

            print("开始执行退出登录测试...")
            self.log_out()
        
            print("所有测试执行完成！")
              
        finally:
        # 生成报告
             self.generate_report()


    def generate_report(self):

        old_report = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs\py_logout.log'
        export_dir = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs'

    # ---- 1. 强制删除旧报告目录 ----
        if os.path.exists(old_report):
        # 先把只读属性去掉，再删
            def readonly_handler(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(old_report, onerror=readonly_handler)
        os.makedirs(export_dir, exist_ok=True)
        h1 = LogToHtml(script_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\logout\py_logout.py', log_root=r"C:\Users\74515\Desktop\UI自动化测试_体验版\logout\log", export_dir=r"C:\Users\74515\Desktop\UI自动化测试_体验版\docs" ,logfile=r'C:\Users\74515\Desktop\UI自动化测试_体验版\logout\log\log.txt', lang='zh', plugins=None)
        h1.report()


            

# 主程序入口
if __name__ == "__main__":
    automation = LoginAutomation()
    automation.run_all_tests()


