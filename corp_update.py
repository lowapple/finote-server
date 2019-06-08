import pandas

def getStockCode(market):
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % market
    df = pandas.read_html(url, header=0)[0]
    return df

if __name__ == '__main__':
    for market in ['kosdaqMkt','stockMkt']:
        result_df = getStockCode(market)
        result_df.to_csv('%s.csv' % market)
        print(result_df[['회사명','종목코드','업종','주요제품','결산월']])