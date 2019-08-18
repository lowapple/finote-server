from mongoengine import *

class DailyPrice(Document):
    # 날자
    date = DateField()
    # 종목 코드
    code = StringField()
    # 시가
    begine_price = LongField()
    # 종가
    ending_price = LongField()
    # 고가
    hi_price = LongField()
    # 저가
    lo_price = LongField()
    # 거래량
    volume = LongField()