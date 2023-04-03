import scrapy,json,re
from crawldata.functions import *

class CrawlerSpider(scrapy.Spider):
    name = 'gartner'
    def start_requests(self):
        f=open('Audit_urls.txt','r')
        URLS=re.split('\r\n|\n',f.read())
        f.close()
        for rows in URLS:
            if not str(rows).startswith('#'):
                if '~' in str(rows):
                    row=str(rows).split('~')
                    url=row[1]
                    company=row[0]
                else:
                    url=rows
                    company=''
                print(url)
                yield scrapy.Request(url,callback=self.parse,meta={'Company':company},dont_filter=True)
    def parse(self, response):
        Company=response.meta['Company']
        if Company=='':
            Company=str(response.url).split('/')
            Company=Company[len(Company)-2]
        DATA=response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        DATA=json.loads(DATA)
        try:
            Data=DATA['props']['pageProps']['serverSideXHRData']['source-ratings-vendor']['productView']
        except:
            Data=DATA['props']['pageProps']['serverSideXHRData']['source-ratings-product']['productView']
        ITEM={}
        ITEM['Company']=(str(Company).replace('-',' ')).title()
        ITEM['URL']=response.url
        ITEM['Category']=Data['marketDTO']['name']
        ITEM['Product Average Rating']=Data['vendorReviewDTO']['averageRating']
        ITEM['Total Num Reviews']=Data['vendorReviewDTO']['ratingsCount']
        ITEM['Total Num Verified Reviews']=0
        #ID=str(response.url).split('/vendor/')[1].split('/')[0]
        #MARKETS=response.xpath('//link[@id="head-link"]/@href').get()
        #MARKET=str(MARKETS).split('/market/')[1].split('/')[0]
        #PRODUCT=str(MARKETS).split('/product/')[1].split('/')[0]
        ID=Data['vendorReviewDTO']['seoName']
        MARKET=Data['marketDTO']['seoName']
        for row in Data['productDTOs']:
            PRODUCT=row['seoName']
            FROM=1
            url='https://www.gartner.com/reviews/api2-proxy/reviews/market/vendor/filter?vendorSeoName='+ID+'&marketSeoName='+MARKET+'&productSeoName='+PRODUCT+'&startIndex='+str(FROM)+'&endIndex='+str(FROM+1999)+'&filters=%7B%22products%22%3A%5B%5D%2C%22reviewRating%22%3A%5B%5D%2C%22companySize%22%3A%5B%5D%2C%22industry%22%3A%5B%5D%2C%22deploymentRegion%22%3A%5B%5D%2C%22jobRole%22%3A%5B%5D%2C%22tags%22%3A%5B%5D%7D&sort=-helpfulness'
            yield scrapy.Request(url,callback=self.parse_reviews,meta={'FROM':FROM,'ID':ID,'MARKET':MARKET,'PRODUCT':PRODUCT,'ITEM':ITEM,'URL':url},dont_filter=True)
    def parse_reviews(self,response):
        FROM=response.meta['FROM']
        ID=response.meta['ID']
        MARKET=response.meta['MARKET']
        PRODUCT=response.meta['PRODUCT']
        ITEM=response.meta['ITEM']
        DATA=json.loads(response.text)
        if FROM==1:
            ITEM['Total Num Verified Reviews']=DATA['totalCount']
        Data=DATA['userReviews']
        for row in Data:
            url='https://www.gartner.com/reviews/market/crm-customer-engagement-center/vendor/'+row['vendorSeoName']+'/product/'+row['productSeoNames'][0]+'/review/view/'+str(row['reviewId'])
            yield scrapy.Request(url,callback=self.parse_content,meta={'ITEM':ITEM,'ROW':row,'dont_redirect': True,'URL':url},dont_filter=True)
        # Next page
        if DATA['nextPage']>0:
            FROM+=len(Data)
            url='https://www.gartner.com/reviews/api2-proxy/reviews/market/vendor/filter?vendorSeoName='+ID+'&marketSeoName='+MARKET+'&productSeoName='+PRODUCT+'&startIndex='+str(FROM)+'&endIndex='+str(FROM+1999)+'&filters=%7B%22products%22%3A%5B%5D%2C%22reviewRating%22%3A%5B%5D%2C%22companySize%22%3A%5B%5D%2C%22industry%22%3A%5B%5D%2C%22deploymentRegion%22%3A%5B%5D%2C%22jobRole%22%3A%5B%5D%2C%22tags%22%3A%5B%5D%7D&sort=-helpfulness'
            yield scrapy.Request(url,callback=self.parse_reviews,meta={'FROM':FROM,'ID':ID,'MARKET':MARKET,'PRODUCT':PRODUCT,'ITEM':ITEM,'URL':url},dont_filter=True)
    def parse_content(self,response):
        item=response.meta['ITEM']
        ROW=response.meta['ROW']
        URL=response.meta['URL']
        try:
            JSDATA=response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
            JSDATA=json.loads(JSDATA)
            item['Review URL']=URL
            item['KEY_']=item['Company']+'_'+key_MD5(URL)
            REVIEW=JSDATA['props']['pageProps']['serverSideXHRData']['getReviewPresentation']['review']
            USER=REVIEW['user']
            try:
                item['Reviewer Title']=USER['title']
            except:
                item['Reviewer Title']=''
            try:
                item['Reviewer Industry']=USER['industry']
            except:
                item['Reviewer Industry']=''
            try:
                item['Reviewer Role']=USER['role']
            except:
                item['Reviewer Role']=''
            try:
                item['Reviewer Firm Size']=USER['companySize']
            except:
                item['Reviewer Firm Size']=''
            try:
                item['Reviewer Deployment Architecture']=REVIEW['deploymentArchitecture']
            except:
                item['Reviewer Deployment Architecture']=''
            try:
                item['Go-Live Date']=REVIEW['goLiveYear']
            except:
                item['Go-Live Date']=''
            try:
                item['Implementation Strategy']=REVIEW['implementationStrategy']
            except:
                item['Implementation Strategy']=''
            try:
                item['Review Source']=REVIEW['source']
            except:
                item['Review Source']=''
            item['Title']=ROW['reviewHeadline']
            item['Date']=ROW['formattedReviewDate']
            item['Overall User Rating']=ROW['reviewRating']
            item['Products Reviewed']=ROW['productNames']
            try:
                item['Overall Comment']=ROW['reviewSummary']
            except:
                item['Overall Comment']=''
            SECTIONS=REVIEW['sections']
            for rs in SECTIONS:
                if 'ratingValue' in rs:
                    item[rs['title']]=rs['ratingValue']
            tmp={}
            tmp['What do you like most']="lessonslearned-like-most"
            tmp['What do you dislike most']="lessonslearned-dislike-most"
            tmp['Business problems/needs that prompted purchase']="business-problem-solved"
            tmp['What would you do differently if you could start over']="lessonslearned-you-did-differently-v2"
            tmp['Advice for prospective customers']="lessonslearned-advice"
            tmp['Why did you purchase']="why-purchase-s24"
            tmp['Key factors that drove your decision']="factors-drove-decision-s24"
            tmp['Other vendors considered']="vendors-considered"
            tmp['Version number(s) currently in use in your organization']="version-number"
            tmp['How extensively is the product used in your org']="deployment-scale"
            tmp['When was it deployed at your org']="go-live-year-"
            tmp['How long did deployment take']="deployment-time"
            tmp['What was your implementation strategy']="implementation-strategy"
            tmp['Deployment architecture']="deployment-architecture-s24"
            tmp['Country of deployment']="deployment-country-multi"
            tmp['Length of usage']="time-used-service"
            tmp['Frequency of usage']="frequency-of-usage"
            tmp['Your role with product']="role-product-optional"
            for k,v in tmp.items():
                item[k]=''
                for rs in SECTIONS:
                    if 'questions' in rs:
                        rcs=rs['questions']
                        for rss in rcs:
                            if v in rss['key']:
                                if isinstance(rss['value'],list):
                                    item[k]='; '.join(rss['value'])
                                else:
                                    item[k]=rss['value']
            yield(item)
        except:
            yield scrapy.Request(response.url,callback=self.parse_content,meta={'ITEM':ITEM,'ROW':row,'dont_redirect': True,'URL':url},dont_filter=True)
