# -*- encoding=utf8 -*-
__author__ = "74515"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
# 初始化设备
if not cli_setup():
    auto_setup(__file__, logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/Device_Management/log", devices=["android://127.0.0.1:5037/192.168.5.73:5557?touch_method=MAXTOUCH&",], project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/Device_Management")

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
def Start_Check():

    safe_touch(Template(r"tpl1754634667443.png", record_pos=(-0.287, -0.897), resolution=(1176, 2480)))
    safe_touch(Template(r"tpl1754710693431.png", record_pos=(-0.378, 0.872), resolution=(1176, 2480)))
    
    # 验证登录状态
    assert_exists(Template(r"tpl1754643113734.png", record_pos=(-0.265, -0.901), resolution=(1176, 2480)), "账号已登录")
Start_Check()

# ====================添加设备=============================


# ====================查看设备=============================

touch(Template(r"tpl1754720475500.png", record_pos=(0.123, 0.876), resolution=(1176, 2480)))
touch(Template(r"tpl1754720493357.png", record_pos=(-0.111, -0.651), resolution=(1176, 2480)))
assert_exists(Template(r"tpl1754720657282.png", record_pos=(0.132, 0.191), resolution=(1176, 2480)), "雷达数据存在")
# ====================删除设备=============================

