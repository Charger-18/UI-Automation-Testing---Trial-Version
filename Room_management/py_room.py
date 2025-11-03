# -*- encoding=utf8 -*-
__author__ = "体验版"
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.error import TargetNotFoundError, AirtestError
from airtest.core.settings import Settings as ST
import subprocess
import time

def get_adb_device_url():
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
if not cli_setup():
    device_url = get_adb_device_url()
    auto_setup(
        __file__,
        logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/Room_management/log",
        devices=[device_url],
        project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/Room_management"
    )

    
#安全函数
def safe_touch(template):
    """安全点击：尝试点击一次，失败时打印日志并返回 False，不中断后续步骤"""
    try:
        touch(template)
        return True
    except (TargetNotFoundError, AirtestError) as e:
        print(f"[safe_touch] 点击失败：{e}")
        return False
def safe_assert_exists(template, msg=None):
    """安全断言（仅执行一次，失败不影响测试报告）"""
    try:
        assert_exists(template, msg)
        return True
    except AssertionError as e:
        print(f"[safe_assert_exists] 断言失败: {str(e)}")
        return False
def safe_assert_not_exists(template, msg=None):
    """安全断言（仅执行一次，失败不影响测试报告）"""
    try:
        assert_not_exists(template, msg)
        return True
    except AssertionError as e:
        print(f"[safe_assert_not_exists] 断言失败: {str(e)}")
        return False

    
# 回归首页
def Start_Check():
    safe_touch(Template(r"tpl1754634667443.png", record_pos=(-0.287, -0.897), resolution=(1176, 2480)))

    # 验证登录状态
    if not safe_assert_exists(Template(r"tpl1760961005997.png", record_pos=(-0.31, -0.978), resolution=(1440, 3200)), "账号已登录"):
        print("未找到目标图像，重新执行safe_touch...")
        safe_touch(Template(r"tpl1754634667443.png", record_pos=(-0.287, -0.897), resolution=(1176, 2480)))
        # 重新验证
        if not safe_assert_exists(Template(r"tpl1760961005997.png", record_pos=(-0.31, -0.978), resolution=(1440, 3200)), "账号已登录"):
            print("重新执行后仍然失败，但继续执行后续代码...")
        else:
            print("重新执行后验证成功！")
Start_Check()

#进入房间管理
def room_management():
    touch(Template(r"tpl1761893550996.png", record_pos=(0.378, 0.873), resolution=(1176, 2480)))
    sleep(1.0)

    touch(Template(r"tpl1761893608016.png", record_pos=(-0.241, -0.284), resolution=(1176, 2480)))
room_management()
# ===============添加房间=======================
touch(Template(r"tpl1754378093737.png", record_pos=(-0.006, 0.832), resolution=(1440, 2560)))
sleep(1.0)

touch(Template(r"tpl1754378113295.png", record_pos=(-0.001, -0.446), resolution=(1440, 2560)))
sleep(1.0)

touch(Template(r"tpl1754378127011.png", record_pos=(-0.004, 0.835), resolution=(1440, 2560)))

assert_exists(Template(r"tpl1754631766713.png", record_pos=(0.007, -0.741), resolution=(1176, 2480)), "房间创建成功")


# ==================编辑房间=========================

touch(Template(r"tpl1754631857075.png", record_pos=(0.002, -0.625), resolution=(1176, 2480)))

touch(Template(r"tpl1754378287125.png", record_pos=(0.422, -0.751), resolution=(1440, 2560)))

touch(Template(r"tpl1754378315005.png", record_pos=(-0.417, 0.741), resolution=(1440, 2560)))



safe_touch(Template(r"tpl1754632343070.png", record_pos=(0.001, 0.86), resolution=(1176, 2480)))
safe_touch(Template(r"tpl1754632471092.png", record_pos=(0.443, 0.117), resolution=(1176, 2480)))

touch(Template(r"tpl1761894000412.png", record_pos=(0.412, 0.699), resolution=(1176, 2480)))
sleep(1.0)

