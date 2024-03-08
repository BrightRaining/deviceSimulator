# def device_code_config(host, port, deviceId, code,deviceConfig:DeviceConfig): 4040 +流水号+id+xxxxxxxxx +校验码(4位) +2323
import random
import time

from bean import LogPrint
from bean.DeviceConfig import DeviceConfig
from dao.Elements import Device

log = LogPrint.log()

def calculate_crc16(data: bytes) -> int:
    # 初始化crc为0xFFFF
    crc = 0xFFFF
    # 循环处理每个数据字节
    for byte in data:
        # 将每个数据字节与crc进行异或操作
        crc ^= byte
        # 对crc的每一位进行处理
        for _ in range(8):
            # 如果最低位为1，则右移一位并执行异或0xA001操作(即0x8005按位颠倒后的结果)
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            # 如果最低位为0，则仅将crc右移一位
            else:
                crc = crc >> 1
    # 返回最终的crc值
    return crc


"""
最好的方式并不是像下面这样替换原本协议而是完整的生成一条，由于成本关系直接替换是快捷道路，也能达成效果
"""


def heart_data(device:Device):
    '4040 100a4757323530303033323305000003000fff000400000100 65b745d5 f838 2323'
    # 10 进制转16进制,设备编号
    devCode16 = device.device_code.encode('utf-8').hex().upper()
    # msgId = str(hex(random.randint(4000, 9999)))[2:]
    msgId = str(hex(random.randint(4000, 9999)))[2:]
    serNum = str(hex(random.randint(4111, 8888)))[2:]
    # log.info('准备的serNum：' + str(serNum))
    num = random.randint(4000, 9999)
    timestamp = int(time.time())
    timeReal = str(hex(timestamp).upper())
    tesc = '100a' + devCode16 + device.device_c16_type + '0001'  + serNum + 'ff' +'0004' + '00000100' + timeReal[2:]
    # log.info('准备的心跳协议：' + str(tesc))
    test_data = bytes.fromhex(tesc)
    # 计算CRC-16校验码
    crc16 = calculate_crc16(test_data)
    codeDid = '4040' + tesc + str(f'{crc16:04X}') + '2323'
    # time.sleep(1)  # 暂停2s
    log.info('发送的心跳协议：' + str(codeDid))
    return str(codeDid)





# 数据进行crc16加密
def device_code_config(deviceConfig: DeviceConfig):
    # 10 进制转16进制
    hex_str = deviceConfig.deviceId.encode('utf-8').hex().upper()
    devEndCode = str(deviceConfig.code)
    # 将截尾的时间戳剔除
    restCode = devEndCode[0: devEndCode.__len__() - 8]
    timestamp = int(time.time())
    rest = str(hex(timestamp).upper())
    # 换成当前时间，不包含设备ID前得数据
    result1 = str(restCode) + rest[2:]
    tesc = None
    # 替换流水号的方法 和3100类型流水号在 6位得可以直接在这里加上
    if deviceConfig.deviceType == 'MCB2000':
        print(str(str(deviceConfig.devicePrefix) + (hex_str) + result1))
        scpN = str(deviceConfig.devicePrefix) + (hex_str)
        tesc = replaceDeviceSerialNumberSimilarMCB2000(scpN.__len__(),
                                                       str(deviceConfig.devicePrefix) + (hex_str) + result1)
    # 替换流水号的方法 和3100类型流水号在前6位得可以直接在这里加上
    elif deviceConfig.deviceType == 'SMR3100' or deviceConfig.deviceType == 'EMR3002':
        tesc = replaceDeviceSerialNumberSimilarSMR3100(str(deviceConfig.devicePrefix) + (hex_str) + result1)
    # 替换流水号的方法 和1003类型相似得流水号在消息体中的设备类型直接在这里加上
    elif deviceConfig.deviceType == 'EMR1003' or deviceConfig.deviceType == 'RTU500' or deviceConfig.deviceType == 'EMR1002':
        result = replaceDeviceSerialNumberSimilarEMR1003(result1)
        tesc = str(deviceConfig.devicePrefix) + (hex_str) + result
    elif deviceConfig.deviceType == 'SMR1210':
        s = '02'
        num = random.randint(5000, 9999)
        cp = str(hex(num))
        tesc = s + cp[2:] + hex_str + result1
    else:
        tesc = str(deviceConfig.devicePrefix) + (hex_str) + result1
    # 测试数据 -crc校验 6BE1
    try:
        test_data = bytes.fromhex(tesc)
    except ValueError as e:
        return None
    # 计算CRC-16校验码
    crc16 = calculate_crc16(test_data)
    codeDid = '4040' + tesc + str(f'{crc16:04X}') + '2323'
    # time.sleep(1)  # 暂停2s
    log.info('准备发送的协议：' + str(codeDid))
    return str(codeDid)


# 替换流水号的方法 和1003类型相似得流水号在消息体中的设备类型直接引用
def replaceDeviceSerialNumberSimilarMCB2000(stNum, repCode):
    # 替换随机四位流水号准备
    num = random.randint(4000, 9999)
    cp = str(hex(num))
    # 取出前4位
    # 再取前4位，成功剥离流水号
    result = repCode[0:int(stNum + 10)] + cp[2:] + repCode[int(stNum + 14):repCode.__len__()]
    return result


# 替换流水号的方法 和1003类型相似得流水号在消息体中的设备类型直接引用
def replaceDeviceSerialNumberSimilarEMR1003(repCode):
    # 替换随机四位流水号准备
    num = random.randint(4000, 9999)
    cp = str(hex(num))
    # 取出前4位
    # 再取前4位，成功剥离流水号
    result = repCode[0:8] + cp[2:] + repCode[12:repCode.__len__()]
    return result


# 替换流水号的方法 和3100类型流水号在前6位得可以直接使用，流水号开头必须大于4
def replaceDeviceSerialNumberSimilarSMR3100(repCode):
    # 替换随机四位流水号准备
    num = random.randint(4000, 9999)
    cp = str(hex(num))
    # 取出前4位
    # 再取前4位，成功剥离流水号
    result = repCode[0:2] + cp[2:] + repCode[6:repCode.__len__()]
    return result

if __name__ == '__main__':
    deviceConfig = DeviceConfig('CC12345678', '100A',
                                '0100000117dfff002e1000243f4abf00415666664151999a000000004358c13940cd5abd3fb131913f7ec62b43d992d100020465e51cbb65e51cbb',
                                'EMR1002')
    device_code_config(deviceConfig)