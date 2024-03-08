# -*- coding:UTF-8 -*-
import asyncio
import logging
import random
import re
import socket
import threading
import time
from socket import *
import sys

from bean import LogPrint
from bean.DeviceConfig import DeviceConfig
from dao import DeviceDbData
from dao.Elements import Device
from deviceRuler import DeviceAgreement
from deviceRuler.DeviceLogic import DeviceLogic

log = LogPrint.log()


# https://blog.51cto.com/u_16213681/6976430   tcp编程基础
# 原始方法
def tcp_utils(host, port, msg):
    # host = "192.168.0.214"
    # port = 7895
    # 组装地址
    addr = (str(host), int(port))
    # 组装tcp链接
    tcpClient = socket(AF_INET, SOCK_STREAM)
    try:
        # 获取根据地址和名字布局的通讯链接
        remote_ip = gethostbyname(host)
    except gaierror:
        # could not resolve
        logging.info('Hostname could not be resolved. Exiting')
        # 发生异常则退出
        sys.exit()
    print('Ip address of ' + host + ' is ' + remote_ip)
    # 建立链接
    tcpClient.connect(addr)
    logging.info('connetion success...')
    logging.info(tcpClient.getpeername())
    info = msg
    tcpClient.send(bytes.fromhex(info))
    # 关闭链接
    tcpClient.close()


def my_callback(future):
    result = future.result()
    print('返回值: ', result)


class SocketClient():

    def __init__(self, host, port, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout

    def creat_connect(self):
        addr = (str(self.host), int(self.port))
        # 组装tcp链接
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, True)
        # self.socket.ioctl(SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        try:
            # 获取根据地址和名字布局的通讯链接
            remote_ip = gethostbyname(self.host)
            # 建立链接
            self.socket.connect(addr)
            log.info('connetion success...')
            log.info(self.socket.getpeername())
        except OSError as e:
            log.info('Tcp服务连接异常，尝试重新连接(10s),%s', e)
            self.socket.close()
            time.sleep(5)
            self.creat_connect()

    def send_msg(self, msg):
        """
        客户端向服务器发送消息
        增加重连机制
        :param msg:
        :return:
        """
        try:
            self.socket.send(bytes.fromhex(msg))
        except OSError as e:
            log.info('Tcp服务在发送消息时连接异常，尝试重新连接(10s),%s', e)
            self.creat_connect()


# 注意这个并没有采取协程的方式
def run_scheduleThread(job_func, *args):
    job_thread = threading.Thread(target=job_func, )
    job_thread.start()


def device_tcp_imitate(device: Device = None):
    pool = DeviceLogic().getPoolNum()
    # 数据库数据
    # deviceList = DeviceDbData.search_device()
    deviceList = regular_device('CS12345678', 500,'10.0.0.193','7893')
    for i in range(0, deviceList.__len__()):
        if deviceList[i].status != '1':
            device = deviceList[i]
            sockerClient = SocketClient(device.host, device.port)
            sockerClient.creat_connect()
            log.info("设备正在进入协程组：" + str(deviceList[i].device_code))
            # 心跳数据 单线程方式，如果需要多线程需要run_scheduleThread进行启动,使用这个启动的适合就需要将客户端链接和设备信息进行常量化
            # schedule.every(60).seconds.do(heartbeat, sockerClient, device)
            # schedule.every(5).seconds.do(run_scheduleThread,heartbeat)
            # 协程方式
            # pool.submit(heartbeat(sockerClient,device))
            pool.submit(handle_device_data(device, sockerClient), i, callback=my_callback)
            # schedule.every(int(device.device_contact)).seconds.do(handle_device_data, device, tcpClient)
    # # 心跳数据数据使用
    # while True:
    #     schedule.run_pending()


# 心跳函数
def heartbeat(sockerClient: SocketClient, device: Device):
    log.info('进入心跳函数')
    heart_data = DeviceAgreement.heart_data(device)
    sockerClient.send_msg(heart_data)


async def handle_device_data(device, sockerClient: SocketClient):
    log.info("执行模拟器数据发送")
    # 存储断链时的协议数据
    stopData = None
    # 获取指定类型设备下的协议类型
    deviceConList = DeviceDbData.search_tab_by_type_devices(device.device_type)
    while True:
        # 需要先发送一包实时数据(前提是有)之后才能判断是否需要发送报警/故障信息
        for deviceCon in deviceConList:
            if deviceCon.device_real_data is not None and deviceCon.device_real_data != '':
                deviceConfig = DeviceConfig(device.device_code, deviceCon.device_prefix,
                                            deviceCon.device_real_data,
                                            deviceCon.device_type)
                agreementRealData = DeviceAgreement.device_code_config(deviceConfig)
                if agreementRealData is not None:
                    stopData = agreementRealData
                    log.info("设备CODE: " + str(device.device_code) + " 可以发送实时数据：" + str(agreementRealData))
                    sockerClient.send_msg(agreementRealData)

        # 创造随机发送某条数据
        randomNum = random.randint(0, (deviceConList.__len__() - 1))
        # 创造发送报警/故障的概率
        y = round(random.uniform(0, 1), 2)
        log.info("报警触发随机数：" + str(y))
        # 如果随机数大于alarm_rate则发送报警
        if y > float(device.alarm_rate):
            # 拼接指定设备需要发送的报警协议信息，如果有报警协议
            if deviceConList[randomNum].device_alarm is not None and str(
                    deviceConList[randomNum].device_alarm) != '':
                deviceConfig = DeviceConfig(device.device_code, deviceConList[randomNum].device_prefix,
                                            deviceConList[randomNum].device_alarm,
                                            deviceConList[randomNum].device_type)
                agreementAlarm = DeviceAgreement.device_code_config(deviceConfig)
                if agreementAlarm is not None:
                    log.info("设备CODE: " + str(device.device_code) + "可以发送报警数据：" + str(agreementAlarm))
                    stopData = agreementAlarm
                    sockerClient.send_msg(agreementAlarm)

        y = round(random.uniform(0, 1), 2)
        # 如果随机数大于fault_rate则发送故障，如果有故障协议
        if y > float(device.fault_rate):
            if deviceConList[randomNum].device_fault is not None and str(
                    deviceConList[randomNum].device_fault) != '':
                deviceConfig = DeviceConfig(device.device_code, deviceConList[randomNum].device_prefix,
                                            deviceConList[randomNum].device_fault,
                                            deviceConList[randomNum].device_type)
                agreementFault = DeviceAgreement.device_code_config(deviceConfig)
                if agreementFault is not None:
                    logging.info("设备CODE: " + str(device.device_code) + "可以发送故障数据：" + str(agreementFault))
                    stopData = agreementFault
                    sockerClient.send_msg(stopData)
        await asyncio.sleep(int(device.device_contact))


def regular_device(initDeviceCode, deviceNum: int,host,port):
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
        device = Device()
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


if __name__ == '__main__':
    regular_device('CS12345678', 5,'10.0.0.193','17893')
    # device_tcp_imitate()
    y = round(random.uniform(0, 1), 2)
    print("随机小数 y:", y)
    # loop = asyncio.get_event_loop()
    # taskMap = [tcp_utils('47.110.73.94', '17893','4040040013494132313039303039370070ff0004000e010a3dc511b3000000aa641aa1b680102323')
    #     ,tcp_utils('47.110.73.94', '17893','4040020019444a32303034303038380030ff0003000a01000101000564e817e650092323')]
    # loop.run_until_complete(asyncio.gather(*taskMap))
    # loop.run_forever()
