# Copyright: https://crawler.pro.vn
import scrapy,json,re
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'aesop_location_scrapy'
    headers = {'Accept': '*/*','Accept-Language': 'en-GB,en;q=0.5','content-type': 'application/json','x-preview': 'false','x-locale': 'en-US','x-contentful-env': 'master','apollographql-client-name': 'aesop-web-ui','apollographql-client-version': '4.86.0','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin'}
    try:
        CRAWLED=re.split('\r\n|\n', open('CRAWLED.txt','r',encoding='utf-8').read())
    except:
        CRAWLED=[]
    def start_requests(self):
        URLS=re.split('\r\n|\n', open('location_urls.txt','r',encoding='utf-8').read())
        for url in URLS:
            if not str(url).startswith('#') and not url in self.CRAWLED:
                ID=str(url).split('/')
                ID=ID[len(ID)-2]
                urls='https://www.aesop.com/graphql?operationName=getPage&variables=%7B%22uri%22%3A%22%2F'+ID+'%2F%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2263274c7310f7188e483af5705779fdbfdd4746fc641a3725ca339a907d34e308%22%7D%7D'
                yield scrapy.Request(urls,callback=self.parse,headers=self.headers,meta={'URL':url})
    def parse(self, response):
        URL=response.meta['URL']
        DATA=json.loads(response.text)
        if 'data' in DATA:
            row=DATA['data']['readPage']
            item={}
            item['KEY_']=row['id']
            item['Store URL']=URL
            item['Store Type']=row['storeType']
            item['Store Name']=row['name']
            item['Store Location']=row['formattedAddress']
            item['Store Email']=row['email']
            item['Store Phone']=row['phone']
            OPENTIME=[]
            if row['openingHours']:
                for k,v in (row['openingHours']).items():
                    try:
                        TXT=str(k).title()+': '+str(v['openingTimeHour'])+':'+str(v['openingTimeMinute'])+' - '+str(v['closingTimeHour'])+':'+str(v['closingTimeMinute'])
                        print(TXT)
                        OPENTIME.append(TXT)
                    except:
                        pass
            item['Store Opening Hours']='; '.join(OPENTIME)
            item['Store Info']=''
            item['Store Description']=''
            INFO=[]
            DESC=[]
            for rs in row['contentSection']:
                if rs['__typename']=="SliceTwoColumnType":
                    if 'narrowColumn' in rs:
                        if rs['narrowColumn']:
                            if rs['narrowColumn']['title']:
                                INFO.append(rs['narrowColumn']['title'])
                    if 'wideColumn' in rs:
                        if rs['wideColumn']:
                            if rs['wideColumn']['copy']:
                                for rcs in rs['wideColumn']['copy']['parsed']['content']:
                                    if rcs['content'][0]['value']:
                                        DESC.append(rcs['content'][0]['value'])

            item['Store Info']='\n '.join(INFO)
            item['Store Description']='\n '.join(DESC)
            yield(item)
            f=open('CRAWLED.txt','a',encoding='utf-8')
            f.write('\n'+URL)
            f.close()
