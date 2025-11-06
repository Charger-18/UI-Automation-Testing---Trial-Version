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

class FriendsAutomation:
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
                logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/friends/log",
                devices=[device_url],
                project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/friends"
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
    
    # ----------- 添加亲友 -------------
    def add_friends(self):
        touch(Template(r"tpl1754459694986.png", threshold=0.6499999999999999, record_pos=(0.373, 1.007), resolution=(1440, 3200)))
        touch(Template(r"tpl1754360830886.png", record_pos=(-0.12, -0.6), resolution=(1440, 2560)))
        touch(Template(r"tpl1754360842727.png", record_pos=(-0.249, -0.693), resolution=(1440, 2560)))
        sleep(1.0)
        touch(Template(r"tpl1754459740608.png", target_pos=8, record_pos=(-0.281, -0.266), resolution=(1440, 3200)))
        sleep(1.0)
        text("13011111111")
        
        if not self.safe_touch(Template(r"tpl1761639040673.png", record_pos=(-0.26, 0.166), resolution=(1176, 2480))):
            self.safe_touch(Template(r"tpl1754459781833.png", target_pos=8, record_pos=(-0.287, -0.023), resolution=(1440, 3200)))
        
        sleep(1.0)
        text("1234")
        sleep(1.0)
        touch(Template(r"tpl1754459795155.png", target_pos=8, record_pos=(-0.323, 0.24), resolution=(1440, 3200)))
        sleep(1.0)
        touch(Template(r"tpl1762235377430.png", threshold=0.9, record_pos=(-0.003, 0.747), resolution=(1176, 2480)))

        touch(Template(r"tpl1754358321706.png", record_pos=(0.451, 0.515), resolution=(1440, 2560)))
        touch(Template(r"tpl1754459812320.png", target_pos=8, record_pos=(-0.326, 0.504), resolution=(1440, 3200)))
        text("儿子")
        touch(Template(r"tpl1761639233201.png", record_pos=(-0.009, -0.423), resolution=(1176, 2480)))
        touch(Template(r"tpl1761639240018.png", record_pos=(-0.002, 0.909), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761639303967.png", record_pos=(0.014, -0.144), resolution=(1176, 2480)), "添加亲友成功")
    
    # ----------- 分享亲友 -------------
    def share_friends(self):
        touch(Template(r"tpl1754375443711.png", record_pos=(0.241, -0.69), resolution=(1440, 2560)))
        touch(Template(r"tpl1754482488925.png", target_pos=6, record_pos=(-0.008, -0.247), resolution=(1440, 3200)))
        touch(Template(r"tpl1754375551879.png", record_pos=(-0.345, 0.65), resolution=(1440, 2560)))
        touch(Template(r"tpl1754375565408.png", rgb=True, record_pos=(0.24, 0.828), resolution=(1440, 2560)))
        touch(Template(r"tpl1754375590775.png", record_pos=(-0.349, -0.179), resolution=(1440, 2560)))
        text("13011111111")
        touch(Template(r"tpl1754375624810.png", record_pos=(-0.364, -0.027), resolution=(1440, 2560)))
        text("1234")
        touch(Template(r"tpl1754375887501.png", record_pos=(-0.226, 0.083), resolution=(1440, 2560)))
        assert_not_exists(Template(r"tpl1754482593260.png", record_pos=(-0.013, -0.435), resolution=(1440, 3200)), "字段无报错")
    
    # ----------- 删除亲友 -------------
    def delete_friends(self):
        touch(Template(r"tpl1761639303967.png", record_pos=(0.014, -0.144), resolution=(1176, 2480)))
        touch(Template(r"tpl1754535937214.png", record_pos=(-0.001, 0.973), resolution=(1440, 3200)))
        touch(Template(r"tpl1754535950784.png", record_pos=(0.169, 0.074), resolution=(1440, 3200)))
        assert_not_exists(Template(r"tpl1761639303967.png", threshold=0.8999999999999999, record_pos=(0.014, -0.144), resolution=(1176, 2480)), "删除成功")
    
    def run_all_tests(self):
        """运行所有测试流程"""
        try:
            print("开始执行回归首页测试...")
            self.start_check()
            print("开始执行添加亲友测试...")
            self.add_friends()
            print("开始执行分享亲友测试...")
#             self.share_friends()
            print("开始执行删除亲友测试...")
            self.delete_friends()
            print("所有测试执行完成！")
        finally:
            # 生成报告
            self.generate_report()
    
    def generate_report(self):
        old_report = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs\py_friends.log'
        export_dir = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs'
        
        # ---- 1. 强制删除旧报告目录 ----
        if os.path.exists(old_report):
            # 先把只读属性去掉，再删
            def readonly_handler(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(old_report, onerror=readonly_handler)
        
        os.makedirs(export_dir, exist_ok=True)
        h1 = LogToHtml(script_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\friends\py_friends.py', log_root=r"C:\Users\74515\Desktop\UI自动化测试_体验版\friends\log", export_dir=r"C:\Users\74515\Desktop\UI自动化测试_体验版\docs", logfile=r'C:\Users\74515\Desktop\UI自动化测试_体验版\friends\log\log.txt', lang='zh', plugins=None)
        h1.report()

# 主程序入口
if __name__ == "__main__":
    automation = FriendsAutomation()
    automation.run_all_tests()