touch(Template(r"tpl1761894039153.png", threshold=0.9500000000000001, target_pos=6, record_pos=(0.338, 0.185), resolution=(1176, 2480)))
sleep(2.0)

touch(Template(r"tpl1761894039153.png", threshold=0.9500000000000001, target_pos=6, record_pos=(0.338, 0.185), resolution=(1176, 2480)))
touch(Template(r"tpl1761894056728.png", rgb=False, record_pos=(-0.005, 0.858), resolution=(1176, 2480)))






touch(Template(r"tpl1754632823173.png", record_pos=(-0.087, 0.698), resolution=(1176, 2480)))
sleep(1.0)

touch(Template(r"tpl1761895088987.png", threshold=0.9500000000000001, record_pos=(0.36, 0.056), resolution=(1176, 2480)))


touch(Template(r"tpl1754378491690.png", record_pos=(0.001, 0.838), resolution=(1440, 2560)))
sleep(1.0)
touch(Template(r"tpl1761894585381.png", record_pos=(-0.247, -0.377), resolution=(1176, 2480)))
swipe(Template(r"tpl1761894592304.png", record_pos=(-0.253, -0.379), resolution=(1176, 2480)), vector=[0.5606, 0.2771])

assert_exists(Template(r"tpl1761895254153.png", threshold=0.8500000000000001, record_pos=(0.302, 0.21), resolution=(1176, 2480)), "元素添加成功")


touch(Template(r"tpl1754378573611.png", record_pos=(0.081, 0.742), resolution=(1440, 2560)))
touch(Template(r"tpl1754378591875.png", record_pos=(-0.002, 0.835), resolution=(1440, 2560)))
assert_exists(Template(r"tpl1761895291252.png", record_pos=(-0.346, -0.593), resolution=(1176, 2480)), "文字添加成功")






touch(Template(r"tpl1754378380408.png", record_pos=(0.001, 0.838), resolution=(1440, 2560)))
touch(Template(r"tpl1754378396119.png", record_pos=(-0.453, -0.819), resolution=(1440, 2560)))
touch(Template(r"tpl1754378404796.png", record_pos=(0.424, -0.749), resolution=(1440, 2560)))
sleep(2.0)

# safe_assert_exists(Template(r"tpl1754378359191.png", record_pos=(-0.007, -0.054), resolution=(1440, 2560)), "房间模板保存成功")
assert_exists(Template(r"tpl1761895291252.png", record_pos=(-0.346, -0.593), resolution=(1176, 2480)), "文字保存成功")
assert_exists(Template(r"tpl1761895254153.png", threshold=0.8500000000000001, record_pos=(0.302, 0.21), resolution=(1176, 2480)), "元素保存成功")
touch(Template(r"tpl1754378777120.png", record_pos=(-0.453, -0.817), resolution=(1440, 2560)))
touch(Template(r"tpl1754379016475.png", target_pos=6, record_pos=(0.451, -0.683), resolution=(1440, 2560)))



text("9999999999")
sleep(1.0)
touch(Template(r"tpl1754379539174.png", record_pos=(0.001, 0.756), resolution=(1440, 2560)))


touch(Template(r"tpl1754378777120.png", record_pos=(-0.453, -0.817), resolution=(1440, 2560)))

assert_exists(Template(r"tpl1754633495510.png", record_pos=(0.246, -0.668), resolution=(1176, 2480)), "房间名称保存成功")


# ====================删除房间============================

touch(Template(r"tpl1754379559406.png", record_pos=(-0.408, -0.519), resolution=(1440, 2560)))

touch(Template(r"tpl1754379137666.png", record_pos=(-0.002, 0.836), resolution=(1440, 2560)))

touch(Template(r"tpl1754633725159.png", record_pos=(0.185, 0.052), resolution=(1176, 2480)))

assert_exists(Template(r"tpl1754379151400.png", record_pos=(0.006, -0.336), resolution=(1440, 2560)), "房间删除提示出现")
sleep(3.0)
assert_not_exists(Template(r"tpl1754379580647.png", record_pos=(-0.408, -0.52), resolution=(1440, 2560)), "删除房间成功")




