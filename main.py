# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# async def device_tcp_imitate(device: Device):
#     addr = (str(device.host), int(device.port))
#     # 组装tcp链接
#     tcpClient = socket(AF_INET, SOCK_STREAM)
#     tcpClient.setsockopt(SOL_SOCKET, SO_KEEPALIVE, True)
#     tcpClient.ioctl(SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
#     try:
#         # 获取根据地址和名字布局的通讯链接
#         remote_ip = gethostbyname(device.host)
#         # 建立链接
#         tcpClient.connect(addr)
#         log.info('connetion success...')
#         log.info(tcpClient.getpeername())
#     except gaierror:
#         log.info('Hostname could not be resolved. Exiting')
#         # 发生异常则退出
#         sys.exit()
#
#     while True:
#         # 获取指定类型设备下的协议类型
#         deviceConList = DeviceDbData.search_tab_by_type_devices(device.device_type)
#         # 需要先发送一包实时数据(前提是有)之后才能判断是否需要发送报警/故障信息
#         for deviceCon in deviceConList:
#             if deviceCon.device_real_data is not None and deviceCon.device_real_data != '':
#                 deviceConfig = DeviceConfig(device.device_code, deviceCon.device_prefix,
#                                             deviceCon.device_real_data,
#                                             deviceCon.device_type)
#                 agreementRealData = DeviceAgreement.device_code_config(deviceConfig)
#                 try:
#                     tcpClient.send(bytes.fromhex(agreementRealData))
#                 except ConnectionError as e:
#                     log.info("发生断连，进行重试：" + str(e))
#                     tcpClient.close()
#                     # 获取根据地址和名字布局的通讯链接
#                     remote_ip = gethostbyname(device.host)
#                     # 建立链接
#                     tcpClient.connect(addr)
#                     tcpClient.send(bytes.fromhex(agreementRealData))
#
#         # 创造随机发送某条数据
#         randomNum = random.randint(0, (deviceConList.__len__() - 1))
#         # 创造发送报警/故障的概率
#         y = round(random.uniform(0, 1), 2)
#         print("报警触发随机数：" + str(y))
#         # 如果随机数大于alarm_rate则发送报警
#         if y > float(device.alarm_rate):
#             # 拼接指定设备需要发送的报警协议信息，如果有报警协议
#             if deviceConList[randomNum].device_alarm is not None and str(deviceConList[randomNum].device_alarm) != '':
#                 deviceConfig = DeviceConfig(device.device_code, deviceConList[randomNum].device_prefix,
#                                             deviceConList[randomNum].device_alarm,
#                                             deviceConList[randomNum].device_type)
#                 agreementAlarm = DeviceAgreement.device_code_config(deviceConfig)
#                 log.info("可以发送报警数据：" + str(agreementAlarm))
#                 try:
#                     tcpClient.send(bytes.fromhex(agreementAlarm))
#                 except ConnectionError as e:
#                     tcpClient.close()
#                     log.info("发生断连，进行重试：" + str(e))
#                     # 获取根据地址和名字布局的通讯链接
#                     remote_ip = gethostbyname(device.host)
#                     # 建立链接
#                     tcpClient.connect(addr)
#                     tcpClient.send(bytes.fromhex(agreementAlarm))
#         y = round(random.uniform(0, 1), 2)
#         # 如果随机数大于fault_rate则发送故障，如果有故障协议
#         if y > float(device.fault_rate):
#             if deviceConList[randomNum].device_fault is not None and str(deviceConList[randomNum].device_fault) != '':
#                 deviceConfig = DeviceConfig(device.device_code, deviceConList[randomNum].device_prefix,
#                                             deviceConList[randomNum].device_fault,
#                                             deviceConList[randomNum].device_type)
#                 agreementFault = DeviceAgreement.device_code_config(deviceConfig)
#                 logging.info("可以发送故障数据：" + str(agreementFault))
#                 tcpClient.send(bytes.fromhex(agreementFault))
#                 try:
#                     tcpClient.send(bytes.fromhex(agreementFault))
#                 except ConnectionError as e:
#                     tcpClient.close()
#                     log.info("发生断连，进行重试：" + str(e))
#                     # 获取根据地址和名字布局的通讯链接
#                     remote_ip = gethostbyname(device.host)
#                     # 建立链接
#                     tcpClient.connect(addr)
#                     tcpClient.send(bytes.fromhex(agreementFault))
#         # 取消判断服务器返回的字节码，有可能会出现实时数据空，报警和故障都未触发的情况
#         # tc = tcpClient.recv(1024)
#         # if str(tc) == '' or str(tc) is None:
#         #     break
#         # print("接收到服务数据："+format(tc))
#         # 根据配置阻塞当前协程，模仿通讯周期
#         await asyncio.sleep(int(device.device_contact))
#         # print("放弃阻塞当前线程")
