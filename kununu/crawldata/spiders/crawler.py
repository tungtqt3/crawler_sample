# Copyright: https://crawler.pro.vn
import scrapy,json
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'kununu'
    def start_requests(self):
        f=open('urls.txt','r')
        URL=f.readlines()
        f.close()
        for url in URL:
            url=str(url).strip()+'/kommentare'
            yield scrapy.Request(url,callback=self.parse,meta={'page':1,'URL':url})
    def parse(self, response):
        Data=response.xpath('//div[contains(@class,"index__profileContentContainer__")]/div/article[not(contains(@class," "))]')
        for row in Data:
            item={}
            item['Review Title']=row.xpath('.//h3/text()').get()
            item['Rating']=row.xpath('.//span[contains(@class,"h3-semibold")]/text()').get()
            item['Recommend']=row.xpath('.//span[@class="p-tiny-bold"]/text()').get()
            item['Date']=str(row.xpath('.//time/@datetime').get()).split('T')[0]
            item['Employment Status']=cleanhtml(row.xpath('.//div[contains(@class,"index__employmentInfoBlock__")]/b').get())
            item['Employment Note']=row.xpath('.//div[contains(@class,"index__employmentInfoBlock__")]/span/text()').get()
            data=row.xpath('.//div[contains(@class,"index__factor__")]')
            for rs in data:
                TITLE=rs.xpath('./h4/text()').get()
                TXT=cleanhtml(rs.xpath('./p').get())
                RATE=rs.xpath('.//span[@data-score]/@data-score').get()
                
                if RATE:
                    item[TITLE+' Rating']=RATE
                    if TXT:
                        item[TITLE+' Review']=TXT
                elif TXT:
                    item[TITLE]=TXT
            yield(item)
        if len(Data)>=10:
            page=response.meta['page']+1
            url=response.meta['URL']+'/'+str(page)
            yield scrapy.Request(url,callback=self.parse,meta={'page':page,'URL':response.meta['URL']})