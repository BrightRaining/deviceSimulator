import queue
import re

from locust import TaskSet, HttpUser, task

from bean.DeviceConfig import DeviceConfig
from bean.Device_Loc_Config import Device_Loc_Config
from dao import DeviceDbData
from deviceRuler import DeviceAgreement
from locust_concurrency.Locust_Tcp import Locust_SocketClient
from bean import LogPrint

log = LogPrint.log()


def lo_handle_device_data(device):
    # 存储断链时的协议数据
    stopData = None
    # 获取指定类型设备下的协议类型
    deviceConList = DeviceDbData.search_tab_by_type_devices(device.device_type)
    for deviceCon in deviceConList:
        if deviceCon.device_real_data is not None and deviceCon.device_real_data != '':
            deviceConfig = DeviceConfig(device.device_code, deviceCon.device_prefix,
                                        deviceCon.device_real_data,
                                        deviceCon.device_type)
            agreementRealData = DeviceAgreement.device_code_config(deviceConfig)
            if agreementRealData is not None:
                device.device_real_data = agreementRealData
                # socke在初始化的时候就默认建立了连接
                sockerClient = Locust_SocketClient(device.host, device.port)
                device.sockerClient = sockerClient
    return device


def lo_regular_device(initDeviceCode, deviceNum: int, host, port):
    """
    压测时不使用数据库，直接按顺序生成
    :param initDeviceCode:
    :param deviceNum:
    :return:
    """
    device_list = []
    # 切割初始设备id进行自增长
    devPre = ''.join(re.findall(r'[A-Za-z]', initDeviceCode))
    devEndP = initDeviceCode.split(devPre)  # 英文部分
    devEnd = int(devEndP[1])  # 数字部分
    for i in range(0, deviceNum):
        device = Device_Loc_Config()
        device.device_code = str(devPre + str(int(devEnd) + int(i)))
        # device.device_code = 'CC12345678'
        device.device_type = 'EMR1002'
        device.device_contact = 1
        device.host = str(host)
        device.port = str(port)
        # 1：默认不报警
        device.alarm_rate = 1
        # 1：默认不触发故障
        device.fault_rate = 1
        # 1为使用中
        device.status = 1
        # 协议中规定的设备key
        device.device_c16_type = '0100'
        device_list.append(device)
    return device_list


class Locust_Run(TaskSet):

    @task(2)
    def im_socket(self):
        device = self.parent.queueData.get()  # 从queueData中取值（该队列循环-先进先出）
        log.info("设备CODE: " + str(device.device_code) + "  可以发送实时数据：" + str(device.device_real_data))
        flag = device.sockerClient.send_msg(device.device_real_data)
        self.parent.queueData.put_nowait(device)  # 将取到的数再丢回队列(后进后出)，即可循环使用


# 数据准备类
class Device_Data(HttpUser):
    # 定义用户行为的类
    tasks = [Locust_Run]
    queueData = queue.Queue()  # 初始化queue队列, 先进先出
    device_list = lo_regular_device('CS12346677', 500, '10.0.0.193', '17893')
    for device in device_list:
        dev = lo_handle_device_data(device)
        # 防止在生成流水号加密失败造成程序终止
        if dev.socketClient is not None:
            queueData.put_nowait(dev)

    min_wait = 500
    max_wait = 1000


if __name__ == "__main__":
    import os

    # os.system("locust -f Locust_Device.py --host=http://localhost:8089 --headless -u 5 -r 2 -t 30s --html HTML_FILE")  # 访问地址http://localhost:8089
    cmd = "locust -f Locust_Device.py --host=http://10.0.0.193 --web-host=127.0.0.1 "
    os.system(cmd)
    print('==================关闭连接，任务结束==================')
