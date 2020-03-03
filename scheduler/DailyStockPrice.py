import asyncio
import logging
from ._base import BaseScheduler
from pandas import read_html, DataFrame
from datetime import datetime
import models


async def fetch_price_df(price_urls):
    async def fetch(price_url):
        return read_html(price_url, header=0)[0]

    price_df = DataFrame()
    price_responses = [fetch(price_url) for price_url in price_urls]
    price_responses = await asyncio.gather(*price_responses)
    for price_response in price_responses:
        price_df = price_df.append(price_response, ignore_index=True)
    return price_df


class DailyStockPrice(BaseScheduler):
    async def execute(self):
        today = datetime.today().strftime("%Y-%m-%d")
        logging.basicConfig(filename='%s.log' % today, level=logging.INFO)
        logger = logging.getLogger(__name__)

        stocks = models.StockMaster.objects
        for stock in stocks:
            stock_daily_price_url = 'https://finance.naver.com/item/sise_day.nhn?code=%s' % stock.stock_code
            price_urls = ['{0}&page={1}'.format(stock_daily_price_url, page) for page in range(1, 2)]
            price_df = await fetch_price_df(price_urls)
            price_df.dropna()

            for price in price_df.values:
                try:
                    update_date = price[0]
                    update_date = datetime.strptime(update_date, '%Y.%m.%d').date()
                except:
                    update_date = None
                # 일일 가격 업데이트
                if update_date is not None:
                    models.DailyStockPrice(
                        update_date=update_date,
                        stock_code=stock.stock_code,
                        price_close=price[1],
                        price_open=price[3],
                        price_high=price[4],
                        price_low=price[5],
                        volume=price[6]
                    ).save()
                    # 업데이트 로그 출력
                    logger.info('[%s] %s %s 업데이트' % (stock.stock_code, update_date, stock.stock_name))
