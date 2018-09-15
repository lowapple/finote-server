import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def downloadCorpList():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://bigdata-trader.com/itemcodehelp.jsp') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')

            # 종목 코드 크롤링
            corp_list =  soup.find_all('tr')
            for corp in corp_list:
                corp_detail = corp.select('td')
                corp_code = corp_detail[0].find('a').text
                corp_name = corp_detail[1].text
                corp_type = corp_detail[2].text
                
                print(corp_code + corp_name + corp_type)


loop = asyncio.get_event_loop()
loop.run_until_complete(downloadCorpList())