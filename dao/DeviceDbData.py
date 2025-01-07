# -*- coding:UTF-8 -*-

import datetime
import hashlib
import logging
import re
import time
from sqlalchemy.orm import sessionmaker

from dao.Elements import Device_info, Device
from dao.base import engine

Session = sessionmaker(bind=engine)
session = Session()


def search_devices_info() -> list:
    """
    :rtype: object
    """
    # 165
    ele_list = session.query(Device_info).all()
    return ele_list


# 根据设备类型查询报警/故障/实时等数据
def search_tab_by_type_devices(deviceType: str) -> list:
    """
    :rtype: Elements
    """
    # session.commit()  # 提交一次，防止查询缓存
    logging.info("接受到查询请求,请求参数为: " + str(deviceType))
    # 返回列表，一个设备类型有多个报警/故障

    result = session.query(Device_info).filter_by(device_type=deviceType).all()
    return result


def insert_device(device: Device):
    addResult = session.add(device)
    session.commit()
    return addResult


# 根据设备id查询设备信息
def search_device_by_did(device_code1: str):
    result = session.query(Device).filter_by(device_code=device_code1).all()
    return result


# 查Device询整张表的数据
def search_device() -> list:
    # 返回列表，一个设备类型有多个报警/故障
    result = session.query(Device).all()
    return result
#
# def insert_device(device:Device):
#     session.add(device)
#     session.commit()

def search_device_all(deviceType: str):
    session.commit()  # 提交一次，防止查询缓存
    logging.info("接受到查询请求,请求参数为: " + str(deviceType))
    # 返回列表，一个设备类型有多个报警/故障
    result = session.query(Device_info, Device).join(Device, Device_info.device_type == Device.device_type).all()
    for device in result:
        print(device.id)

session.close()
if __name__ == '__main__':
    device_list = search_device()
    print(device_list[0])
        # devPre = ''.join(re.findall(r'[A-Za-z]', 'DJ20040088'))
        # devEndP = 'DJ20040088'.split(devPre)  # 英文部分
        # devEnd = devEndP[1]  # 数字部分
        # for i in range(1,201):
        #     de = Device(device_type='SMR1210', device_code=str(devPre + str(int(devEnd) + int(i))), device_name='DJ20040088', device_contact='30',
        #                 host='192.168.0.188', port='7893',alarm_rate=0.01,fault_rate=1,device_c16_type='0030')
        #     t = insert_device(de)
        # search_tab_by_type_devices("EMR1002")
        # result = search_device()
        # for t in result:
        #     print(t.id)
