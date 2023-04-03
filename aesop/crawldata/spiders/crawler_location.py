# Copyright: https://crawler.pro.vn
import scrapy,json,re,requests
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'aesop_location'
    cookies = {
    '_abck': '3F1F351AB26269CE3A10B24ADEB29169~-1~YAAQVS43FyE91HeFAQAA5F1Pmgn57BsLxrKV9KsB96OA6ENk4nO8plpO8G2A0aLF3bHcHMc87EumeA8copXVhwDH5PR3Uors+7QjAnvCdu1dUyUAHIJqj8B0jPYkAqxyc/AvdKj5wnr3Qdp1WfHCGyS6rTZ/eXdRYVXfoCxn9WIFQdp97E/YAO0cIfG3+9w5uw20H991K3fR1aJwT/8XoQOpQSJxjEjJouTg552gleCV4rLIC+RsahKK3jW7v4LUm7ri5afGQk9O7NAcj1fGf3Jxgb03I9ZEVGYFKEHkjR4ChRGpAlaojkPO9w1bi+DQ0JnlRB4UouDqg5505k1LxNgEvH87NEvlUcRq+2wnlyoVbH9h9XBMnwrmHRhRm6E=~-1~-1~-1',
    'RT': 'z=1&dm=www.aesop.com&si=1a44e53c-de1e-4827-97df-7fbc497b50af&ss=lcpsrkjz&sl=0&tt=0&bcn=%2F%2F684d0d44.akstat.io%2F',
    'initial_session_source': '',
    'km_ai': 'HKisrxTvUwNLuh6i940cWkjFzsQ%3D',
    'km_lv': 'x',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Jan+10+2023+13%3A04%3A22+GMT%2B0700+(Indochina+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=eac1f1c0-108c-45c2-8d1d-f93c4bde0d50&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=VN%3BHN&AwaitingReconsent=false',
    '__zlcmid': '1DqlVtRGgllkQGz',
    'OptanonAlertBoxClosed': '2023-01-09T14:34:12.118Z',
    '_gcl_au': '1.1.1391547434.1673274852',
    '_ga_EGJBD3JJDM': 'GS1.1.1673327762.5.1.1673331170.0.0.0',
    '_ga': 'GA1.2.299958736.1673274852',
    '_ga_P5HKP37923': 'GS1.1.1673312673.2.1.1673313500.0.0.0',
    '_gid': 'GA1.2.839628980.1673274853',
    '_pin_unauth': 'dWlkPVptUXlZVFU1TkRJdE1tSTBNUzAwWmprekxUaG1ZamN0WlRrNE56YzNORFkyT0RNeQ',
    '_fbp': 'fb.1.1673274853515.446078125',
    'fs_uid': '#NAFZX#6347982570475520:6121206472724480:::#/1704810853',
    '_ga_TLT0NBNW84': 'GS1.1.1673327762.5.1.1673331170.0.0.0',
    'bm_sz': 'FF00FFB33BFDB205C76874407554DAA4~YAAQVS43F6xD03eFAQAAD+rPmRJQfYDF3pvib+AvaUydfbtfAQXPQpBjnlW0KeKmFGGcsEuLOKAQWM4p3MGHoinQsPsDLoNI+sudrF1MsPGlDEn+LYW7f4ruTlN3LQ4cPrLdU2M7pKwaKKs/9c45MqULc7R9hNGy2Hq9ErTWHADXZ5NYpBzms/kzU0Z6Jv8e9BCq6vAqbDigSC9RbC0LhWnx7CgDwK3mK6quPv5bHdnk5b+lTM6+8qeNS3lsFIp+50w1RZ0++PI1cEDaY9KTE3ABPwAdNx6EddNnMWm0zcXxkmIT5iqMoJGVvr58MVwLITgEtvx8Z0eBnQ==~3354949~3159865',
    'JSESSIONID': 'Y4-dc4c9836-d0cf-47c9-9eaf-f0b87d127dbc.accstorefront-6447fff77f-v7njl',
    'ROUTE': '.accstorefront-6447fff77f-v7njl',
    'kvcd': '1673331171353',
    'AKA_A2': 'A',
    'ak_bmsc': 'DECC3179DBD0C4B5E2A65AF9403D3B0A~000000000000000000000000000000~YAAQHAvGFz5fDReFAQAAymUbmhIrxA16/s+uaLaJPRy0JlvmuXSsXiBKdSNIvI8tHBWlDSZOi0FFm5fVU1cjEfEypv6JTi3fGkrYKcIYmbXbt7r6lrUNka4xWUrEzLow62mCVpN3mXZ5Dn2xs+51g4vyu3U0OWi0pSnmG6ew/ji7TJG6aLqHphe49dZcgNTb/yXwFhuUByS75Si3hV18HWDzSrnoaPh3pCjYbehyIgdZE2wbByOPf0wqhTcTn9qC+TZ0xGqOVUS4Bu1M2d8RSe3OF7Cf3UqjR6a3NMcPtSJ3Ft8iA29BwR5ICt0Ve6340aGHN9LphclUPWegnjN6R4yFstnu/VyXp06LD4eWlHl/sFtPf+YnVaAGZ4oOUFY39qXXJBxLnclIMYZJ9H6EhRiBufPCrj8J0t56ib6L7dieQOXSaJUO4TSOLhBJao/kI3CMG7HhX7/IiOBRlWNWO6zmPJprT1iIHwpT6wU/9oiJ/ntH5bwCKZA=',
    'km_vs': '1',
    'bm_sv': 'EF1246A18462DB5900E39C1CD90A07D9~YAAQVS43FyI91HeFAQAA5F1PmhLkvnZEJO79hkNdbKVWl1m+TwnDcsWMC8EynKmuI7bWn4wn05qNWiNzGNeqkjKeu2E1dgOfpsDWoaCuJLXsDBoQhCCaRshIusAyDThWs1tIxkgvZUWM8gTAOEVUC+4ui+yTJ+6megqxt1Qned2zF+wzrMK82YHmmLIDCeOUTUR1x+aDTbHZNnAtOFqxOvX4au0jR9/GkHEQJsxC7WXkfESVapbboyRuIn7ZmG9M~1',
}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'content-type': 'application/json',
    'x-preview': 'false',
    'x-api-key': 'unPGMTFfsi1fyT9Fi03Ee6Ds5LMhatBh7LZtQ7o8',
    'x-locale': 'en-US',
    'x-contentful-env': 'master',
    'apollographql-client-name': 'aesop-web-ui',
    'apollographql-client-version': '4.86.0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
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
                yield scrapy.Request('http://httpbin.org/ip',callback=self.parse,headers=self.headers,meta={'URL':url,'ID':ID},dont_filter=True)
    def parse(self, response):
        URL=response.meta['URL']
        ID=response.meta['ID']
        params = {'operationName': 'getPage','variables': '{"uri":"/'+ID+'/"}','extensions': '{"persistedQuery":{"version":1,"sha256Hash":"63274c7310f7188e483af5705779fdbfdd4746fc641a3725ca339a907d34e308"}}',}
        response = requests.get('https://www.aesop.com/graphql', params=params, cookies=self.cookies, headers=self.headers)
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
