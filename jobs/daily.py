import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import tasks

from models.StockMaster import StockMaster

if __name__ == "__main__":
    # 종목 업데이트
    tasks.update_corplist()
    # 종목 전체 일일 거래 업데이트
    stocks = StockMaster.objects
    for stock in stocks:
        tasks.update_dailyprice.delay(stock.name, stock.code)