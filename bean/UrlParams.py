# 设置全局变量让域名使用更加广泛
class UrlParams:
    def __init__(self):
        # 请求链接
        self.url = None
        # 请求参数
        self.param = None
        # 请求头
        self.headMap = None

        # 登录信息
        # 请求IP
        self.doMain = 'https://cloud.sendiag.cn'
        # 请求链接(不包含IP部分)
        self.link = None
        self.userName = 'tpson123'
        self.pwd = 'Tpson123456'

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_param(self):
        return self.param

    def set_param(self, param):
        self.param = param

    def get_headMap(self):
        return self.headMap

    def set_headMap(self, headMap):
        self.headMap = headMap


if __name__ == '__main__':
    a = UrlParams()
    for i in a.__dict__:
        print("def get_" + str(i) + "(self):")
        print("    return self." + str(i))
        print("\n")
        print("def set_" + str(i) + "(self, " + str(i) + "):")
        print("    self." + str(i) + " = " + str(i))
        print("\n")
