import scrapy,re
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'amazon_price'
    cookies = {
    'csm-hit': 'tb:C5ZR8C8HN9CWRXBTKJDC+s-C5ZR8C8HN9CWRXBTKJDC^|1674708959429&t:1674708959429&adb:adblk_no',
    'session-id': '146-5848512-1515966',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'ubid-main': '133-4943341-2530334',
    'session-token': 'tSF0BpgYRS38v/Axs9s8GBu+lGYZciLl41dZNt26eiMwLsX1IrKS9XMgdydjMrFn8eebRn/bxvtFh39+AKrZW2pVaZ6yJXfOCa6oNDXXNYzdNmHnwrFYGZtBH7lpqkJuwiGf6jWXktVpKsn0UXRJt9juOUlRMX6KmECiCMga3+0bVmDmzL7uzxUglvqihsTGwTW9ajCb9XD1LDDNF5LDP2sMSrEXpSMwrmRPgQkN1Q0=',
    'regStatus': 'registered',
    'aws-ubid-main': '780-1845330-5853020',
    'aws-account-alias': '637307937437',
    'remember-account': 'false',
    'aws-userInfo': '^%^7B^%^22arn^%^22^%^3A^%^22arn^%^3Aaws^%^3Aiam^%^3A^%^3A637307937437^%^3Auser^%^2Fbradford^%^22^%^2C^%^22alias^%^22^%^3A^%^22637307937437^%^22^%^2C^%^22username^%^22^%^3A^%^22bradford^%^22^%^2C^%^22keybase^%^22^%^3A^%^221arrgEfhu7Z86Qb9B6uuXU6dRIb0yTZVX7Blp3CyH9k^%^5Cu003d^%^22^%^2C^%^22issuer^%^22^%^3A^%^22http^%^3A^%^2F^%^2Fsignin.aws.amazon.com^%^2Fsignin^%^22^%^2C^%^22signinType^%^22^%^3A^%^22PUBLIC^%^22^%^7D',
    'aws-userInfo-signed': 'eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTIiLCJhbGciOiJFUzM4NCIsImtpZCI6IjM1NzUwMzg2LWU5OTQtNDU5OC1hNzAxLTI0NmQ2MTEyMjgwNSJ9.eyJzdWIiOiI2MzczMDc5Mzc0MzciLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiMWFycmdFZmh1N1o4NlFiOUI2dXVYVTZkUkliMHlUWlZYN0JscDNDeUg5az0iLCJhcm4iOiJhcm46YXdzOmlhbTo6NjM3MzA3OTM3NDM3OnVzZXJcL2JyYWRmb3JkIiwidXNlcm5hbWUiOiJicmFkZm9yZCJ9.FwOEZ7rY8lB1FtbBMDs3_IvGzwPw4JOfHmkweiFF2SapZZ9iPRtx3bV-DEbwl16E29_gHjMun0cWn_FQ7GS9XbjERnWxsC69ZByfZpObbubmCOijNP8gAQCABPdVCeQN',
    'noflush_awsccs_sid': '73eaf127fc07a8f95ed62b792f7dfdfd2e7595a2b383ba134a74731ba8b0efd2',
    'aws-signer-token_us-west-2': 'eyJrZXlWZXJzaW9uIjoieGYyNUZtbERwQ2dQdnZMLkV3NWRSc2lWdU15bUpsN3MiLCJ2YWx1ZSI6Ilg2MmxzUW5pWWI5TGRJcnhjeFRzL0NjeUZqeENHSWdNTXVPbW8zOENhYk09IiwidmVyc2lvbiI6MX0=',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}
    def start_requests(self):
        URLS=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
        for url in URLS:
            if not str(url).startswith('#'):
                yield scrapy.Request(url,callback=self.parse,meta={'URL':url},cookies=self.cookies,headers=self.headers)
    def parse(self, response):
        URL=response.meta['URL']
        Data=response.xpath('//div[@data-component-type="s-search-result"]')
        for row in Data:
            item={}
            item['URL']=URL
            item['Title']=str(row.xpath('.//h2/a/span/text()').get()).strip()
            item['Rating']=(str(row.xpath('.//span[@class="a-icon-alt"]/text()').get()).strip()).split()[0]
            item['Reviews']=row.xpath('.//span[@class="a-size-base s-underline-text"]/text()').get()
            item['Original Price']=row.xpath('.//span[@data-a-strike="true"]/span[@class="a-offscreen"]/text()').get()
            item['Price']=row.xpath('.//span[@data-a-color="base"]/span[@class="a-offscreen"]/text()').get()
            PR=row.xpath('.//span[@class="a-size-base a-color-secondary" and(contains(text(),"$"))]/text()').get()
            if PR:
                item['Price/Oz']=str(PR).split('(')[1].split('/')[0]
            else:
                item['Price/Oz']=''
            item['SNAP Eligible']='No'
            SNAP=row.xpath('.//span[contains(text(),"SNAP EBT eligible")]')
            if SNAP:
                item['SNAP Eligible']='Yes'
            yield item
        next_page=response.xpath('//a[contains(@class,"pagination-next")]/@href').get()
        if next_page:
            url='https://www.amazon.com'+next_page
            yield scrapy.Request(url,callback=self.parse,meta={'URL':URL},cookies=self.cookies,headers=self.headers)