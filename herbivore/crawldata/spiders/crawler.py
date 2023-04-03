import scrapy,json,re
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'herbivore'
    def start_requests(self):
        URLS=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
        for url in URLS:
            yield scrapy.Request(url,callback=self.parse,meta={'URL':url})
    def parse(self, response):
        HTML=response.xpath('//script[@id="oke-reviews-settings"]/text()').get()
        Data=json.loads(HTML)
        subscriberId=str(Data['subscriberId'])
        Data=response.xpath('//script[@id="__st"]/text()').get()
        HTML=Data.split('__st=')[1].split(';')[0]
        Data=json.loads(HTML)
        product_id=str(Data['rid'])
        url='https://api.okendo.io/v1/stores/'+subscriberId+'/products/shopify-'+product_id+'/reviews?limit=100&orderBy=rating%20desc'
        yield scrapy.Request(url,callback=self.parse_review,meta=response.meta)
    def parse_review(self,response):
        DATA=json.loads(response.text)
        Data=DATA['reviews']
        for row in Data:
            item={}
            item['URL']=response.meta['URL']
            item['Stars']=row['rating']
            item['Date']=str(row['dateCreated']).split('T')[0]
            item['Title']=row['title']
            item['Text']=row['body']
            if 'productAttributes' in row:
                for rs in row['productAttributes']:
                    item[rs['title']]='; '.join(rs['value'])
            if 'reviewer' in row:
                if 'attributes' in row['reviewer']:
                    for rs in row['reviewer']['attributes']:
                        if isinstance(rs['value'], list):
                            item[rs['title']]=', '.join(rs['value'])
                        else:
                            item[rs['title']]=rs['value']
            yield(item)
        if 'nextUrl' in DATA:
            url='https://api.okendo.io/v1'+DATA['nextUrl']
            yield scrapy.Request(url,callback=self.parse_review,meta=response.meta)



