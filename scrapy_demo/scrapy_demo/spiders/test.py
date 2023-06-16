

import scrapy
import requests
from ..items import AItem


class ASpider(scrapy.Spider):
    name = 'A'
    allowed_domains = ['www.ahhhhfs.com']
    base_url = 'https://www.ahhhhfs.com/'
    # start_urls = ['https://www.ahhhhfs.com/']
    start_urls = []
    for i in range(1, 4):
        start_urls.append(base_url+f'page/{i}/')
        

    def parse(self, response):
        for res in response.css('.entry-title *'):
            url = res.css('a::attr(href)').extract()
            title = res.css('a::attr(title)').extract()

            item = AItem()
            item['url'] = url
            item['title'] = title
            yield item

        # print(response.css('.entry-title a::attr(href)').extract())



# import asyncio
# from pyppeteer import launch
# from pyquery import PyQuery as pq
#
# async def main():
#     browser = await launch()
#     page = await browser.newPage()
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
#     }
#     await page.setExtraHTTPHeaders(headers)
#
#     await page.goto('https://www.ahhhhfs.com/')
#     await page.waitFor(5000)
#     # await page.waitForSelector('.main container')
#     doc = pq(await page.content())
#     print(doc)
#     # print('Quotes:', doc('.quote').length)
#     await browser.close()
#
# asyncio.get_event_loop().run_until_complete(main())


