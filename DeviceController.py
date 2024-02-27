import socket

from flask import request
from flask import Flask

from dao.Elements import Device
from deviceRuler.DeviceLogic import DeviceLogic

flask = Flask(__name__)
flask.config["JSON_AS_ASCII"] = False


@flask.route("/add_device", methods=['GET'])
def deviceTrgger():
    # 发送来的请求体
    device_type = request.args.get('device_type', default='1')  # 设备类型
    device_code = request.args.get('device_code', default='1')  # 设备编号
    device_name = request.args.get('device_name', default='1')  # 设备名称
    device_contact = request.args.get('device_contact', default='1')  # 通讯周期
    host = request.args.get('host', default='1')  # 目标IP
    port = request.args.get('port', default='1')  # 目标端口
    device = Device(device_type=device_type, device_code=device_code, device_name=device_name,
                    device_contact=device_contact, host=host, port=port)
    DeviceLogic().add_device(device)
    return {"msg": "添加成功"}


# 查询当前任务数量
@flask.route("/search/tasknum", methods=['GET'])
def deviceSearchTaskNum():
    pool = DeviceLogic().getPoolNum()
    taskNum = pool.get_task().__len__()
    return {"msg": "当前任务数量：" + str(taskNum)}


# 启动数据库中所有的设备模拟
@flask.route('/start/device/sim')
def startTaskDevice():
    DeviceLogic().device()


# 停止协程任务
@flask.route('/stop/device/sim')
def stopTaskDevice():
    pool = DeviceLogic().getPoolNum()
    pool.stop_loop()


# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)
# flask.run(host=ip,port=9090, threaded=True)
flask.run(host='192.168.0.251', threaded=True)
