# -*- coding: utf-8 -*- 

from pandas import read_html, DataFrame
from models import StockMaster, DailyPrice
import datetime
from celery import Celery
import asyncio

BROKER_URL = 'redis://localhost:6379/0'
app = Celery('tasks', broker=BROKER_URL)


def update_corplist():
    for market in ['kosdaqMkt', 'stockMkt']:
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % market
        code_df = read_html(url, header=0)[0]
        code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
        code_df = code_df[['회사명', '종목코드']]

        for code in code_df.values:
            stock_code = str(code[1])
            stock_name = str(code[0])
            stock = StockMaster.objects(code=stock_code).first()
            if stock is None:
                stock = StockMaster(code=stock_code)
            stock.name = stock_name
            stock.save()


async def fetch_price_df(price_urls):
    async def fetch(price_url):
        return read_html(price_url, header=0)[0]

    price_df = DataFrame()
    price_responses = [fetch(price_url) for price_url in price_urls]
    price_responses = await asyncio.gather(*price_responses)
    for price_response in price_responses:
        price_df = price_df.append(price_response, ignore_index=True)
    return price_df


@app.task
def update_dailyprice(name, code):
    stock_dailyprice_url = 'https://finance.naver.com/item/sise_day.nhn?code=%s' % code
    price_urls = ['{0}&page={1}'.format(stock_dailyprice_url, page) for page in range(1, 21)]
    price_df = asyncio.get_event_loop().run_until_complete(fetch_price_df(price_urls))
    price_df.dropna()
    for price in price_df.values:
        price_date = None
        try:
            price_date = datetime.datetime.strptime(price[0], '%Y.%m.%d')
        except:
            pass

        if price_date is not None:
            daily_price = DailyPrice.objects(code=code, date=price_date).first()
            if daily_price is None:
                daily_price = DailyPrice(
                    code=code,
                    date=price_date,
                    ending_price=price[1],
                    begine_price=price[3],
                    hi_price=price[4],
                    lo_price=price[5],
                    volume=price[6]
                )
                daily_price.save()
    print('%s : %s 업데이트' % (name, code))
