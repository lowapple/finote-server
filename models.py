# models.py 파일
# coding: utf-8

from mongoengine import connect, Document, StringField, DateField, LongField

connect('finote')


# 종목 정보
# 종목 코드 / 이름
class StockMaster(Document):
    stock_code = StringField()
    stock_name = StringField(default='')


# 일일 종목별 거래 
class DailyStockPrice(Document):
    # 날자
    update_date = DateField()
    # 종목 코드
    stock_code = StringField()
    # 시가
    price_open = LongField()
    # 종가
    price_close = LongField()
    # 고가
    price_high = LongField()
    # 저가
    price_low = LongField()
    # 거래량
    volume = LongField()
