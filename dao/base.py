from sqlalchemy import create_engine
import pymysql
# host = 10.0.0.143
# ;database = api_testing
# database = rabbit-v2
# username = root
# passwrod = 123456
engine = create_engine("mysql+pymysql://root:123456@10.0.0.143:3306/device_data?charset=utf8",
                       echo=True,
                       pool_size=1000,
                       pool_recycle=1000*30
                       )
