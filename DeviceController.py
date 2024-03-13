import socket
import sys

from flask import request
from flask import Flask

from asyncUtils import TcpUtils
from bean.Device_Sim_Config import Device_Sim_Config
from dao.Elements import Device

flask = Flask(__name__)
flask.config["JSON_AS_ASCII"] = False


# @flask.route("/add_device", methods=['GET'])
# def deviceTrgger():
#     # 发送来的请求体
#     device_type = request.args.get('device_type', default='1')  # 设备类型
#     device_code = request.args.get('device_code', default='1')  # 设备编号
#     device_name = request.args.get('device_name', default='1')  # 设备名称
#     device_contact = request.args.get('device_contact', default='1')  # 通讯周期
#     host = request.args.get('host', default='1')  # 目标IP
#     port = request.args.get('port', default='1')  # 目标端口
#     device = Device(device_type=device_type, device_code=device_code, device_name=device_name,
#                     device_contact=device_contact, host=host, port=port)
#     DeviceLogic().add_device(device)
#     return {"msg": "添加成功"}


# 查询当前任务数量
# @flask.route("/search/tasknum", methods=['GET'])
# def deviceSearchTaskNum():
#     pool = DeviceLogic().getPoolNum()
#     taskNum = pool.get_task().__len__()
#     return {"msg": "当前任务数量：" + str(taskNum)}


# 启动数据库中所有的设备模拟
@flask.route('/start')
def startTaskDevice():
    device_num = request.args.get('device_num', default='10')  # 设备数量
    host = request.args.get('host', default='10.0.0.193')  # 目标IP
    port = request.args.get('port', default='17893')  # 目标端口
    initDeviceCode = request.args.get('initDeviceCode', default='CS12345678')  # 目标端口
    device_config = Device_Sim_Config()
    device_config.device_num = device_num
    device_config.host = host
    device_config.port = port
    device_config.initDeviceCode = initDeviceCode
    TcpUtils.device_tcp_imitate(device_config)
    return {'msg': 'success'}


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
flask.run(host=ip, port=9090, threaded=True)
