from mongoengine import *

# 종목 정보
# 종목 코드 / 이름
class StockMaster(Document):
    code = StringField()
    name = StringField(default='')