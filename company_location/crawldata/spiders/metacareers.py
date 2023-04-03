# Copyright: https://crawler.pro.vn
import scrapy,json
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'metacareers'
    cookies = {
    '_fbp': 'fb.1.1673498017212.849554147',
    'wd': '1536x381',
    'datr': 'mo2_Y5kPYnpMv-jN0BTSwdzN',
    'dpr': '1.25',
    'cp_sess': 'FrCp8PnjmDQWHhgOZlMtQ2ZtTEV1b0syWWcWuMr%2BuwwA',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Alt-Used': 'www.metacareers.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}
    PAGE=0
    def start_requests(self):
        for i in range(1,29):
            url='https://www.metacareers.com/jobs/?is_leadership=0&page='+str(i)+'&is_in_page=0'
            yield scrapy.Request(url,headers=self.headers,cookies=self.cookies,dont_filter=True)
    def parse(self, response):
        Data=response.xpath('//a[contains(@href,"/v2/jobs/")]/@href').getall()
        for row in Data:
            url='https://www.metacareers.com'+row
            yield scrapy.Request(url,callback=self.parse_content,headers=self.headers,cookies=self.cookies,dont_filter=True)
        if len(Data)<=0:
            print('\n ----------------')
            yield scrapy.Request(response.url,headers=self.headers,cookies=self.cookies,dont_filter=True)
    def parse_content(self,response):
        TITLE=response.xpath('//div[@class="_9ata _8ww0"]/text()').get()
        if TITLE:
            item={}
            item['Company']='metacareers'
            item['Title']=response.xpath('//div[@class="_9ata _8ww0"]/text()').get()
            item['Location']=''
            item['Salary']=''
            SALA=response.xpath('//div[contains(text(),"$")]/text()').getall()
            if len(SALA)>0:
                item['Salary']=SALA[len(SALA)-1]
            ADD=response.xpath('//span[@class="_8lfp _9a80 _97fe"]//a/text()').getall() or response.xpath('//span[@class="_8lfp _9a80 _97fe"]/text()').getall()
            item['Location']='; '.join(ADD)
            yield(item)
        else:
            print('\n ==============')
            yield scrapy.Request(response.url,callback=self.parse_content,headers=self.headers,cookies=self.cookies,dont_filter=True)
        