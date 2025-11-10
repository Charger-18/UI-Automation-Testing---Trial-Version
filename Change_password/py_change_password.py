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

class ChangePasswordAutomation:
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
                logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/Change_password/log",
                devices=[device_url],
                project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/Change_password"
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
    
    # ----------- 回归首页 -------------
    def start_check(self):
        self.safe_touch(Template(r"tpl1754634667443.png", record_pos=(-0.287, -0.897), resolution=(1176, 2480)))
        
        # 验证登录状态
        if not self.safe_assert_exists(Template(r"tpl1760961005997.png", record_pos=(-0.31, -0.978), resolution=(1440, 3200)), "账号已登录"):
            print("未找到目标图像，重新执行safe_touch...")
            self.safe_touch(Template(r"tpl1754634667443.png", record_pos=(-0.287, -0.897), resolution=(1176, 2480)))
            # 重新验证
            if not self.safe_assert_exists(Template(r"tpl1760961005997.png", record_pos=(-0.31, -0.978), resolution=(1440, 3200)), "账号已登录"):
                print("重新执行后仍然失败，但继续执行后续代码...")
            else:
                print("重新执行后验证成功！")
    

    def change_password(self):
        touch(Template(r"tpl1762420797022.png", record_pos=(0.369, 0.876), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762420805794.png", record_pos=(0.435, -0.752), resolution=(1176, 2480)))
        touch(Template(r"tpl1762420816867.png", record_pos=(0.331, -0.387), resolution=(1176, 2480)))
        touch(Template(r"tpl1762420832348.png", threshold=0.8999999999999999, target_pos=6, record_pos=(-0.136, -0.745), resolution=(1176, 2480)))
        text("1234567")
        touch(Template(r"tpl1762420857409.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.136, -0.628), resolution=(1176, 2480)))
        text("1234567")
        touch(Template(r"tpl1762431496440.png", record_pos=(-0.331, -0.625), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1762758662048.png", threshold=0.9500000000000002, record_pos=(-0.003, 0.851), resolution=(1176, 2480)))


        keyevent("back")

        touch(Template(r"tpl1762429359221.png", record_pos=(-0.003, 0.855), resolution=(1176, 2480)))
        touch(Template(r"tpl1762429368738.png", record_pos=(0.179, 0.051), resolution=(1176, 2480)))
        sleep(3.0)

        touch(Template(r"tpl1762429413718.png", record_pos=(-0.032, -0.906), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762429421613.png", record_pos=(-0.008, 0.772), resolution=(1176, 2480)))
        touch(Template(r"tpl1762429433633.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.224, -0.173), resolution=(1176, 2480)))
        text("17660700727")
        touch(Template(r"tpl1762429446797.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.203, -0.02), resolution=(1176, 2480)))
        text("123")
        touch(Template(r"tpl1762429509725.png", threshold=0.8, target_pos=4, record_pos=(-0.009, 0.299), resolution=(1176, 2480)))
        touch(Template(r"tpl1762429525869.png", record_pos=(0.001, 0.173), resolution=(1176, 2480)))
        if not self.safe_assert_exists(Template(r"tpl1762429824371.png", record_pos=(0.008, -0.434), resolution=(1176, 2480)), "修改密码成功"):
            assert_not_exists(Template(r"tpl1762430026371.png", record_pos=(0.005, 0.882), resolution=(1176, 2480)), "修改密码失败")
        touch(Template(r"tpl1762430277754.png", threshold=0.8, target_pos=6, record_pos=(-0.277, -0.013), resolution=(1176, 2480)))
        for i in range(3):
            keyevent("KEYCODE_DEL")
        text("1234567")
        touch(Template(r"tpl1762429525869.png", record_pos=(0.001, 0.173), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1762430360611.png", record_pos=(-0.003, 0.87), resolution=(1176, 2480)), "新密码登录成功")
        assert_exists(Template(r"tpl1762430367630.png", record_pos=(-0.371, -0.902), resolution=(1176, 2480)), "新密码登录成功")
    def recovery(self):
        touch(Template(r"tpl1762430435344.png", record_pos=(0.373, 0.873), resolution=(1176, 2480)))
        touch(Template(r"tpl1762430439584.png", threshold=0.9000000000000001, record_pos=(0.432, -0.75), resolution=(1176, 2480)))
        touch(Template(r"tpl1762430456233.png", record_pos=(0.337, -0.386), resolution=(1176, 2480)))
        touch(Template(r"tpl1762420832348.png", threshold=0.8999999999999999, target_pos=6, record_pos=(-0.136, -0.745), resolution=(1176, 2480)))
        text("123456")
        touch(Template(r"tpl1762420857409.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.136, -0.628), resolution=(1176, 2480)))
        text("123456")
        touch(Template(r"tpl1762431496440.png", record_pos=(-0.331, -0.625), resolution=(1176, 2480)))
        touch(Template(r"tpl1762758662048.png", threshold=0.9500000000000002, record_pos=(-0.003, 0.851), resolution=(1176, 2480)))


        
        

    
    
    def run_all_tests(self):
        """运行所有测试流程"""
        try:
            print("开始执行回归首页测试...")
            self.start_check()
            self.change_password()
            self.recovery()

            print("所有测试执行完成！")
        finally:
            # 生成报告
            self.generate_report()
    
    def generate_report(self):
        old_report = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs\py_change_password.log'
        export_dir = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs'
        
        # ---- 1. 强制删除旧报告目录 ----
        if os.path.exists(old_report):
            # 先把只读属性去掉，再删
            def readonly_handler(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(old_report, onerror=readonly_handler)
        
        os.makedirs(export_dir, exist_ok=True)
        h1 = LogToHtml(script_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\Change_password\py_change_password.py', log_root=r"C:\Users\74515\Desktop\UI自动化测试_体验版\Change_password\log", export_dir=r"C:\Users\74515\Desktop\UI自动化测试_体验版\docs", logfile=r'C:\Users\74515\Desktop\UI自动化测试_体验版\Change_password\log\log.txt', lang='zh', plugins=None)
        h1.report()

# 主程序入口
if __name__ == "__main__":
    automation = ChangePasswordAutomation()
    automation.run_all_tests()