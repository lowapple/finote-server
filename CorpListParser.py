import asyncio
import aiohttp
from bs4 import BeautifulSoup
from slacker import Slacker
from config import Config

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

            slack_body = dict()
            slack_body['title'] = "종목코드가 전부 업데이트 되었습니다."
            slack_body['fallback'] = "종목코드가 전부 업데이트 되었습니다."

            attachments = [slack_body]

            slack = Slacker(Config().slack_token)
            slack.chat.post_message(
                channel='#corp_update', 
                text=None,
                attachments=attachments)


loop = asyncio.get_event_loop()
loop.run_until_complete(downloadCorpList())