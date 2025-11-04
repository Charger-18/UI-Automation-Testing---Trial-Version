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

class HealthRecordsAutomation:
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
                logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/Health_records/log",
                devices=[device_url],
                project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/Health_records"
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
    
    def safe_assert_not_exists(self, template, msg=None):
        """安全断言（仅执行一次，失败不影响测试报告）"""
        try:
            assert_not_exists(template, msg)
            return True
        except AssertionError as e:
            print(f"[safe_assert_not_exists] 断言失败: {str(e)}")
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
    
    # ----------- 进入我的页面 -------------
    def enter_health_record(self):
        self.safe_touch(Template(r"tpl1761641977886.png", record_pos=(0.374, 0.876), resolution=(1176, 2480)))
        touch(Template(r"tpl1754380649139.png", record_pos=(-0.356, -0.586), resolution=(1440, 2560)))
        self.safe_assert_exists(Template(r"tpl1761644104746.png", record_pos=(-0.157, -0.682), resolution=(1176, 2480)), "个人信息显示成功")
    
    # ----------- 基础信息 -------------
    def test_basic_info(self):
        """
        测试基础信息功能
        包含以下步骤：
        1. 进入基础信息页面
        2. 验证个人信息显示
        3. 编辑个人信息
        4. 验证编辑结果
        """
        # 编辑个人信息
        touch(Template(r"tpl1754380694020.png", record_pos=(-0.372, -0.508), resolution=(1440, 2560)))
        sleep(1.0)
        touch(Template(r"tpl1761644123303.png", target_pos=6, record_pos=(0.341, -0.638), resolution=(1176, 2480)))
        text("一二三四五")
        touch(Template(r"tpl1761632365212.png", target_pos=6, record_pos=(-0.009, -0.285), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761632376458.png", record_pos=(0.0, 0.75), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632380778.png", record_pos=(0.418, 0.311), resolution=(1176, 2480)))
        touch(Template(r"tpl1761631875041.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.044, -0.048), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632244953.png", target_pos=6, record_pos=(-0.05, 0.071), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632249258.png", target_pos=6, record_pos=(-0.049, 0.186), resolution=(1176, 2480)))
        touch(Template(r"tpl1761025763584.png", record_pos=(-0.401, 0.123), resolution=(1440, 3200)))
        sleep(1.0)
        touch(Template(r"tpl1760961356858.png", record_pos=(-0.005, 0.893), resolution=(1440, 3200)))
        touch(Template(r"tpl1754380761484.png", record_pos=(0.453, 0.517), resolution=(1440, 2560)))
        touch(Template(r"tpl1761632416982.png", target_pos=6, record_pos=(-0.008, 0.418), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761632449080.png", record_pos=(-0.003, 0.469), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632457481.png", record_pos=(0.416, 0.304), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632470919.png", target_pos=6, record_pos=(-0.007, 0.531), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761632481371.png", record_pos=(0.001, 0.751), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632485832.png", record_pos=(0.414, 0.308), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632514950.png", target_pos=6, record_pos=(-0.008, 0.649), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761632524959.png", record_pos=(0.001, 0.84), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632531197.png", record_pos=(0.406, 0.308), resolution=(1176, 2480)))
        swipe(Template(r"tpl1761632568798.png", record_pos=(-0.391, 0.651), resolution=(1176, 2480)), vector=[-0.0233, -0.2191])
        touch(Template(r"tpl1761632770380.png", target_pos=6, record_pos=(0.0, 0.378), resolution=(1176, 2480)))
        sleep(1.0)
        text("一二三四五")
        sleep(1.0)
        touch(Template(r"tpl1761632830626.png", record_pos=(-0.005, 0.594), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761632851432.png", threshold=0.99, target_pos=5, record_pos=(-0.384, 0.611), resolution=(1176, 2480)))
        touch(Template(r"tpl1761632934465.png", target_pos=6, record_pos=(-0.002, 0.684), resolution=(1176, 2480)))
        text("一二三四五")
        touch(Template(r"tpl1761633333513.png", record_pos=(-0.3, 0.736), resolution=(1176, 2480)))
        
        # 保存编辑结果
        touch(Template(r"tpl1754635735109.png", record_pos=(0.001, 0.857), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1754380803814.png", record_pos=(0.001, -0.34), resolution=(1440, 2560)), "基础信息更新弹窗")
        
        # 验证复位
        sleep(3.0)
        touch(Template(r"tpl1754380694020.png", record_pos=(-0.372, -0.508), resolution=(1440, 2560)))
        sleep(1.0)
        touch(Template(r"tpl1761634635585.png", target_pos=6, record_pos=(-0.012, -0.639), resolution=(1176, 2480)))
        for i in range(5):
            keyevent("KEYCODE_DEL")
        touch(Template(r"tpl1761633586410.png", target_pos=6, record_pos=(-0.013, -0.289), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761633600289.png", record_pos=(-0.003, 0.563), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633604172.png", record_pos=(0.42, 0.31), resolution=(1176, 2480)))
        touch(Template(r"tpl1761644356242.png", threshold=0.98, target_pos=4, record_pos=(0.226, -0.048), resolution=(1176, 2480)))
        touch(Template(r"tpl1761644387145.png", threshold=0.98, target_pos=4, record_pos=(0.22, 0.063), resolution=(1176, 2480)))
        touch(Template(r"tpl1761644392044.png", threshold=0.98, target_pos=4, record_pos=(0.223, 0.185), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633879867.png", target_pos=6, record_pos=(-0.01, 0.297), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761633891578.png", record_pos=(-0.001, 0.557), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633894427.png", record_pos=(0.413, 0.304), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633915946.png", target_pos=6, record_pos=(-0.008, 0.416), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761633924327.png", record_pos=(0.003, 0.845), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633933532.png", record_pos=(0.422, 0.31), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633952802.png", threshold=0.75, target_pos=6, record_pos=(-0.004, 0.534), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761633967586.png", record_pos=(-0.005, 0.561), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633970732.png", record_pos=(0.414, 0.309), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633986522.png", target_pos=6, record_pos=(-0.009, 0.645), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761633993071.png", record_pos=(-0.004, 0.466), resolution=(1176, 2480)))
        touch(Template(r"tpl1761633996089.png", record_pos=(0.42, 0.312), resolution=(1176, 2480)))
        swipe(Template(r"tpl1761634042057.png", record_pos=(-0.391, 0.651), resolution=(1176, 2480)), vector=[-0.0233, -0.2454])
        touch(Template(r"tpl1761898375920.png", threshold=0.8, target_pos=9, record_pos=(-0.005, 0.355), resolution=(1176, 2480)))
        for i in range(6):
            keyevent("KEYCODE_DEL")
        touch(Template(r"tpl1761634812173.png", record_pos=(-0.358, 0.068), resolution=(1176, 2480)))
        touch(Template(r"tpl1761634135366.png", record_pos=(-0.004, 0.467), resolution=(1176, 2480)))
        sleep(2.0)
        touch(Template(r"tpl1761634142383.png", threshold=0.9500000000000002, target_pos=5, record_pos=(-0.382, 0.719), resolution=(1176, 2480)))
        touch(Template(r"tpl1761898974791.png", threshold=0.8500000000000001, target_pos=9, record_pos=(-0.01, 0.64), resolution=(1176, 2480)))
        for i in range(6):
            keyevent("KEYCODE_DEL")
        touch(Template(r"tpl1761634233735.png", record_pos=(-0.303, 0.618), resolution=(1176, 2480)))
        touch(Template(r"tpl1761634224301.png", record_pos=(0.001, 0.86), resolution=(1176, 2480)))
    
    # ----------- 健康信息 -------------
    def test_health_info(self):
        """
        测试健康信息功能
        包含以下步骤：
        1. 进入健康信息页面
        2. 添加家族病史、药物过敏史和既往病史
        3. 验证添加结果
        4. 修改各项健康信息
        5. 验证修改结果
        6. 返回主页面
        """
        sleep(4.0)
        # 进入健康信息页面
        touch(Template(r"tpl1761636082320.png", record_pos=(-0.313, -0.014), resolution=(1176, 2480)))
        sleep(1.0)
        
        # 添加既往病史
        touch(Template(r"tpl1754711068270.png", target_pos=6, record_pos=(-0.008, -0.637), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761635722458.png", threshold=0.9000000000000001, record_pos=(-0.363, -0.185), resolution=(1176, 2480)))
        touch(Template(r"tpl1754646281398.png", record_pos=(-0.002, 0.815), resolution=(1176, 2480)))
        
        # 添加家族病史
        touch(Template(r"tpl1754646304927.png", record_pos=(-0.009, -0.52), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1754646318939.png", threshold=0.9000000000000001, target_pos=4, record_pos=(-0.364, -0.065), resolution=(1176, 2480)))
        touch(Template(r"tpl1754646341842.png", record_pos=(-0.002, 0.818), resolution=(1176, 2480)))
        
        # 添加药物过敏史
        touch(Template(r"tpl1754646365116.png", record_pos=(-0.009, -0.405), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1754646387695.png", target_pos=4, record_pos=(-0.306, 0.178), resolution=(1176, 2480)))
        touch(Template(r"tpl1754646397913.png", record_pos=(0.002, 0.821), resolution=(1176, 2480)))
        sleep(1.0)
        assert_exists(Template(r"tpl1761635272788.png", threshold=0.9000000000000001, record_pos=(0.28, -0.526), resolution=(1176, 2480)), "选择选项")
        
        # 保存健康信息
        touch(Template(r"tpl1760962122934.png", record_pos=(0.0, 0.992), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1754646471859.png", record_pos=(-0.34, -0.517), resolution=(1176, 2480)), "家族病史显示")
        
        # 验证添加结果
        touch(Template(r"tpl1754647150687.png", record_pos=(0.122, -0.316), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761635371629.png", threshold=0.9500000000000002, record_pos=(0.001, -0.64), resolution=(1176, 2480)), "既往病史保存成功")
        assert_exists(Template(r"tpl1761635381549.png", threshold=0.9500000000000001, record_pos=(0.002, -0.522), resolution=(1176, 2480)), "家族病史保存成功")
        assert_exists(Template(r"tpl1761635569499.png", threshold=0.9500000000000002, record_pos=(-0.009, -0.407), resolution=(1176, 2480)), "药物过敏史保存成功")
        
        # 修改家族病史
        touch(Template(r"tpl1754646761184.png", record_pos=(-0.003, -0.52), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1754646771365.png", target_pos=4, record_pos=(-0.363, -0.064), resolution=(1176, 2480)))
        touch(Template(r"tpl1754646783888.png", record_pos=(-0.001, 0.821), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761635818557.png", record_pos=(-0.005, -0.517), resolution=(1176, 2480)), "家族病史修改")
        
        # 修改既往病史
        touch(Template(r"tpl1754646828405.png", record_pos=(-0.35, -0.638), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1760962294736.png", record_pos=(-0.375, 0.034), resolution=(1440, 3200)))
        touch(Template(r"tpl1754646852227.png", record_pos=(-0.006, 0.821), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761026258279.png", record_pos=(-0.006, -0.733), resolution=(1440, 3200)), "既往病史修改")
        
        # 修改药物过敏史
        touch(Template(r"tpl1761027594433.png", record_pos=(-0.34, -0.519), resolution=(1440, 3200)))
        sleep(1.0)
        touch(Template(r"tpl1754646923732.png", target_pos=4, record_pos=(-0.3, 0.184), resolution=(1176, 2480)))
        touch(Template(r"tpl1754646935790.png", record_pos=(-0.002, 0.821), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761026285937.png", record_pos=(0.001, -0.521), resolution=(1440, 3200)), "药物过敏史修改")
        
        # 保存修改
        touch(Template(r"tpl1754646993569.png", record_pos=(0.002, 0.859), resolution=(1176, 2480)))
        sleep(3.0)
        
        # 返回并验证修改结果
        touch(Template(r"tpl1761026370348.png", record_pos=(-0.222, -0.108), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761026398483.png", record_pos=(0.347, -0.624), resolution=(1440, 3200)), "健康信息修改成功")
        touch(Template(r"tpl1754647402376.png", threshold=0.8500000000000001, record_pos=(-0.407, -0.897), resolution=(1176, 2480)))
    
    # ----------- 用药信息 -------------
    def test_medication_info(self):
        """
        测试用药信息功能
        包含以下步骤：
        1. 进入用药信息页面
        2. 添加新药品信息（名称、用量、时间、备注）
        3. 验证药品添加结果
        4. 修改药品信息
        5. 验证修改结果
        6. 删除药品
        7. 验证删除结果
        8. 返回主页面
        """
        # 进入用药信息页面
        touch(Template(r"tpl1754648734885.png", record_pos=(0.125, -0.129), resolution=(1176, 2480)))
        sleep(1.0)
        
        # 点击添加药品按钮
        touch(Template(r"tpl1754648742022.png", record_pos=(-0.001, 0.862), resolution=(1176, 2480)))
        sleep(1.0)
        
        # 输入药品名称
        touch(Template(r"tpl1761644961091.png", target_pos=6, record_pos=(-0.229, -0.786), resolution=(1176, 2480)))
        text("感冒药")
        
        # 输入用药时间
        touch(Template(r"tpl1754648804297.png", target_pos=6, record_pos=(-0.232, -0.669), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1754648824617.png", record_pos=(0.417, 0.306), resolution=(1176, 2480)))
        sleep(1.0)
        
        # 输入每日用量
        touch(Template(r"tpl1754648850946.png", target_pos=6, record_pos=(-0.234, -0.554), resolution=(1176, 2480)))
        sleep(1.0)
        text("一")
        sleep(1.0)
        
        # 输入备注信息
        touch(Template(r"tpl1754648875143.png", target_pos=6, record_pos=(-0.23, -0.433), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1754648902615.png", record_pos=(0.418, 0.307), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1754648916353.png", threshold=0.85, target_pos=6, record_pos=(-0.23, -0.324), resolution=(1176, 2480)))
        text("不好吃")
        
        # 保存药品信息
        touch(Template(r"tpl1754648965676.png", record_pos=(-0.419, 0.166), resolution=(1176, 2480)))
        touch(Template(r"tpl1754648974876.png", threshold=0.9500000000000002, record_pos=(0.003, 0.855), resolution=(1176, 2480)))
        sleep(1.0)
        
        # 验证药品添加结果
        assert_exists(Template(r"tpl1754649025431.png", record_pos=(-0.381, -0.741), resolution=(1176, 2480)), "药品名称添加成功")
        assert_exists(Template(r"tpl1754649086692.png", record_pos=(0.393, -0.547), resolution=(1176, 2480)), "每日用量添加成功")
        assert_exists(Template(r"tpl1754649110770.png", record_pos=(0.27, -0.618), resolution=(1176, 2480)), "用药时间添加成功")
        
        # 修改药品信息
        touch(Template(r"tpl1754649174041.png", record_pos=(-0.383, -0.741), resolution=(1176, 2480)))
        
        # 修改每日用量
        touch(Template(r"tpl1754649187526.png", threshold=0.85, target_pos=6, record_pos=(-0.27, -0.553), resolution=(1176, 2480)))
        text("七")
        
        # 修改药品名称
        touch(Template(r"tpl1754649262887.png", threshold=0.85, target_pos=6, record_pos=(-0.231, -0.783), resolution=(1176, 2480)))
        text("2")
        
        # 保存修改
        touch(Template(r"tpl1761645131017.png", record_pos=(-0.011, -0.899), resolution=(1176, 2480)))
        touch(Template(r"tpl1754649290242.png", record_pos=(0.002, 0.856), resolution=(1176, 2480)))
        
        # 验证修改结果
        assert_exists(Template(r"tpl1754649329199.png", record_pos=(0.376, -0.542), resolution=(1176, 2480)), "每日用量修改成功")
        assert_exists(Template(r"tpl1754649357351.png", threshold=0.95, record_pos=(-0.333, -0.747), resolution=(1176, 2480)), "药品名称修改成功")
        
        # 删除药品
        touch(Template(r"tpl1754649432996.png", threshold=0.95, target_pos=6, record_pos=(-0.008, -0.743), resolution=(1176, 2480)))
        touch(Template(r"tpl1754649446331.png", record_pos=(0.188, 0.053), resolution=(1176, 2480)))
        
        # 验证删除结果
        assert_not_exists(Template(r"tpl1754649401231.png", threshold=0.95, record_pos=(-0.003, -0.646), resolution=(1176, 2480)), "药品删除成功")
        touch(Template(r"tpl1754649478331.png", threshold=0.9, record_pos=(-0.415, -0.897), resolution=(1176, 2480)))
    
    # ----------- 健康数据 -------------
    def test_health_data_info(self):

        touch(Template(r"tpl1754724200064.png", threshold=0.9000000000000001, record_pos=(-0.313, 0.361), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761874953861.png", threshold=0.9000000000000001, record_pos=(-0.268, -0.685), resolution=(1176, 2480)), "个人信息显示")

        assert_exists(Template(r"tpl1754724301859.png", record_pos=(0.237, -0.472), resolution=(1176, 2480)), "性别显示")

        assert_exists(Template(r"tpl1761704903255.png", threshold=0.9, rgb=True, record_pos=(-0.237, -0.48), resolution=(1176, 2480)), "室内卡片")
        touch(Template(r"tpl1761705935857.png", threshold=0.9, rgb=True, record_pos=(-0.379, 0.22), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761710306900.png", record_pos=(-0.223, -0.074), resolution=(1176, 2480)), "卧室卡片跳转")

        touch(Template(r"tpl1761706025091.png", record_pos=(-0.411, -0.899), resolution=(1176, 2480)))
        touch(Template(r"tpl1761706035904.png", threshold=0.9, rgb=True, record_pos=(-0.241, 0.222), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761706054245.png", rgb=True, record_pos=(-0.009, -0.186), resolution=(1176, 2480)), "客厅卡片跳转")
        keyevent("BACK")
        touch(Template(r"tpl1761706090373.png", record_pos=(-0.103, 0.225), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761706100454.png", rgb=True, record_pos=(-0.068, -0.201), resolution=(1176, 2480)), "卫生间卡片跳转")
        touch(Template(r"tpl1761706120182.png", record_pos=(-0.211, 0.997), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761706166854.png", record_pos=(0.229, 0.167), resolution=(1176, 2480)), "活动卡片")


        #室内
        touch(Template(r"tpl1761710406551.png", record_pos=(0.142, 0.171), resolution=(1176, 2480)))
        templates = [
            (Template(r"tpl1761724006225.png", record_pos=(0.354, -0.179), resolution=(1176, 2480)), "热力图加载"),
            (Template(r"tpl1761706219292.png", record_pos=(-0.226, -0.142), resolution=(1176, 2480)), "室内活动"),
            (Template(r"tpl1761823994978.png", record_pos=(0.003, -0.185), resolution=(1176, 2480)), "室内活动"),
            (Template(r"tpl1761890493205.png", record_pos=(-0.077, -0.194), resolution=(1176, 2480)), "室内活动")
        ]
        for template, description in templates:
            if self.safe_assert_exists(template, description):
                print(f"{description}验证通过")
                break
        else:
            print("所有验证都失败")
        keyevent("back")

        #室外
        touch(Template(r"tpl1761723934115.png", record_pos=(0.333, 0.17), resolution=(1176, 2480)))
        templates = [
            (Template(r"tpl1761724006225.png", record_pos=(0.354, -0.179), resolution=(1176, 2480)), "热力图加载"),
            (Template(r"tpl1761706219292.png", record_pos=(-0.226, -0.142), resolution=(1176, 2480)), "室内活动"),
            (Template(r"tpl1761823994978.png", record_pos=(0.003, -0.185), resolution=(1176, 2480)), "室内活动"),
            (Template(r"tpl1761890493205.png", record_pos=(-0.077, -0.194), resolution=(1176, 2480)), "室内活动")
        ]
        for template, description in templates:
            if self.safe_assert_exists(template, description):
                print(f"{description}验证通过")
                break
        else:
            print("所有验证都失败")
        keyevent("back")
        
        #心率
        touch(Template(r"tpl1761708769980.png", record_pos=(-0.249, -0.283), resolution=(1176, 2480)))
        assert_not_exists(Template(r"tpl1761816853068.png", threshold=0.9000000000000001, rgb=True, record_pos=(0.039, -0.045), resolution=(1176, 2480)), "心率数据表")

        assert_exists(Template(r"tpl1761709000988.png", threshold=0.98, record_pos=(-0.312, 0.371), resolution=(1176, 2480)), "日心率范围")
        assert_not_exists(Template(r"tpl1761709338755.png", threshold=0.98, record_pos=(0.104, 0.422), resolution=(1176, 2480)), "日平均心率")
        self.safe_assert_not_exists(Template(r"tpl1761709493726.png", record_pos=(-0.312, 0.684), resolution=(1176, 2480)), "日高心率次数")
        self.safe_assert_not_exists(Template(r"tpl1761709500061.png", record_pos=(0.122, 0.689), resolution=(1176, 2480)), "日低心率次数")
        
        
        
        self.safe_assert_exists
        touch(Template(r"tpl1761709072711.png", record_pos=(0.001, -0.769), resolution=(1176, 2480)))

        assert_exists(Template(r"tpl1761724875867.png", threshold=0.9, rgb=True, record_pos=(-0.271, -0.219), resolution=(1176, 2480)), "心率数据周表")



        
        assert_exists(Template(r"tpl1761709000988.png", threshold=0.98, record_pos=(-0.312, 0.371), resolution=(1176, 2480)), "周心率范围")
        assert_not_exists(Template(r"tpl1761709338755.png", threshold=0.98, record_pos=(0.104, 0.422), resolution=(1176, 2480)), "周平均心率")
        self.safe_assert_not_exists(Template(r"tpl1761709493726.png", threshold=0.9, record_pos=(-0.312, 0.684), resolution=(1176, 2480)), "周高心率次数")
        self.safe_assert_not_exists(Template(r"tpl1761709500061.png", threshold=0.9, record_pos=(0.122, 0.689), resolution=(1176, 2480)), "周低心率次数")


        touch(Template(r"tpl1761709128193.png", record_pos=(0.288, -0.764), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761724875867.png", threshold=0.9, rgb=True, record_pos=(-0.271, -0.219), resolution=(1176, 2480)), "心率数据月表")
        assert_exists(Template(r"tpl1761709000988.png", threshold=0.98, record_pos=(-0.312, 0.371), resolution=(1176, 2480)), "月心率范围")
        assert_not_exists(Template(r"tpl1761709338755.png", threshold=0.98, record_pos=(0.104, 0.422), resolution=(1176, 2480)), "月平均心率")
        
        self.safe_assert_not_exists(Template(r"tpl1761709493726.png", threshold=0.9, record_pos=(-0.312, 0.684), resolution=(1176, 2480)), "月高心率次数")
        self.safe_assert_not_exists(Template(r"tpl1761709500061.png", threshold=0.9, record_pos=(0.122, 0.689), resolution=(1176, 2480)), "月低心率次数")

        keyevent("back")



        #呼吸
        assert_not_exists(Template(r"tpl1761816895002.png", record_pos=(0.216, 0.193), resolution=(1176, 2480)), "呼吸卡片")

        touch(Template(r"tpl1761816910097.png", record_pos=(0.139, 0.1), resolution=(1176, 2480)))

        assert_not_exists(Template(r"tpl1761817072759.png", threshold=0.9000000000000001, rgb=True, record_pos=(0.031, -0.046), resolution=(1176, 2480)), "呼吸日表")

        assert_exists(Template(r"tpl1761725183243.png", threshold=0.9500000000000002, record_pos=(-0.34, 0.365), resolution=(1176, 2480)), "呼吸范围")
        assert_not_exists(Template(r"tpl1761725236174.png", threshold=0.98, record_pos=(0.12, 0.431), resolution=(1176, 2480)), "平均呼吸率")
        assert_not_exists(Template(r"tpl1761725281683.png", threshold=0.98, target_pos=6, record_pos=(-0.298, 0.679), resolution=(1176, 2480)), "高呼吸次数")
        assert_not_exists(Template(r"tpl1761725287470.png", threshold=0.98, record_pos=(0.135, 0.69), resolution=(1176, 2480)), "低呼吸次数")


        touch(Template(r"tpl1761725406957.png", threshold=0.9, record_pos=(0.0, -0.769), resolution=(1176, 2480)))
        sleep(1.0)

        assert_not_exists(Template(r"tpl1762156776983.png", record_pos=(0.002, -0.186), resolution=(1176, 2480)), "呼吸周表")



        assert_exists(Template(r"tpl1761725183243.png", threshold=0.9500000000000002, record_pos=(-0.34, 0.365), resolution=(1176, 2480)), "呼吸范围")
        assert_not_exists(Template(r"tpl1761725236174.png", threshold=0.98, record_pos=(0.12, 0.431), resolution=(1176, 2480)), "平均呼吸率")
        assert_not_exists(Template(r"tpl1761725281683.png", threshold=0.98, target_pos=6, record_pos=(-0.298, 0.679), resolution=(1176, 2480)), "高呼吸次数")
        assert_not_exists(Template(r"tpl1761725287470.png", threshold=0.98, record_pos=(0.135, 0.69), resolution=(1176, 2480)), "低呼吸次数")
        
        touch(Template(r"tpl1761725467939.png", record_pos=(0.286, -0.766), resolution=(1176, 2480)))
        sleep(1.0)

        assert_not_exists(Template(r"tpl1762156809916.png", record_pos=(0.002, -0.209), resolution=(1176, 2480)), "呼吸月表")

        assert_exists(Template(r"tpl1761725183243.png", threshold=0.9500000000000002, record_pos=(-0.34, 0.365), resolution=(1176, 2480)), "呼吸范围")
        assert_not_exists(Template(r"tpl1761725236174.png", threshold=0.98, record_pos=(0.12, 0.431), resolution=(1176, 2480)), "平均呼吸率")
        assert_not_exists(Template(r"tpl1761725281683.png", threshold=0.98, target_pos=6, record_pos=(-0.298, 0.679), resolution=(1176, 2480)), "高呼吸次数")
        assert_not_exists(Template(r"tpl1761725287470.png", threshold=0.98, record_pos=(0.135, 0.69), resolution=(1176, 2480)), "低呼吸次数")
        keyevent("back")

        
        swipe(Template(r"tpl1761727121371.png", record_pos=(-0.307, 0.924), resolution=(1176, 2480)), vector=[-0.0077, -0.5788]) 
    #     assert_not_exists(Template(r"tpl1761727220857.png", record_pos=(-0.264, -0.618), resolution=(1176, 2480)), "睡眠卡片")
        touch(Template(r"tpl1761727241912.png", record_pos=(-0.337, -0.715), resolution=(1176, 2480)))
    #     assert_not_exists(Template(r"tpl1761727250104.png", record_pos=(0.0, -0.325), resolution=(1176, 2480)), "睡眠数据")
        sleep(1.0)

        touch(Template(r"tpl1761818314315.png", record_pos=(-0.205, 0.997), resolution=(1176, 2480)))
        sleep(1.0)


        
        touch(Template(r"tpl1761727282455.png", threshold=0.8, record_pos=(0.236, -0.599), resolution=(1176, 2480)))
        
        sleep(2.0)

        assert_not_exists(Template(r"tpl1761727339610.png", record_pos=(0.009, -0.221), resolution=(1176, 2480)), "卫生间数据")
        touch(Template(r"tpl1761727408896.png", record_pos=(0.001, -0.763), resolution=(1176, 2480)))

        sleep(1.0)

        assert_exists(Template(r"tpl1762158790853.png", rgb=True, record_pos=(-0.259, -0.122), resolution=(1176, 2480)), "卫生间周数据")

        touch(Template(r"tpl1761727460502.png", record_pos=(0.294, -0.772), resolution=(1176, 2480)))
        sleep(1.0)

        assert_exists(Template(r"tpl1761727488301.png", rgb=True, record_pos=(0.187, -0.09), resolution=(1176, 2480)), "卫生间月数据")
        keyevent("back")

        #血氧
        touch(Template(r"tpl1761727537057.png", record_pos=(-0.241, 0.081), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761803527937.png", record_pos=(0.026, -0.304), resolution=(1176, 2480)), "血氧日数据")


        assert_not_exists(Template(r"tpl1761731668251.png", threshold=0.9, record_pos=(0.193, 0.373), resolution=(1176, 2480)), "血氧健康指标")

        assert_not_exists(Template(r"tpl1761731614924.png", threshold=0.9, record_pos=(0.374, 0.679), resolution=(1176, 2480)), "健康指标")

        
        touch(Template(r"tpl1761731538593.png", record_pos=(0.007, -0.766), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761803527937.png", record_pos=(0.026, -0.304), resolution=(1176, 2480)), "血氧日数据")
        assert_not_exists(Template(r"tpl1761731668251.png", threshold=0.9, record_pos=(0.193, 0.373), resolution=(1176, 2480)), "血氧健康指标")
        assert_not_exists(Template(r"tpl1761731614924.png", record_pos=(0.374, 0.679), resolution=(1176, 2480)), "健康指标")
        touch(Template(r"tpl1761731562823.png", record_pos=(0.292, -0.765), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761803527937.png", record_pos=(0.026, -0.304), resolution=(1176, 2480)), "血氧日数据")
        assert_not_exists(Template(r"tpl1761731668251.png", threshold=0.9, record_pos=(0.193, 0.373), resolution=(1176, 2480)), "血氧健康指标")
        assert_not_exists(Template(r"tpl1761731614924.png", record_pos=(0.374, 0.679), resolution=(1176, 2480)), "健康指标")
        keyevent("back")
        
        
        #运动步数
        touch(Template(r"tpl1761803631501.png", record_pos=(0.243, 0.105), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761803665679.png", record_pos=(-0.219, -0.267), resolution=(1176, 2480)), "运动日数据")
        touch(Template(r"tpl1761803685389.png", record_pos=(0.001, -0.769), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761803665679.png", record_pos=(-0.219, -0.267), resolution=(1176, 2480)), "运动周数据")
        touch(Template(r"tpl1761803689989.png", record_pos=(0.287, -0.774), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761803665679.png", record_pos=(-0.219, -0.267), resolution=(1176, 2480)), "运动月数据")
        keyevent("back")
        
        
        
        
        #血压
    #     assert_not_exists(Template(r"tpl1761803860816.png", record_pos=(0.238, -0.12), resolution=(1176, 2480)), "请填写测试点")

        touch(Template(r"tpl1761805367655.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.253, 0.035), resolution=(1176, 2480)))
        touch(Template(r"tpl1761805402709.png", record_pos=(-0.003, 0.227), resolution=(1176, 2480)))
        keyevent("back")
        sleep(3.0)
        assert_exists(Template(r"tpl1761805444272.png", record_pos=(-0.292, 0.144), resolution=(1176, 2480)), "新增血压功能")
        
        touch(Template(r"tpl1761803905219.png", record_pos=(-0.241, 0.153), resolution=(1176, 2480)))

        assert_not_exists(Template(r"tpl1761804022293.png", threshold=0.98, rgb=True, record_pos=(0.004, 0.379), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761804632680.png", threshold=0.9500000000000002, rgb=True, record_pos=(-0.247, 0.28), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761804648777.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.243, 0.275), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761805264365.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.179, 0.275), resolution=(1176, 2480)), "请填写测试点")

        touch(Template(r"tpl1761804697084.png", record_pos=(0.382, -0.571), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761804714872.png", record_pos=(-0.003, -0.898), resolution=(1176, 2480)), "新增血压")
        assert_exists(Template(r"tpl1761804748127.png", record_pos=(-0.004, -0.207), resolution=(1176, 2480)), "新增血压")
        keyevent("back")
        
        touch(Template(r"tpl1761804806363.png", record_pos=(0.001, -0.763), resolution=(1176, 2480)))

        assert_not_exists(Template(r"tpl1761804022293.png", threshold=0.98, rgb=True, record_pos=(0.004, 0.379), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761804632680.png", threshold=0.9500000000000002, rgb=True, record_pos=(-0.247, 0.28), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761804648777.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.243, 0.275), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761805264365.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.179, 0.275), resolution=(1176, 2480)), "请填写测试点")

        touch(Template(r"tpl1761804697084.png", record_pos=(0.382, -0.571), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761804714872.png", record_pos=(-0.003, -0.898), resolution=(1176, 2480)), "新增血压")
        assert_exists(Template(r"tpl1761804748127.png", record_pos=(-0.004, -0.207), resolution=(1176, 2480)), "新增血压")
        keyevent("back")

        touch(Template(r"tpl1761804809584.png", record_pos=(0.287, -0.769), resolution=(1176, 2480)))
    #     assert_exists(Template(r"tpl1761804514836.png", record_pos=(-0.029, -0.26), resolution=(1176, 2480)), "血压数据表")
        assert_not_exists(Template(r"tpl1761804022293.png", threshold=0.98, rgb=True, record_pos=(0.004, 0.379), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761804632680.png", threshold=0.9500000000000002, rgb=True, record_pos=(-0.247, 0.28), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761804648777.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.243, 0.275), resolution=(1176, 2480)), "血压指标")
        self.safe_assert_exists(Template(r"tpl1761805264365.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.179, 0.275), resolution=(1176, 2480)), "请填写测试点")

        touch(Template(r"tpl1761804697084.png", record_pos=(0.382, -0.571), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761804714872.png", record_pos=(-0.003, -0.898), resolution=(1176, 2480)), "新增血压")
        assert_exists(Template(r"tpl1761804748127.png", record_pos=(-0.004, -0.207), resolution=(1176, 2480)), "新增血压")
        keyevent("back")
        sleep(1.0)

        keyevent("back")

        
        #血糖
        touch(Template(r"tpl1761809049925.png", threshold=0.8500000000000001, target_pos=6, record_pos=(0.241, 0.457), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761808916201.png", record_pos=(0.0, -0.395), resolution=(1176, 2480)), "新增血糖页面")
        touch(Template(r"tpl1761808923455.png", record_pos=(-0.002, -0.032), resolution=(1176, 2480)))
        keyevent("back")
        assert_exists(Template(r"tpl1761808960994.png", record_pos=(0.078, 0.56), resolution=(1176, 2480)), "新增血糖功能")
        touch(Template(r"tpl1761807765142.png", record_pos=(0.24, 0.15), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761808842461.png", record_pos=(0.116, -0.222), resolution=(1176, 2480)), "血糖数据表")

        assert_not_exists(Template(r"tpl1761807939966.png", threshold=0.98, record_pos=(-0.006, 0.382), resolution=(1176, 2480)), "血糖数据")
        self.safe_assert_exists(Template(r"tpl1761807965376.png", threshold=0.8500000000000001, rgb=True, record_pos=(-0.071, 0.265), resolution=(1176, 2480)), "血糖指标")
        self.safe_assert_exists(Template(r"tpl1761807968894.png", threshold=0.8500000000000001, rgb=True, record_pos=(-0.383, 0.266), resolution=(1176, 2480)), "血糖指标")
        self.safe_assert_exists(Template(r"tpl1761807972801.png", threshold=0.8500000000000001, rgb=True, record_pos=(0.193, 0.272), resolution=(1176, 2480)), "血糖指标")
        touch(Template(r"tpl1761808889717.png", record_pos=(0.386, -0.572), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761808916201.png", record_pos=(0.0, -0.395), resolution=(1176, 2480)), "新增血糖页面")

        keyevent("back")

        touch(Template(r"tpl1761808876810.png", record_pos=(0.004, -0.768), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761808842461.png", record_pos=(0.116, -0.222), resolution=(1176, 2480)), "血糖数据表")

        assert_not_exists(Template(r"tpl1761807939966.png", threshold=0.98, record_pos=(-0.006, 0.382), resolution=(1176, 2480)), "血糖数据")
        self.safe_assert_exists(Template(r"tpl1761807965376.png", threshold=0.8500000000000001, rgb=True, record_pos=(-0.071, 0.265), resolution=(1176, 2480)), "血糖指标")
        self.safe_assert_exists(Template(r"tpl1761807968894.png", threshold=0.8500000000000001, rgb=True, record_pos=(-0.383, 0.266), resolution=(1176, 2480)), "血糖指标")
        self.safe_assert_exists(Template(r"tpl1761807972801.png", threshold=0.8500000000000001, rgb=True, record_pos=(0.193, 0.272), resolution=(1176, 2480)), "血糖指标")
        touch(Template(r"tpl1761808889717.png", record_pos=(0.386, -0.572), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761808916201.png", record_pos=(0.0, -0.395), resolution=(1176, 2480)), "新增血糖页面")
        keyevent("back")

        touch(Template(r"tpl1761808879943.png", record_pos=(0.295, -0.764), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761808842461.png", record_pos=(0.116, -0.222), resolution=(1176, 2480)), "血糖数据表")

        assert_not_exists(Template(r"tpl1761807939966.png", threshold=0.98, record_pos=(-0.006, 0.382), resolution=(1176, 2480)), "血糖数据")
        self.safe_assert_exists(Template(r"tpl1761807965376.png", threshold=0.8500000000000001, rgb=True, record_pos=(-0.071, 0.265), resolution=(1176, 2480)), "血糖指标")
        self.safe_assert_exists(Template(r"tpl1761807968894.png", threshold=0.8500000000000001, rgb=True, record_pos=(-0.383, 0.266), resolution=(1176, 2480)), "血糖指标")
        self.safe_assert_exists(Template(r"tpl1761807972801.png", threshold=0.8500000000000001, rgb=True, record_pos=(0.193, 0.272), resolution=(1176, 2480)), "血糖指标")
        touch(Template(r"tpl1761808889717.png", record_pos=(0.386, -0.572), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761808916201.png", record_pos=(0.0, -0.395), resolution=(1176, 2480)), "新增血糖页面")
        keyevent("back")
        sleep(2.0)
        keyevent("back")
        
        swipe(Template(r"tpl1761879916842.png", record_pos=(-0.302, 0.556), resolution=(1176, 2480)), vector=[0.0062, -0.3524])
        

        # 体温测试
        touch(Template(r"tpl1761812717900.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.245, 0.455), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761812740910.png", record_pos=(-0.003, -0.897), resolution=(1176, 2480)), "新增体温")
        assert_exists(Template(r"tpl1761812749495.png", record_pos=(-0.004, -0.457), resolution=(1176, 2480)), "体温添加页面")
        touch(Template(r"tpl1761812758431.png", record_pos=(-0.004, -0.147), resolution=(1176, 2480)))
        keyevent("back")
        assert_exists(Template(r"tpl1761812772400.png", threshold=0.9500000000000002, record_pos=(-0.364, 0.557), resolution=(1176, 2480)), "体温添加成功")
        touch(Template(r"tpl1761812784826.png", record_pos=(-0.23, 0.574), resolution=(1176, 2480)))
        self.safe_assert_exists(Template(r"tpl1761890898046.png", threshold=0.7, rgb=True, record_pos=(-0.059, -0.303), resolution=(1176, 2480)), "体温数据表")
        assert_not_exists(Template(r"tpl1762171404210.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.001, -0.188), resolution=(1176, 2480)), "体温数据表")
        assert_not_exists(Template(r"tpl1761812860352.png", threshold=0.8500000000000001, record_pos=(-0.007, 0.505), resolution=(1176, 2480)), "请填写测试点")
        touch(Template(r"tpl1761812952710.png", record_pos=(0.381, -0.571), resolution=(1176, 2480)))
        touch(Template(r"tpl1761812968207.png", record_pos=(-0.004, -0.147), resolution=(1176, 2480)))
        keyevent("BACK")
        sleep(2.0)
        keyevent("BACK")
        touch(Template(r"tpl1761813019047.png", threshold=0.9000000000000001, record_pos=(0.114, -0.324), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1761812878995.png", threshold=0.9000000000000001, record_pos=(0.001, -0.766), resolution=(1176, 2480)))
        self.safe_assert_exists(Template(r"tpl1761890898046.png", threshold=0.7, rgb=True, record_pos=(-0.059, -0.303), resolution=(1176, 2480)), "体温数据表")
        assert_not_exists(Template(r"tpl1762171404210.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.001, -0.188), resolution=(1176, 2480)), "体温数据表")
        touch(Template(r"tpl1761812883009.png", record_pos=(0.288, -0.763), resolution=(1176, 2480)))
        self.safe_assert_exists(Template(r"tpl1761890898046.png", threshold=0.7, rgb=True, record_pos=(-0.059, -0.303), resolution=(1176, 2480)), "体温数据表")
        assert_not_exists(Template(r"tpl1762171411182.png", threshold=0.95, rgb=True, record_pos=(0.004, -0.19), resolution=(1176, 2480)), "体温数据表")
        keyevent("BACK")
        
        # 体重测试
        
        touch(Template(r"tpl1754725031499.png", record_pos=(0.007, 0.86), resolution=(1176, 2480)))
        touch(Template(r"tpl1761813847926.png", threshold=0.9500000000000002, target_pos=3, record_pos=(0.226, 0.179), resolution=(1176, 2480)))
        touch(Template(r"tpl1761813882396.png", record_pos=(0.001, 0.861), resolution=(1176, 2480)))
        sleep(3.0)
        assert_not_exists(Template(r"tpl1762249610696.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.24, 0.591), resolution=(1176, 2480)), "删除卡片")

        touch(Template(r"tpl1754725031499.png", record_pos=(0.007, 0.86), resolution=(1176, 2480)))
        touch(Template(r"tpl1761813933472.png", threshold=0.9000000000000001, target_pos=3, record_pos=(-0.227, 0.519), resolution=(1176, 2480)))
        touch(Template(r"tpl1754725172516.png", record_pos=(0.001, 0.855), resolution=(1176, 2480)))

        assert_exists(Template(r"tpl1762253389656.png", threshold=0.9000000000000001, rgb=True, record_pos=(0.236, 0.59), resolution=(1176, 2480)), "添加卡片")


        
        
        
        touch(Template(r"tpl1761813146535.png", threshold=0.9500000000000002, target_pos=6, record_pos=(0.23, 0.455), resolution=(1176, 2480)))
        touch(Template(r"tpl1762168230428.png", record_pos=(-0.003, -0.526), resolution=(1176, 2480)))
        for i in range(2):
            keyevent("KEYCODE_DEL")
        text("70")
        touch(Template(r"tpl1762168315332.png", record_pos=(0.003, -0.139), resolution=(1176, 2480)))
        keyevent("back")
        sleep(1.0)
        touch(Template(r"tpl1762249587219.png", threshold=0.9500000000000002, record_pos=(0.1, 0.557), resolution=(1176, 2480)))

        assert_not_exists(Template(r"tpl1762239852895.png", threshold=0.9000000000000001, rgb=True, record_pos=(-0.008, -0.204), resolution=(1176, 2480)), "日体重数据表")        
        touch(Template(r"tpl1761813401060.png", record_pos=(0.004, -0.766), resolution=(1176, 2480)))
        assert_not_exists(Template(r"tpl1762239852895.png", threshold=0.9000000000000001, rgb=True, record_pos=(-0.008, -0.204), resolution=(1176, 2480)), "周体重数据表")

        touch(Template(r"tpl1761813404755.png", record_pos=(0.298, -0.765), resolution=(1176, 2480)))
        assert_not_exists(Template(r"tpl1762239862161.png", threshold=0.95, rgb=True, target_pos=5, record_pos=(-0.003, -0.201), resolution=(1176, 2480)), "月体重数据表")

        keyevent("back")
        
        swipe(Template(r"tpl1754725640899.png", record_pos=(0.132, -0.375), resolution=(1176, 2480)), vector=[0.017, 0.6154])
        touch(Template(r"tpl1754724347578.png", record_pos=(-0.227, -0.248), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1754724455516.png", record_pos=(-0.128, 0.873), resolution=(1176, 2480)), "跳转健康画像")
        assert_exists(Template(r"tpl1761814000532.png", record_pos=(-0.188, -0.712), resolution=(1176, 2480)), "个人信息显示")
        touch(Template(r"tpl1761028846992.png", record_pos=(0.371, 1.002), resolution=(1440, 3200)))
        touch(Template(r"tpl1761028852908.png", record_pos=(-0.329, -0.616), resolution=(1440, 3200)))
    
    # ----------- 体检报告 -------------
    def test_medical_examination_report_info(self):
        touch(Template(r"tpl1761891874040.png", record_pos=(0.112, 0.176), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1761012402650.png", record_pos=(-0.002, 0.001), resolution=(1440, 3200)), "体检报告页面")
        touch(Template(r"tpl1761012427303.png", record_pos=(-0.422, -0.973), resolution=(1440, 3200)))
    
    # ----------- 健康报告 -------------
    def test_health_report_info(self):
        touch(Template(r"tpl1761891949145.png", record_pos=(-0.313, 0.423), resolution=(1176, 2480)))
        touch(Template(r"tpl1761012742590.png", record_pos=(-0.301, -0.81), resolution=(1440, 3200)))
        self.safe_assert_exists(Template(r"tpl1761012759077.png", record_pos=(-0.006, 0.233), resolution=(1440, 3200)), "睡眠报告无数据")
#         self.safe_assert_exists(Template(r"tpl1761012881972.png", record_pos=(0.403, -0.851), resolution=(1440, 3200)), "请填写测试点")
#         self.safe_touch(Template(r"tpl1761012894493.png", record_pos=(-0.407, -0.85), resolution=(1440, 3200)))
#         self.safe_touch(Template(r"tpl1761012913023.png", record_pos=(0.399, -0.85), resolution=(1440, 3200)))
        
        touch(Template(r"tpl1761012918869.png", record_pos=(0.109, -0.853), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761012935267.png", record_pos=(-0.002, -0.121), resolution=(1440, 3200)), "请填写测试点")
        touch(Template(r"tpl1761012962861.png", record_pos=(0.0, 0.991), resolution=(1440, 3200)))
        keyevent("back")
        
        touch(Template(r"tpl1761012795776.png", record_pos=(-0.303, -0.618), resolution=(1440, 3200)))
        self.safe_assert_exists(Template(r"tpl1761012805606.png", record_pos=(-0.007, 0.226), resolution=(1440, 3200)), "睡眠报告无数据")
        assert_exists(Template(r"tpl1761012881972.png", record_pos=(0.403, -0.851), resolution=(1440, 3200)), "请填写测试点")
        self.safe_touch(Template(r"tpl1761012894493.png", record_pos=(-0.407, -0.85), resolution=(1440, 3200)))
        self.safe_touch(Template(r"tpl1761012913023.png", record_pos=(0.399, -0.85), resolution=(1440, 3200)))

        touch(Template(r"tpl1761012918869.png", record_pos=(0.109, -0.853), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761012935267.png", record_pos=(-0.002, -0.121), resolution=(1440, 3200)), "请填写测试点")
        touch(Template(r"tpl1761012962861.png", record_pos=(0.0, 0.991), resolution=(1440, 3200)))
        keyevent("back")
        
        touch(Template(r"tpl1761025085825.png", record_pos=(-0.303, -0.438), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761025098169.png", record_pos=(-0.008, 0.222), resolution=(1440, 3200)), "床位监测报告无数据")
        assert_exists(Template(r"tpl1761012881972.png", record_pos=(0.403, -0.851), resolution=(1440, 3200)), "请填写测试点")
        self.safe_touch(Template(r"tpl1761012894493.png", record_pos=(-0.407, -0.85), resolution=(1440, 3200)))
        self.safe_touch(Template(r"tpl1761012913023.png", record_pos=(0.399, -0.85), resolution=(1440, 3200)))

        touch(Template(r"tpl1761012918869.png", record_pos=(0.109, -0.853), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761012935267.png", record_pos=(-0.002, -0.121), resolution=(1440, 3200)), "请填写测试点")
        touch(Template(r"tpl1761012962861.png", record_pos=(0.0, 0.991), resolution=(1440, 3200)))
        keyevent("back")
        
        touch(Template(r"tpl1761025147593.png", record_pos=(-0.298, -0.237), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761025157386.png", record_pos=(-0.019, 0.235), resolution=(1440, 3200)), "跌倒报告无数据")
        assert_exists(Template(r"tpl1761012881972.png", record_pos=(0.403, -0.851), resolution=(1440, 3200)), "请填写测试点")
        self.safe_touch(Template(r"tpl1761012894493.png", record_pos=(-0.407, -0.85), resolution=(1440, 3200)))
        self.safe_touch(Template(r"tpl1761012913023.png", record_pos=(0.399, -0.85), resolution=(1440, 3200)))

        touch(Template(r"tpl1761012918869.png", record_pos=(0.109, -0.853), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761012935267.png", record_pos=(-0.002, -0.121), resolution=(1440, 3200)), "请填写测试点")
        touch(Template(r"tpl1761012962861.png", record_pos=(0.0, 0.991), resolution=(1440, 3200)))
        keyevent("back")
        sleep(1.0)
        keyevent("back")

    
    # ----------- 医护建议 -------------
    def test_medical_advice_info(self):
        touch(Template(r"tpl1761025383292.png", record_pos=(0.208, 0.6), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761025392210.png", record_pos=(0.003, -0.972), resolution=(1440, 3200)), "医护建议页面")
    
    
    #运行测试流程
    def run_all_tests(self):
        """运行所有测试流程"""
        try:
            print("开始执行回归首页测试...")
            self.start_check()
            print("开始执行进入我的页面测试...")
            self.enter_health_record()
            print("开始执行基础信息测试...")
            self.test_basic_info()
            print("开始执行健康信息测试...")
            self.test_health_info()
            print("开始执行用药信息测试...")
            self.test_medication_info()
            print("开始执行健康数据测试...")
            self.test_health_data_info()
            print("开始执行体检报告测试...")
            self.test_medical_examination_report_info()
            print("开始执行健康报告测试...")
            self.test_health_report_info()
            print("开始执行医护建议测试...")
            self.test_medical_advice_info()
            print("所有测试执行完成！")
        finally:
            # 生成报告
            self.generate_report()
    # 生成报告
    def generate_report(self):
        old_report = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs\Health_records.log'
        export_dir = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs'
        
        # ---- 1. 强制删除旧报告目录 ----
        if os.path.exists(old_report):
            # 先把只读属性去掉，再删
            def readonly_handler(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(old_report, onerror=readonly_handler)
        
        os.makedirs(export_dir, exist_ok=True)
        h1 = LogToHtml(script_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\Health_records\Health_records.py', log_root=r"C:\Users\74515\Desktop\UI自动化测试_体验版\Health_records\log", export_dir=r"C:\Users\74515\Desktop\UI自动化测试_体验版\docs", logfile=r'C:\Users\74515\Desktop\UI自动化测试_体验版\Health_records\log\log.txt', lang='zh', plugins=None)
        h1.report()

# 主程序入口
if __name__ == "__main__":
    automation = HealthRecordsAutomation()
    automation.run_all_tests()


