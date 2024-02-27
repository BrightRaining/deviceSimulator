# crc16协议加密
from asyncUtils import TcpUtils
from asyncUtils.AsyncPool import AsyncPool
from bean import LogPrint
from dao import DeviceDbData
from dao.Elements import Device

log = LogPrint.log()


def my_callback(future):
    result = future.result()
    print('返回值: ', result)

# 设备侧，模拟数据逻辑处理
class DeviceLogic:

    # 初始化线程池
    def setPoolNum(self):
        global pool
        pool = AsyncPool(maxsize=1000, pool_maxsize=900)

    def getPoolNum(self):
        if globals() == None or globals().get('pool') == None:
            self.setPoolNum()
        return globals().get("pool")

    def device(self):
        TcpUtils.device_tcp_imitate()
        # pool = getPoolNum()
        # deviceList = DeviceDbData.search_device()
        # for i in range(0, deviceList.__len__()):
        #     if deviceList[i].status != '1':
        #         log.info("设备正在进入协程组：" + str(deviceList[i].device_code))
        #         pool.submit(TcpUtils.device_tcp_imitate(deviceList[i]), i, callback=my_callback)

    def add_device(self, device: Device):
        DeviceDbData.insert_device(device)
        result = DeviceDbData.search_device_by_did(device.device_code)
        pool = self.getPoolNum()
        if result is not None and result.__len__() > 0:
            log.info("设备添加成功，准备将设备加入协程池运行：" + str(device.device_code))
            log.info("当前线程池中的任务数量：" + str(pool.get_task().__len__()))
            pool.submit(TcpUtils.device_tcp_imitate(device), pool.get_task().__len__())


if __name__ == '__main__':
    deviceLogic = DeviceLogic()
    deviceLogic.device()

