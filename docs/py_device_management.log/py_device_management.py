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
# 设置全局的超时时长
ST.FIND_TIMEOUT = 10
ST.FIND_TIMEOUT_TMP = 3


class device_management:
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
                logdir="C:/Users/74515/Desktop/UI自动化测试_体验版/device_management/log",
                devices=[device_url],
                project_root="C:/Users/74515/Desktop/UI自动化测试_体验版/device_management"
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

    def safe_assert_not_exists(self,template, msg=None):
        """安全否定断言（仅执行一次，失败不影响测试报告）"""
        try:
            assert_not_exists(template, msg)
            return True
        except AssertionError as e:
            print(f"[safe_assert_not_exists] 断言失败: {str(e)}")
            return False

    # ====================回归首页=============================
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
    # ====================进入设备页面=========================
    def Device_Page(self):
        touch(Template(r"tpl1762484377943.png", record_pos=(0.123, 0.873), resolution=(1176, 2480)))
        sleep(1.0)
        self.safe_touch(Template(r"tpl1762484397554.png", threshold=0.8500000000000001, record_pos=(-0.012, 0.287), resolution=(1176, 2480)))
    def Device_details(self,type):
        #进入空间设备       
        if type == 1 :
            touch(Template(r"tpl1762496491158.png", threshold=0.9500000000000002, rgb=True, target_pos=4, record_pos=(-0.063, -0.541), resolution=(1176, 2480)))
        #进入跌倒设备 
        elif type == 2 :
            touch(Template(r"tpl1762860542526.png", target_pos=4, record_pos=(-0.068, -0.055), resolution=(1176, 2480)))

        #进入健康设备 
        elif type == 3 :
            touch(Template(r"tpl1762860634356.png", target_pos=4, record_pos=(-0.094, 0.713), resolution=(1176, 2480)))

    # ====================添加设备=============================
    # def Add_device():
    # ====================查看设备=============================
    #呼吸监控数据    
    def Breathe_Monitoring_Data(self):
        self.safe_touch(Template(r"tpl1761117722453.png",record_pos=(-0.385, -0.782), resolution=(1440, 3200)))
        if not self.safe_assert_not_exists(Template(r"tpl1761115543262.png", record_pos=(0.421, -0.651), resolution=(1440, 3200)), "设备数据看板"):
            assert_not_exists(Template(r"tpl1761115548435.png", record_pos=(0.41, -0.582), resolution=(1440, 3200)), "人体状态")
        self.safe_assert_not_exists(Template(r"tpl1761115577737.png", threshold=0.95, record_pos=(0.006, -0.225), resolution=(1440, 3200)), "心率数据列表")
        self.self.safe_assert_not_exists(Template(r"tpl1761115582460.png", threshold=0.99, record_pos=(0.006, 0.285), resolution=(1440, 3200)), "呼吸数据列表")
        swipe(Template(r"tpl1762828867654.png", record_pos=(-0.302, 0.427), resolution=(1176, 2480)), vector=[-0.027, -0.4522])

        self.safe_assert_not_exists(Template(r"tpl1761115587330.png", threshold=0.95, record_pos=(0.008, 0.795), resolution=(1440, 3200)), "体动数据列表")

    #空间监控数据    
    def Space_Monitoring_Data(self):
        self.safe_touch(Template(r"tpl1761117722453.png",record_pos=(-0.385, -0.782), resolution=(1440, 3200)))
        if not self.safe_assert_not_exists(Template(r"tpl1761115543262.png", record_pos=(0.421, -0.651), resolution=(1440, 3200)), "设备数据看板"):
            assert_not_exists(Template(r"tpl1761115548435.png", record_pos=(0.41, -0.582), resolution=(1440, 3200)), "人体状态")
        assert_not_exists(Template(r"tpl1762828775038.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.004, -0.179), resolution=(1176, 2480)), "目标距离数据列表")
        assert_not_exists(Template(r"tpl1762828781118.png", threshold=0.9500000000000002, rgb=True, target_pos=5, record_pos=(0.008, 0.063), resolution=(1176, 2480)), "目标距离数据列表")

    #跌倒监控数据
    def Fall_Monitoring_Data(self):
        self.safe_touch(Template(r"tpl1761117722453.png",record_pos=(-0.385, -0.782), resolution=(1440, 3200)))
        if not self.safe_assert_not_exists(Template(r"tpl1761115543262.png", record_pos=(0.421, -0.651), resolution=(1440, 3200)), "设备数据看板"):
            assert_not_exists(Template(r"tpl1761115548435.png", record_pos=(0.41, -0.582), resolution=(1440, 3200)), "人体状态")
        assert_not_exists(Template(r"tpl1762828105757.png", record_pos=(0.007, -0.19), resolution=(1176, 2480)), "目标数量数据列表")
        assert_not_exists(Template(r"tpl1762828112438.png", record_pos=(0.001, 0.053), resolution=(1176, 2480)), "目标数量数据列表")

    #生命监控数据
    def Life_Monitoring_Data(self,type):
        if type == 1 :
            # 处理床位监护模式
            if not self.safe_assert_not_exists(Template(r"tpl1762767466459.png", record_pos=(0.42, -0.354), resolution=(1176, 2480)), "床位监护卡片"):
                assert_not_exists(Template(r"tpl1762767455205.png", record_pos=(0.409, -0.346), resolution=(1176, 2480)), "床位监护卡片")
            assert_not_exists(Template(r"tpl1762767601592.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.002, 0.205), resolution=(1176, 2480)), "呼吸数据列表")
            swipe(Template(r"tpl1762767690028.png", record_pos=(-0.306, 0.011), resolution=(1176, 2480)), vector=[-0.018, -0.1582])
            assert_not_exists(Template(r"tpl1762767622153.png", threshold=0.9500000000000002, rgb=True, target_pos=5, record_pos=(0.004, 0.388), resolution=(1176, 2480)), "心率数据列表")
            swipe(Template(r"tpl1762767708892.png", record_pos=(-0.303, 0.202), resolution=(1176, 2480)), vector=[-0.0024, -0.3026])
            assert_not_exists(Template(r"tpl1762767634120.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.003, 0.661), resolution=(1176, 2480)), "目标数量列表")

        elif type == 2 :
            # 处理人员跟踪模式
            assert_not_exists(Template(r"tpl1761115543262.png", record_pos=(0.421, -0.651), resolution=(1440, 3200)), "设备数据看板")
            assert_not_exists(Template(r"tpl1762763738068.png", threshold=0.9500000000000002, record_pos=(0.01, -0.191), resolution=(1176, 2480)), "目标数量数据列表")
            
        elif type == 3 or type == "oxygen_saturation":
            # 处理跌倒监测模式
            assert_not_exists(Template(r"tpl1761115543262.png", record_pos=(0.421, -0.651), resolution=(1440, 3200)), "设备数据看板")
            assert_not_exists(Template(r"tpl1762763738068.png", threshold=0.9500000000000002, record_pos=(0.01, -0.191), resolution=(1176, 2480)), "目标数量数据列表")            
            
        elif type == 4 or type == "body_temperature":
            # 处理呼吸睡眠模式
            if not self.safe_assert_not_exists(Template(r"tpl1762767466459.png", record_pos=(0.42, -0.354), resolution=(1176, 2480)), "床位监护卡片"):
                assert_not_exists(Template(r"tpl1762767455205.png", record_pos=(0.409, -0.346), resolution=(1176, 2480)), "床位监护卡片")
            assert_not_exists(Template(r"tpl1762767601592.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.002, 0.205), resolution=(1176, 2480)), "呼吸数据列表")
            swipe(Template(r"tpl1762767690028.png", record_pos=(-0.306, 0.011), resolution=(1176, 2480)), vector=[-0.018, -0.1582])
            assert_not_exists(Template(r"tpl1762767622153.png", threshold=0.9500000000000002, rgb=True, target_pos=5, record_pos=(0.004, 0.388), resolution=(1176, 2480)), "心率数据列表")
            swipe(Template(r"tpl1762767708892.png", record_pos=(-0.303, 0.202), resolution=(1176, 2480)), vector=[-0.0024, -0.3026])
            assert_not_exists(Template(r"tpl1762767634120.png", threshold=0.9500000000000002, rgb=True, record_pos=(0.003, 0.661), resolution=(1176, 2480)), "目标数量列表")
            
        else:
            raise ValueError(f"不支持的数据类型: {type}，支持的类型有: 1/2/3/4 ")

    #基础配置
    def Basic_configuration(self,type):
        touch(Template(r"tpl1762855540830.png", record_pos=(-0.42, -0.584), resolution=(1176, 2480)))
        touch(Template(r"tpl1762839767822.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.009, -0.305), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762839783894.png", threshold=0.9500000000000002, record_pos=(-0.005, 0.747), resolution=(1176, 2480)))

        touch(Template(r"tpl1762839791836.png", record_pos=(0.411, 0.308), resolution=(1176, 2480)))

        touch(Template(r"tpl1762840018052.png", threshold=0.9500000000000002, target_pos=3, record_pos=(-0.043, -0.136), resolution=(1176, 2480)))

        touch(Template(r"tpl1762863426390.png", target_pos=6, record_pos=(-0.05, 0.032), resolution=(1176, 2480)))

        touch(Template(r"tpl1762850327346.png", threshold=0.8499999999999999, target_pos=6, record_pos=(-0.034, 0.173), resolution=(1176, 2480)))
        touch(Template(r"tpl1762850349780.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.001, 0.309), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762850366383.png", record_pos=(0.003, 0.754), resolution=(1176, 2480)))
        touch(Template(r"tpl1762850372211.png", record_pos=(0.414, 0.31), resolution=(1176, 2480)))

        touch(Template(r"tpl1762934756482.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.023, 0.443), resolution=(1176, 2480)))



        touch(Template(r"tpl1762935010495.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.116, 0.587), resolution=(1176, 2480)))



        touch(Template(r"tpl1762934794123.png", threshold=0.9000000000000001, target_pos=9, record_pos=(-0.024, 0.567), resolution=(1176, 2480)))

        swipe(Template(r"tpl1762850462483.png", record_pos=(-0.325, 0.723), resolution=(1176, 2480)), vector=[-0.0302, -0.4822])
        sleep(1.0)


        touch(Template(r"tpl1762935310652.png", threshold=0.8, target_pos=9, record_pos=(-0.118, -0.224), resolution=(1176, 2480)))

        touch(Template(r"tpl1762850588171.png", record_pos=(-0.005, -0.315), resolution=(1176, 2480)))
        sleep(3.0)

        touch(Template(r"tpl1762852743342.png", threshold=0.9500000000000002, target_pos=8, record_pos=(0.004, 0.429), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762850372211.png", record_pos=(0.414, 0.31), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762850619834.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.065, -0.109), resolution=(1176, 2480)))
        touch(Template(r"tpl1762850640270.png", threshold=0.95, target_pos=6, record_pos=(-0.014, 0.092), resolution=(1176, 2480)))
        touch(Template(r"tpl1762850659608.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.01, 0.293), resolution=(1176, 2480)))

        sleep(1.0)

        touch(Template(r"tpl1762850694290.png", threshold=0.9000000000000001, target_pos=8, record_pos=(0.0, 0.697), resolution=(1176, 2480)))
        touch(Template(r"tpl1762850682982.png", record_pos=(0.42, 0.311), resolution=(1176, 2480)))

        sleep(2.0)

        assert_not_exists(Template(r"tpl1762938109692.png", threshold=0.95, record_pos=(-0.005, 0.147), resolution=(1176, 2480)), "姿态检测联动")


        swipe(Template(r"tpl1762935578286.png", record_pos=(-0.324, 0.707), resolution=(1176, 2480)), vector=[-0.0263, -0.4625])




        touch(Template(r"tpl1762850796469.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.044, 0.288), resolution=(1176, 2480)))



        touch(Template(r"tpl1762850811821.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.037, 0.491), resolution=(1176, 2480)))
        touch(Template(r"tpl1762850824128.png", record_pos=(-0.012, 0.69), resolution=(1176, 2480)))
        touch(Template(r"tpl1762850838183.png", record_pos=(0.0, 0.855), resolution=(1176, 2480)))
        keyevent("back")
        touch(Template(r"tpl1762860866672.png", record_pos=(0.001, 0.86), resolution=(1176, 2480)))
        keyevent("back")
                
        #验证复位
        self.Device_details(type)
        touch(Template(r"tpl1761117771638.png",record_pos=(-0.153, -0.783), resolution=(1440, 3200)))
        
        
        touch(Template(r"tpl1762935755015.png", record_pos=(-0.026, -0.309), resolution=(1176, 2480)))
        sleep(1.0)
        touch(Template(r"tpl1762935764422.png", record_pos=(-0.007, 0.555), resolution=(1176, 2480)))
        touch(Template(r"tpl1762935768324.png", record_pos=(0.413, 0.302), resolution=(1176, 2480)))
        touch(Template(r"tpl1762935833902.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.134, -0.167), resolution=(1176, 2480)))
        touch(Template(r"tpl1762935854626.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.136, 0.032), resolution=(1176, 2480)))
        touch(Template(r"tpl1762935887244.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.134, 0.171), resolution=(1176, 2480)))
        touch(Template(r"tpl1762935903621.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.019, 0.315), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762935920924.png", record_pos=(-0.005, 0.555), resolution=(1176, 2480)))

        touch(Template(r"tpl1762935923490.png", record_pos=(0.419, 0.302), resolution=(1176, 2480)))

        touch(Template(r"tpl1762937540602.png", threshold=0.8500000000000001, target_pos=3, record_pos=(-0.095, 0.591), resolution=(1176, 2480)))




        touch(Template(r"tpl1762935964607.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.017, 0.589), resolution=(1176, 2480)))
        touch(Template(r"tpl1762935977574.png", threshold=0.9000000000000001, target_pos=9, record_pos=(-0.109, 0.573), resolution=(1176, 2480)))
        swipe(Template(r"tpl1762935992308.png", record_pos=(-0.326, 0.718), resolution=(1176, 2480)), vector=[-0.0389, -0.4576])
        sleep(2.0)

        touch(Template(r"tpl1762936044596.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.034, -0.359), resolution=(1176, 2480)))
        touch(Template(r"tpl1762936060202.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.014, -0.225), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762936076478.png", record_pos=(-0.009, 0.753), resolution=(1176, 2480)))

        touch(Template(r"tpl1762936079760.png", record_pos=(0.42, 0.307), resolution=(1176, 2480)))
        touch(Template(r"tpl1762940302593.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.16, -0.207), resolution=(1176, 2480)))
        touch(Template(r"tpl1762940372761.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.1, 0.315), resolution=(1176, 2480)))


        touch(Template(r"tpl1762936146986.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.026, 0.384), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762936162635.png", record_pos=(-0.008, 0.55), resolution=(1176, 2480)))

        touch(Template(r"tpl1762936165422.png", record_pos=(0.419, 0.304), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1762936191627.png", threshold=0.9500000000000002, record_pos=(-0.009, 0.528), resolution=(1176, 2480)), "姿态检测")
        touch(Template(r"tpl1762936208141.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.008, 0.523), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762936223641.png", record_pos=(-0.01, 0.555), resolution=(1176, 2480)))



        touch(Template(r"tpl1762936227094.png", record_pos=(0.422, 0.304), resolution=(1176, 2480)))
        swipe(Template(r"tpl1762936241820.png", record_pos=(-0.339, 0.652), resolution=(1176, 2480)), vector=[0.0033, -0.5816])
        touch(Template(r"tpl1762936307115.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.14, 0.283), resolution=(1176, 2480)))
        touch(Template(r"tpl1762936325971.png", threshold=0.8500000000000001, target_pos=6, record_pos=(-0.128, 0.491), resolution=(1176, 2480)))
        touch(Template(r"tpl1762936346331.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.012, 0.685), resolution=(1176, 2480)))
        touch(Template(r"tpl1762936365855.png", record_pos=(-0.009, -0.645), resolution=(1176, 2480)))
        touch(Template(r"tpl1762936396847.png", threshold=0.9500000000000002, target_pos=4, record_pos=(0.002, 0.749), resolution=(1176, 2480)))
        touch(Template(r"tpl1762936446662.png", record_pos=(0.242, 0.284), resolution=(1176, 2480)))


        touch(Template(r"tpl1762936457381.png", threshold=0.9000000000000001, target_pos=6, record_pos=(-0.016, 0.559), resolution=(1176, 2480)))
        touch(Template(r"tpl1762936483845.png", record_pos=(0.406, 0.124), resolution=(1176, 2480)))
        assert_exists(Template(r"tpl1762936503642.png", threshold=0.9500000000000002, record_pos=(-0.314, -0.645), resolution=(1176, 2480)), "鼾声检测时间段")
        touch(Template(r"tpl1762936511834.png", record_pos=(0.384, -0.733), resolution=(1176, 2480)))
        touch(Template(r"tpl1762940491953.png", record_pos=(0.189, 0.051), resolution=(1176, 2480)))

        keyevent("back")
        sleep(1.0)

        touch(Template(r"tpl1762936542012.png", record_pos=(-0.001, 0.861), resolution=(1176, 2480)))
        




























        





        
        
        


    #通话配置
    def Call_configuration(self):
        touch(Template(r"tpl1762855655217.png", threshold=0.9500000000000002, target_pos=4, record_pos=(-0.173, -0.58), resolution=(1176, 2480)))
        touch(Template(r"tpl1762855684732.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.013, -0.448), resolution=(1176, 2480)))
        for i in range(11):
            keyevent("KEYCODE_DEL")
        text("17622222222")
        touch(Template(r"tpl1762855772721.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.005, -0.311), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762855790667.png", threshold=0.8500000000000001, target_pos=2, record_pos=(0.004, 0.612), resolution=(1176, 2480)))
        touch(Template(r"tpl1762858282599.png", record_pos=(0.422, 0.31), resolution=(1176, 2480)))
        touch(Template(r"tpl1762858305005.png", threshold=0.95, target_pos=6, record_pos=(-0.014, -0.171), resolution=(1176, 2480)))
        text("17633333333")
        touch(Template(r"tpl1762858808436.png", record_pos=(0.003, 0.861), resolution=(1176, 2480)))
        self.safe_assert_exists(Template(r"tpl1762858868370.png", record_pos=(0.007, -0.438), resolution=(1176, 2480)), "保存成功弹窗")
        keyevent("back")

        


        



        





        


    #设备配置
    def Device_Configuration(self,type):
        sleep(1.0)

        self.safe_touch(Template(r"tpl1761117771638.png",record_pos=(-0.153, -0.783), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761117788161.png",record_pos=(-0.119, -0.681), resolution=(1440, 3200)), "设备配置选项卡")
        
        self.Basic_configuration(type)
        


        

        







        touch(Template(r"tpl1762850759164.png", threshold=0.9000000000000001, target_pos=8, record_pos=(-0.004, 0.427), resolution=(1176, 2480)))
        sleep(1.0)

        touch(Template(r"tpl1762850682982.png", record_pos=(0.42, 0.311), resolution=(1176, 2480)))        
        touch(Template(r"tpl1762850796469.png", threshold=0.9500000000000002, target_pos=6, record_pos=(-0.044, 0.288), resolution=(1176, 2480)))






        









        
        
        
        
        
        
        
        
        
        touch(Template(r"tpl1761117842247.png",record_pos=(-0.276, -0.675), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761117851971.png", record_pos=(0.002, -0.483), resolution=(1440, 3200)), "通话配置选项")
        touch(Template(r"tpl1761117895103.png",
              record_pos=(-0.131, -0.676), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761117910928.png", record_pos=(0.001, -0.08), resolution=(1440, 3200)), "音频配置选项")
        touch(Template(r"tpl1761117917946.png", record_pos=(0.026, -0.676), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761117931689.png",record_pos=(-0.001, -0.482), resolution=(1440, 3200)), "外设配置选项")

        touch(Template(r"tpl1761117921280.png", record_pos=(0.177, -0.681), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761117942915.png", record_pos=(0.001, -0.554), resolution=(1440, 3200)), "时段配置选项")
        assert_exists(Template(r"tpl1761117961408.png",record_pos=(-0.003, 0.981), resolution=(1440, 3200)), "保存设备配置按钮")

    #设备自动化
    def Equipment_Automation(self):
        self.safe_touch(Template(r"tpl1761118106593.png", record_pos=(0.097, -0.781), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761118152074.png",record_pos=(-0.008, 0.127), resolution=(1440, 3200)), "自动化空场景")
        assert_exists(Template(r"tpl1761118156414.png",record_pos=(-0.002, 0.99), resolution=(1440, 3200)), "新增自动化场景按钮")

    # ====================编辑设备=============================
    def Edit_respiratory_equipment(self):
        touch(Template(r"tpl1761115924466.png", threshold=0.9,record_pos=(-0.176, -0.397),resolution=(1440, 3200)))

    def Device_settings(self):
        touch(Template(r"tpl1761210346269.png", threshold=0.9,record_pos=(0.362, -0.88), resolution=(1440, 3200)))

        # 设备名称
        touch(Template(r"tpl1761210387033.png", record_pos=(0.001, -0.865), resolution=(1440, 3200)))
        touch(Template(r"tpl1761210609159.png", threshold=0.8, target_pos=6,record_pos=(-0.131, -0.865), resolution=(1440, 3200)))
        text("2222222222")
        touch(Template(r"tpl1761210660446.png",record_pos=(-0.005, 0.988), resolution=(1440, 3200)))
        touch(Template(r"tpl1761211281481.png",record_pos=(-0.42, -0.972), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761210734056.png", record_pos=(0.291, -0.87), resolution=(1440, 3200)), "修改设备名称")
        touch(Template(r"tpl1761211716097.png",record_pos=(-0.044, -0.866), resolution=(1440, 3200)))
        touch(Template(r"tpl1761211698030.png",record_pos=(-0.001, -0.863), resolution=(1440, 3200)))
        for i in range(10):
            keyevent("KEYCODE_DEL")
        touch(Template(r"tpl1761211758481.png",record_pos=(-0.395, -0.794), resolution=(1440, 3200)))
        touch(Template(r"tpl1761210660446.png",record_pos=(-0.005, 0.988), resolution=(1440, 3200)))
        touch(Template(r"tpl1761211809847.png",record_pos=(-0.417, -0.969), resolution=(1440, 3200)))

        assert_exists(Template(r"tpl1761210413658.png",record_pos=(-0.003, -0.767), resolution=(1440, 3200)), "设备编号")
        assert_exists(Template(r"tpl1761210420149.png", record_pos=(0.005, -0.661), resolution=(1440, 3200)), "设备版本")

        # 设备房间
        touch(Template(r"tpl1761273297212.png", target_pos=6,record_pos=(-0.006, -0.507), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761273332360.png", threshold=0.8500000000000001,record_pos=(0.0, -0.76), resolution=(1440, 3200)), "当前绑定房间")
        touch(Template(r"tpl1761273357632.png",record_pos=(-0.368, -0.866), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761273386236.png",record_pos=(-0.01, -0.427), resolution=(1440, 3200)), "更新绑定")
        assert_exists(Template(r"tpl1761273367876.png", threshold=0.9000000000000001,record_pos=(-0.002, -0.867), resolution=(1440, 3200)), "更新绑定")
        touch(Template(r"tpl1761273426924.png",record_pos=(-0.415, -0.97), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761273438493.png", threshold=0.9500000000000002,record_pos=(-0.005, -0.51), resolution=(1440, 3200)), "更新绑定")
        touch(Template(r"tpl1761273520966.png", threshold=0.8, target_pos=6,record_pos=(-0.008, -0.508), resolution=(1440, 3200)))
        touch(Template(r"tpl1761273539078.png",record_pos=(-0.419, -0.765), resolution=(1440, 3200)))
        keyevent("BACK")

        # 安装区域
        touch(Template(r"tpl1761273773317.png", threshold=0.8500000000000001,target_pos=6, record_pos=(-0.01, -0.408), resolution=(1440, 3200)))
        touch(Template(r"tpl1761273799831.png",record_pos=(-0.005, 0.722), resolution=(1440, 3200)))
        touch(Template(r"tpl1761273808705.png", record_pos=(0.42, 0.494), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761273834655.png", threshold=0.9500000000000002,target_pos=5, record_pos=(-0.008, -0.404), resolution=(1440, 3200)), "安装区域")
        touch(Template(r"tpl1761273834655.png", threshold=0.9500000000000002,target_pos=5, record_pos=(-0.008, -0.404), resolution=(1440, 3200)))
        touch(Template(r"tpl1761273874218.png",record_pos=(-0.002, 0.894), resolution=(1440, 3200)))

        touch(Template(r"tpl1761273808705.png", record_pos=(0.42, 0.494), resolution=(1440, 3200)))

        # 绑定亲友
        touch(Template(r"tpl1761274536953.png", threshold=0.8, target_pos=6,record_pos=(-0.014, -0.301), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761274574781.png", threshold=0.9000000000000001,target_pos=5, record_pos=(0.0, -0.841), resolution=(1440, 3200)), "绑定亲友")
        touch(Template(r"tpl1761274598212.png",record_pos=(-0.342, -0.669), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761274639735.png",record_pos=(-0.003, -0.44), resolution=(1440, 3200)), "更换绑定亲友")
        assert_exists(Template(r"tpl1761274663782.png", threshold=0.9500000000000002,record_pos=(-0.002, -0.672), resolution=(1440, 3200)), "更换绑定亲友")
        touch(Template(r"tpl1761275530134.png",record_pos=(-0.345, -0.841), resolution=(1440, 3200)))
        assert_exists(Template(r"tpl1761274574781.png", threshold=0.9000000000000001,target_pos=5, record_pos=(0.0, -0.841), resolution=(1440, 3200)), "绑定亲友")
        keyevent("BACK")

        # 网络信息
        assert_exists(Template(r"tpl1761210494090.png",record_pos=(-0.005, -0.153), resolution=(1440, 3200)), "网络信息")
        touch(Template(r"tpl1761275707693.png", threshold=0.8500000000000001,target_pos=6, record_pos=(-0.006, -0.151), resolution=(1440, 3200)))

    # ====================设备类型=============================
    # 空间设备
    def View_space_equipment(self):
        touch(Template(r"tpl1762496491158.png", threshold=0.9500000000000002, rgb=True, target_pos=4, record_pos=(-0.063, -0.541), resolution=(1176, 2480)))
        self.Space_Monitoring_Data()
        self.Device_Configuration()
        self.Equipment_Automation()
    # 跌倒设备
    def View_fall_equipment(self):
        touch(Template(r"tpl1762496491158.png", threshold=0.9500000000000002, rgb=True, target_pos=4, record_pos=(-0.063, -0.541), resolution=(1176, 2480)))
        self.Monitoring_Data()
        self.Device_Configuration()
        self.Equipment_Automation()
    # 健康设备
    def View_health_equipment(self,type):
        self.Device_details(type)
#         self.Life_Monitoring_Data(3)
        self.Device_Configuration(type)
#         self.Device_Configuration()
#         self.Equipment_Automation()

        
    # ====================测试入口=============================
    def run_all_tests(self):
        """运行所有测试流程"""
        try:
#             self.start_check()
#             self.Device_Page()
            self.View_health_equipment(3)
        finally:
        # 生成报告
             self.generate_report()

    def generate_report(self):

        old_report = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs\py_device_management.log'
        export_dir = r'C:\Users\74515\Desktop\UI自动化测试_体验版\docs'

        # ---- 1. 强制删除旧报告目录 ----
        if os.path.exists(old_report):
        # 先把只读属性去掉，再删
            def readonly_handler(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(old_report, onerror=readonly_handler)
        os.makedirs(export_dir, exist_ok=True)
        h1 = LogToHtml(script_root=r'C:\Users\74515\Desktop\UI自动化测试_体验版\device_management\py_device_management.py', log_root=r"C:\Users\74515\Desktop\UI自动化测试_体验版\device_management\log", export_dir=r"C:\Users\74515\Desktop\UI自动化测试_体验版\docs" ,logfile=r'C:\Users\74515\Desktop\UI自动化测试_体验版\device_management\log\log.txt', lang='zh', plugins=None)
        h1.report()

# 主程序入口
if __name__ == "__main__":
    automation = device_management()
    automation.run_all_tests()
    
    
    

    
    
    
# assert_not_exists(Template(r"tpl1761115543262.png", record_pos=(0.421, -0.651), resolution=(1440, 3200)), "设备数据看板")
# assert_not_exists(Template(r"tpl1761115548435.png", record_pos=(0.41, -0.582), resolution=(1440, 3200)), "人体状态")

# assert_not_exists(Template(r"tpl1761115577737.png", threshold=0.9, record_pos=(0.006, -0.225), resolution=(1440, 3200)), "心率数据列表")
# assert_not_exists(Template(r"tpl1761115582460.png", threshold=0.9, record_pos=(0.006, 0.285), resolution=(1440, 3200)), "呼吸数据列表")
# assert_not_exists(Template(r"tpl1761115587330.png", threshold=0.9, record_pos=(0.008, 0.795), resolution=(1440, 3200)), "体动数据列表")


