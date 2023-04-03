# Copyright: https://crawler.pro.vn
import scrapy,json,re
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'careers_google'
    start_urls=['https://careers.google.com/api/v3/search/?page=1']
    def parse(self, response):
        Data=json.loads(response.text)
        for row in Data['jobs']:
            item={}
            item['Company']=row['company_name']
            item['Title']=row['title']
            item['Location']=''
            item['Salary']=''
            HTML=scrapy.Selector(text=row['description'])
            SALA=HTML.xpath('//p[contains(text(),"$") and (contains(text(),"Salary") or contains(text(),"salary"))]/text()').get()
            if SALA:
                SALAS=str(SALA).split('\\n')
                for SLA in SALAS:
                    if '$' in SLA and item['Salary']=='':
                        item['Salary']=SALA
            ADD=[]
            for rs in row['locations']:
                ADD.append(', '.join(rs['address_lines']))
            item['Location']=('; '.join(ADD))

            yield item
        if len(Data['jobs'])>0:
            url='https://careers.google.com/api/v3/search/?page='+str(Data['next_page'])
            yield scrapy.Request(url,callback=self.parse)
