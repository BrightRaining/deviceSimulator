
class Device_Loc_Config:
    def __init__(self,device_type=None,device_code=None,device_name=None,device_contact=None,device_msg=None,host=None,port=None,device_real_data=None
                 ,alarm_rate=None,fault_rate=None,status=None,device_c16_type=None,socketClient=None):
        self.device_type = device_type
        self.device_code = device_code
        self.device_name = device_name
        self.device_contact = device_contact
        self.device_msg = device_msg
        self.host = host
        self.port = port
        self.device_real_data = device_real_data
        self.alarm_rate = alarm_rate
        self.fault_rate = fault_rate
        self.status = status
        self.device_c16_type = device_c16_type
        self.socketClient = socketClient