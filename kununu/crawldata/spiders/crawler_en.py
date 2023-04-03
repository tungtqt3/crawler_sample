# Copyright: https://crawler.pro.vn
import scrapy,json
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'kununu_en'
    def start_requests(self):
        f=open('urls.txt','r')
        URL=f.readlines()
        f.close()
        for url in URL:
            #url=str(url).strip()+'/kommentare'
            if not '#' in url:
                url=str(url).strip()
                yield scrapy.Request(url,callback=self.parse,meta={'page':1,'URL':url})
    def parse(self, response):
        Data=response.xpath('//div[contains(@class,"index__profileContentContainer__")]/div/article[not(contains(@class," "))]')
        for row in Data:
            item={}
            item['URL']=response.meta['URL']
            item['Review Title']=translate(row.xpath('.//h3/text()').get(),'de','en')
            item['Rating']=row.xpath('.//span[contains(@class,"h3-semibold")]/text()').get()
            item['Recommend']=translate(row.xpath('.//span[@class="p-tiny-bold"]/text()').get(),'de','en')
            item['Date']=str(row.xpath('.//time/@datetime').get()).split('T')[0]
            item['Employment Status']=translate(cleanhtml(row.xpath('.//div[contains(@class,"index__employmentInfoBlock__")]/b').get()),'de','en')
            item['Employment Note']=translate(row.xpath('.//div[contains(@class,"index__employmentInfoBlock__")]/span/text()').get(),'de','en')
            data=row.xpath('.//div[contains(@class,"index__factor__")]')
            for rs in data:
                TITLE=translate(rs.xpath('./h4/text()').get(),'de','en')
                TXT=cleanhtml(rs.xpath('./p').get())
                RATE=rs.xpath('.//span[@data-score]/@data-score').get()
                if RATE:
                    item[TITLE+' Rating']=RATE
                    if TXT:
                        item[TITLE+' Review']=translate(TXT,'de','en')
                elif TXT:
                    item[TITLE]=translate(TXT,'de','en')
            #item['KEY_']=key_MD5(str(item['URL'])+str(item['Review Title'])+str(item['Rating'])+str(item['Date'])+str(item['Recommend']))
            yield(item)
        if len(Data)>=10:
            page=response.meta['page']+1
            url=response.meta['URL']+'/'+str(page)
            yield scrapy.Request(url,callback=self.parse,meta={'page':page,'URL':response.meta['URL']})