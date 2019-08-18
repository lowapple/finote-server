# -*- coding: utf-8 -*- 

from pandas import read_html
from models.StockMaster import StockMaster

def sync():
    update_corplist()

def update_corplist():
    for market in ['kosdaqMkt','stockMkt']:
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % market
        code_df = read_html(url, header=0)[0]
        code_df = code_df[['회사명','종목코드']]
        code_df = code_df.rename(columns={
            '회사명' : 'name', 
            '종목코드' : 'code'
        })
        
        for code in code_df.values:
            stock_code = str(code[1])
            stock_name = str(code[0])
            stock = StockMaster.objects(code=stock_code).first()
            if stock is None:
                stock = StockMaster(code=stock_code)
            stock.name = stock_name
            stock.save()