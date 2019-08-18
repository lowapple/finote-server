import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import tasks

from models.StockMaster import StockMaster

if __name__ == "__main__":
    tasks.update_corplist()
    stocks = StockMaster.objects
    for stock in stocks:
        tasks.update_dailyprice.delay(stock.name, stock.code)