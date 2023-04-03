# Copyright: https://crawler.pro.vn
import scrapy,json,re
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'aesop'
    headers = {'Accept': '*/*','Accept-Language': 'en-GB,en;q=0.5','content-type': 'application/json','x-preview': 'false','x-locale': 'en-US','x-contentful-env': 'master','apollographql-client-name': 'aesop-web-ui','apollographql-client-version': '4.86.0','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin'}
    TT=0
    def start_requests(self):
        URLS=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
        for url in URLS:
            if not str(url).startswith('#'):
                ID=str(url).split('/')
                ID=ID[len(ID)-2]
                url='https://www.aesop.com/graphql?operationName=CategoryAPI&variables=%7B%22category%22%3A%22'+ID+'%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22990d093c83c95b52421f7fca74b22cd86a27a22f34d83c222e1cf8c2a23c884a%22%7D%7D'
                yield scrapy.Request(url,callback=self.parse,headers=self.headers,meta={'ID':ID})
    def parse(self, response):
        ID=response.meta['ID']
        DATA=json.loads(response.text)
        if 'data' in DATA:
            Data=DATA['data']['categoryApi']['subcategories']
            for ROW in Data:
                for row in ROW['aesopProductData']:
                    self.TT+=1
                    print(self.TT,'=>',row['code'])
                    item={}
                    item['KEY_']=ID+'_'+ROW['categoryCode']+'_'+row['code']
                    item['Groups']=ID
                    item['Product URL']=row['linkUrl']
                    item['Product Type']=DATA['data']['categoryApi']['categoryCode']
                    item['Product Subtype']=ROW['name']
                    item['Product Name']=row['name']
                    item['Product Description']=''
                    item['Sizes']=''
                    item['Price']=''
                    for i in range(20):
                        TITLE='field'+str(i)+'Label'
                        VAL='field'+str(i)+'Description'
                        if TITLE in row:
                            item[str(row[TITLE]).lower()]=row[VAL]
                    try:
                        item['Ingredients_text']=cleanhtml(row['ingredientText'])
                    except:
                        item['Ingredients_text']=''
                    for rcs in row['variants']:
                        it={}
                        it.update(item)
                        it['KEY_']+=('_'+rcs['id'])
                        it['Product Description']=rcs['description']
                        it['Sizes']=rcs['size']
                        it['Price']=rcs['price']
                        yield(it)