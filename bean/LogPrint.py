import sys
import time
import logging
import os.path


class logger_handler(object):
    '''封装后的logging'''

    def __init__(self, logger=None):
        '''
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        '''

        # 第一步，创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)  # Log等级总开关

        # 第二步，创建一个handler，用于写入日志文件
        self.rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        if not os.path.exists(os.path.dirname(os.getcwd()) + '/log'):
            os.mkdir(os.path.dirname(os.getcwd()) + '/log')
        self.log_path = os.path.dirname(os.getcwd()) + '/log'
        # if not os.path.exists(self.log_path + 'xx_' + self.rq + '.log'):
        #     os.(self.log_path + 'xx_' + self.rq + '.log')
        self.log_name = self.log_path + '/log_' + self.rq + '.log'
        # self.log_name_detail = self.log_path + 'xx_detail_' + self.rq + '.log'
        self.logfile = self.log_name
        # self.logfile_detail = self.log_name_detail
        fh = logging.FileHandler(self.logfile, mode='w')
        # fh_detail = logging.FileHandler(self.logfile_detail, mode='w')
        fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
        # fh_detail.setLevel(logging.INFO)  # 输出到file的log等级的开关
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

        # 第三步，定义handler的输出格式
        formatter_file = logging.Formatter(
            "[%(asctime)s] %(filename)s->%(funcName)s [line:%(lineno)d] - %(levelname)s: %(message)s")

        formatter_detail = logging.Formatter(
            "[%(asctime)s] %(pathname)s->%(filename)s->%(funcName)s [line:%(lineno)d] - %(levelname)s: %(message)s")

        formatter_console = logging.Formatter(
            "[%(asctime)s] %(pathname)s->%(filename)s->%(funcName)s [line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter_file)
        # fh_detail.setFormatter(formatter_detail)
        ch.setFormatter(formatter_console)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)
        # self.logger.addHandler(fh_detail)
        self.logger.addHandler(ch)
        # 日志
        # self.logger.debug('this is a logger debug message')
        # self.logger.info('this is a logger info message')
        # self.logger.warning('this is a logger warning message')
        # self.logger.error('this is a logger error message')
        # self.logger.critical('this is a logger critical message')
        # # 2432jdsf
        # try:
        #     open("sklearn.txt", "rb")
        # except (SystemExit, KeyboardInterrupt):
        #     raise
        # except Exception:
        #     self.logger.error("Faild to open sklearn.txt from logger.error", exc_info=True)
        self.logger.propagate = True
        self.logger.info("Finish")

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        # fh.close()
        # ch.close()

    def getlog(self):
        return self.logger


def getlogs():
    """全局变量，不要调用"""
    try:
        if globals() == None or globals().get('loginfo') == None:
            logs = logger_handler().getlog()
            global loginfo
            loginfo = logs
    except:
        logs = logger_handler().getlog()
        global log
        log = logs
    return globals().get("loginfo")


def log():
    log = getlogs()
    return log


if __name__ == '__main__':
    logger_handler().getlog().info("hahha")
