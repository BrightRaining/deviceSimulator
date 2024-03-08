import time
from socket import *

from bean import LogPrint

log = LogPrint.log()

class Locust_SocketClient():
    """
    单独组包，避免以后交叉修改
    """

    def __init__(self, host, port, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        # 默认直接建立连接
        self.creat_connect()

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
            resu = self.socket.recv(1024)
            if resu is None:
                return False
        except OSError as e:
            log.info('Tcp服务在发送消息时连接异常，尝试重新连接(10s),%s', e)
            self.creat_connect()
        return True