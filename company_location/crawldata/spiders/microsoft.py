# Copyright: https://crawler.pro.vn
import scrapy,json
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'microsoft'
    start_urls=['https://careers.microsoft.com/professionals/us/en/search-results']
    START=0
    IDS=[]
    def parse(self, response):
        HTML=str(response.text).split('"eagerLoadRefineSearch":')[1].split('};')[0]
        Data=json.loads(HTML)
        for row in Data['data']['jobs']:
            if not row['jobSeqNo'] in self.IDS:
                self.IDS.append(row['jobSeqNo'])
            item={}
            item['Company']=row['companyName']
            item['Title']=row['title']
            item['Location']=('; '.join(row['multi_location']))
            item['Salary']=''
            HTML=scrapy.Selector(text=row['jobQualifications'])
            SALA=HTML.xpath('//p[contains(text(),"$")]/text()').get()
            if SALA:
                SALAS=str(SALA).split('\\n')
                for SLA in SALAS:
                    if '$' in SLA and item['Salary']=='':
                        item['Salary']=SALA
            yield(item)
        if len(Data['data']['jobs'])>0:
            self.START+=len(Data['data']['jobs'])
            url=self.start_urls[0]+'?from='+str(self.START)+'&s=1'
            yield scrapy.Request(url,callback=self.parse)