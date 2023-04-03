# Copyright: https://crawler.pro.vn
import scrapy,re
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'stackoverflow'
    def start_requests(self):
        URL=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
        for url in URL:
            if not str(url).startswith('#'):
                Group=str(url).split('/')
                Group=Group[len(Group)-1]
                for i in range(20):
                    urls=url+'?tab=newest&pagesize=50&page='+str(i+1)
                    yield scrapy.Request(urls,callback=self.parse,meta={'Group':Group,'page':i+1,'URL':url})
    def parse(self, response):
        Page=response.meta['page']
        URL=response.meta['URL']
        Group=response.meta['Group']
        Data=response.xpath('//div[@data-post-id]')
        for row in Data:
            VAL=row.xpath('.//span[@class="s-post-summary--stats-item-number"]/text()').getall()
            TITLE=row.xpath('.//span[@class="s-post-summary--stats-item-unit"]/text()').getall()
            item={}
            item['Group']=Group
            item['Question URL']='https://stackoverflow.com'+row.xpath('.//h3/a/@href').get()
            item['Question Title']=row.xpath('.//h3/a/text()').get()
            item['Date']=str(row.xpath('.//time/span[@title]/@title').get()).split()[0]
            item['# of Views']=0
            item['# of Answers']=0
            item['# of Votes']=0
            for i in range(len(TITLE)):
                if 'answer' in str(TITLE[i]).lower():
                    item['# of Answers']=VAL[i]
                if 'votes' in str(TITLE[i]).lower():
                    item['# of Votes']=VAL[i]
                if 'views' in str(TITLE[i]).lower():
                    item['# of Answers']=VAL[i]
            item['KEY_']=key_MD5(item['Question URL'])
            yield(item)
        if len(Data)>0:
            ITEM={}
            ITEM['KEY_']=Group+'_'+str(Page)
            ITEM['SHEET']='Summary'
            ITEM['Group']=Group
            ITEM['Page']=Page
            ITEM['Records']=len(Data)
            yield(ITEM)
            urls=URL+'?tab=newest&pagesize=50&page='+str(Page+20)
            yield scrapy.Request(urls,callback=self.parse,meta={'Group':Group,'page':Page+20,'URL':URL})
        #next_page=response.xpath('//a[@rel="next"]/@href').get()
        #if next_page:
        #    url='https://stackoverflow.com'+next_page
        #    yield scrapy.Request(url,callback=self.parse,meta={'Group':Group})