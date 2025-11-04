# -*- encoding=utf-8 -*-
__author__ = "体验版"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.error import TargetNotFoundError, AirtestError
from airtest.core.settings import Settings as ST
from airtest.report.report import LogToHtml
import subprocess
import time
import os
import shutil
import stat

# ---------- 全局参数 ----------
ST.THRESHOLD        = 0.8
ST.FIND_TIMEOUT     = 10
ST.FIND_TIMEOUT_TMP = 3


# ===================================================================
#  房间管理自动化 —— 风格完全对齐格式.ini
# ===================================================================
class RoomAutomation:
    def __init__(self):
        self.setup_device()

    # ----------------------------------------------------------
    #  设备连接
    # ----------------------------------------------------------
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
                logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/Room_management/log",
                devices=[device_url],
                project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/Room_management"
            )

    # ----------------------------------------------------------
    #  安全函数 —— 与格式.ini 完全一致
    # ----------------------------------------------------------
    def safe_touch(self, template):
        try:
            touch(template)
            return True
        except (TargetNotFoundError, AirtestError) as e:
            print(f"[safe_touch] 点击失败：{e}")
            return False

    def safe_assert_exists(self, template, msg=None):
        try:
            assert_exists(template, msg)
            return True
        except AssertionError as e:
            print(f"[safe_assert_exists] 断言失败: {str(e)}")
            return False

    def safe_assert_not_exists(self, template, msg=None):
        try:
            assert_not_exists(template, msg)
            return True
        except AssertionError as e:
            print(f"[safe_assert_not_exists] 断言失败: {str(e)}")
            return False

    # ----------------------------------------------------------
    #  业务动作
    # ----------------------------------------------------------
    def _start_check(self):
        """回归首页并验证登录状态"""
        self.safe_touch(Template(r"tpl1754634667443.png", record_pos=(-0.287, -0.897), resolution=(1176, 2480)))
        if not self.safe_assert_exists(Template(r"tpl1760961005997.png", record_pos=(-0.31, -0.978), resolution=(1440, 3200)), "账号已登录"):
            print("未找到目标图像，重新执行safe_touch...")
            self.safe_touch(Template(r"tpl1754634667443.png", record_pos=(-0.287, -0.897), resolution=(1176, 2480)))
            if not self.safe_assert_exists(Template(r"tpl1760961005997.png", record_pos=(-0.31, -0.978), resolution=(1440, 3200)), "账号已登录"):
                print("重新执行后仍然失败，但继续执行后续代码...")
            else:
                print("重新执行后验证成功！")

    def _enter_room_management(self):
        self.safe_touch(Template(r"tpl1761893550996.png", record_pos=(0.378, 0.873), resolution=(1176, 2480)))
        time.sleep(1)
        self.safe_touch(Template(r"tpl1761893608016.png", record_pos=(-0.241, -0.284), resolution=(1176, 2480)))

    def _add_room(self):
        touch(Template(r"tpl1754378093737.png", record_pos=(-0.006, 0.832), resolution=(1440, 2560)))
        time.sleep(1)
        touch(Template(r"tpl1762236055876.png", threshold=0.8500000000000001, record_pos=(0.0, -0.27), resolution=(1176, 2480)))

        time.sleep(1)
        touch(Template(r"tpl1754378127011.png", record_pos=(-0.004, 0.835), resolution=(1440, 2560)))
        self.safe_assert_exists(Template(r"tpl1754631766713.png", record_pos=(0.007, -0.741), resolution=(1176, 2480)), "房间创建成功")

    def _edit_room(self):
        self.safe_touch(Template(r"tpl1754631857075.png", record_pos=(0.002, -0.625), resolution=(1176, 2480)))
        self.safe_touch(Template(r"tpl1754378287125.png", record_pos=(0.422, -0.751), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754378315005.png", record_pos=(-0.417, 0.741), resolution=(1440, 2560)))

        self.safe_touch(Template(r"tpl1754632343070.png", record_pos=(0.001, 0.86), resolution=(1176, 2480)))
        self.safe_touch(Template(r"tpl1754632471092.png", record_pos=(0.443, 0.117), resolution=(1176, 2480)))

        self.safe_touch(Template(r"tpl1761894000412.png", record_pos=(0.412, 0.699), resolution=(1176, 2480)))
        time.sleep(1)
        self.safe_touch(Template(r"tpl1761894039153.png", threshold=0.95, target_pos=6, record_pos=(0.338, 0.185), resolution=(1176, 2480)))
        time.sleep(2)
        self.safe_touch(Template(r"tpl1761894039153.png", threshold=0.95, target_pos=6, record_pos=(0.338, 0.185), resolution=(1176, 2480)))
        self.safe_touch(Template(r"tpl1761894056728.png", rgb=False, record_pos=(-0.005, 0.858), resolution=(1176, 2480)))

        self.safe_touch(Template(r"tpl1754632823173.png", record_pos=(-0.087, 0.698), resolution=(1176, 2480)))
        time.sleep(1)
        self.safe_touch(Template(r"tpl1761895088987.png", threshold=0.95, record_pos=(0.36, 0.056), resolution=(1176, 2480)))

        self.safe_touch(Template(r"tpl1754378491690.png", record_pos=(0.001, 0.838), resolution=(1440, 2560)))
        time.sleep(1)
        self.safe_touch(Template(r"tpl1761894585381.png", record_pos=(-0.247, -0.377), resolution=(1176, 2480)))
        swipe(Template(r"tpl1761894592304.png", record_pos=(-0.253, -0.379), resolution=(1176, 2480)), vector=[0.5606, 0.2771])

        self.safe_assert_exists(Template(r"tpl1761895254153.png", threshold=0.85, record_pos=(0.302, 0.21), resolution=(1176, 2480)), "元素添加成功")

        self.safe_touch(Template(r"tpl1754378573611.png", record_pos=(0.081, 0.742), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754378591875.png", record_pos=(-0.002, 0.835), resolution=(1440, 2560)))
        self.safe_assert_exists(Template(r"tpl1761895291252.png", record_pos=(-0.346, -0.593), resolution=(1176, 2480)), "文字添加成功")

        self.safe_touch(Template(r"tpl1754378380408.png", record_pos=(0.001, 0.838), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754378396119.png", record_pos=(-0.453, -0.819), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754378404796.png", record_pos=(0.424, -0.749), resolution=(1440, 2560)))
        time.sleep(2)

        self.safe_assert_exists(Template(r"tpl1761895291252.png", record_pos=(-0.346, -0.593), resolution=(1176, 2480)), "文字保存成功")
        self.safe_assert_exists(Template(r"tpl1761895254153.png", threshold=0.85, record_pos=(0.302, 0.21), resolution=(1176, 2480)), "元素保存成功")
        self.safe_touch(Template(r"tpl1754378777120.png", record_pos=(-0.453, -0.817), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754379016475.png", target_pos=6, record_pos=(0.451, -0.683), resolution=(1440, 2560)))

        text("9999999999")
        time.sleep(1)
        self.safe_touch(Template(r"tpl1754379539174.png", record_pos=(0.001, 0.756), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754378777120.png", record_pos=(-0.453, -0.817), resolution=(1440, 2560)))
        self.safe_assert_exists(Template(r"tpl1754633495510.png", record_pos=(0.246, -0.668), resolution=(1176, 2480)), "房间名称保存成功")

    def _delete_room(self):
        self.safe_touch(Template(r"tpl1754379559406.png", record_pos=(-0.408, -0.519), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754379137666.png", record_pos=(-0.002, 0.836), resolution=(1440, 2560)))
        self.safe_touch(Template(r"tpl1754633725159.png", record_pos=(0.185, 0.052), resolution=(1176, 2480)))
        self.safe_assert_exists(Template(r"tpl1754379151400.png", record_pos=(0.006, -0.336), resolution=(1440, 2560)), "房间删除提示出现")
        time.sleep(3)
        self.safe_assert_not_exists(Template(r"tpl1754379580647.png", record_pos=(-0.408, -0.52), resolution=(1440, 2560)), "删除房间成功")

    # ----------------------------------------------------------
    #  主入口
    # ----------------------------------------------------------
    def run_all_tests(self):
        try:
            print("开始执行回归首页...")
            self._start_check()
            print("开始执行进入房间管理...")
            self._enter_room_management()
            print("开始执行添加房间...")
            self._add_room()
            print("开始执行编辑房间...")
            self._edit_room()
            print("开始执行删除房间...")
            self._delete_room()
            print("所有房间管理用例执行完毕！")
        finally:
            self.generate_report()

    # ----------------------------------------------------------
    #  生成报告 —— 与格式.ini 完全一致
    # ----------------------------------------------------------
    def generate_report(self):
        old_report = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs\py_room.log'
        export_dir = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs'

        if os.path.exists(old_report):
            def readonly_handler(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(old_report, onerror=readonly_handler)

        os.makedirs(export_dir, exist_ok=True)

        h1 = LogToHtml(
            script_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\Room_management\py_room.py',
            log_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\Room_management\log',
            export_dir=export_dir,
            logfile=r'C:\Users\74515\Desktop\UI自动化测试_体验版\Room_management\log\log.txt',
            lang='zh',
            plugins=None
        )
        h1.report()


# ===================================================================
#  脚本入口
# ===================================================================
if __name__ == "__main__":
    automation = RoomAutomation()
    automation.run_all_tests()