# coding: utf-8

import logging

from datetime import datetime
from pandas import read_html
from models import StockMaster

from ._base import BaseScheduler


class DailyStockMaster(BaseScheduler):
    async def execute(self):
        today = datetime.today().strftime("%Y-%m-%d")
        logging.basicConfig(filename='%s.log' % today, level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info('StockMaster Update Start')
        # Stock Update
        for market in ['kosdaqMkt', 'stockMkt']:
            url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % market
            code_df = read_html(url, header=0)[0]
            code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
            code_df = code_df[['회사명', '종목코드']]
            # 종목 코드 업데이트
            for code in code_df.values:
                stock_code = str(code[1])
                stock_name = str(code[0])
                logger.info('Stock [%s] %s' % (stock_code, stock_name))
                stock = StockMaster.objects(stock_code=stock_code).first()
                if stock is None:
                    stock = StockMaster(stock_code=stock_code)
                stock.stock_name = stock_name
                stock.save()
