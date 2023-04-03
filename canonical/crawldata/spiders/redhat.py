# Copyright: https://crawler.pro.vn
import scrapy
from urllib.parse import quote
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'redhat'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-GB,en;q=0.5','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'same-origin','Sec-Fetch-User': '?1',}
    cookies={'notice_behavior':'implied,eu','AMCV_945D02BE532957400A490D4C%40AdobeOrg':'179643557%7CMCIDTS%7C19364%7CMCMID%7C13067108014768817952282484282377850093%7CMCAAMLH-1673578629%7C3%7CMCAAMB-1673578629%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1672981029s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19371%7CvVersion%7C5.5.0','mbox':'session#0880f9c36b7c4858a864144f22f61ac4#1672975777|PC#0880f9c36b7c4858a864144f22f61ac4.38_0#1736218714','at_check':'true','rh_omni_tc':'701f2000001OH6kAAG','chrome_session_id':'376110|1672973828823','sat_ppv':'5','AMCVS_945D02BE532957400A490D4C%40AdobeOrg':'1','sat_prevExtCmp':'701f2000001OH6kAAG','s_ecid':'MCMID%7C13067108014768817952282484282377850093','scCidHist':'701f2000001OH6kAAG','s_cc':'true','aam_did':'20285184268851127111272798038782051049','notice_preferences':'2:','notice_gdpr_prefs':'0,1,2:','s_sq':'%5B%5BB%5D%5D','cmapi_gtm_bl':'','cmapi_cookie_privacy':'permit 1,2,3','rh_common_id':'790195fc-d12b-43a2-859c-02b83a322b6b','ak_bmsc':'4A4CCF561AFAB312825CEB5542C8F0D5~000000000000000000000000000000~YAAQ5lJNG4gGL4KFAQAADZYDhRIdzQIVD3O6STj7VVN/WJlCDjy6PqDVNXSIP0ZbNiVvIuamw94R4y6s79Kp884NrU2DxgpAqUZCsRqx2VSGCpiKwdjS6i0goAMYw1XykeeZ+JtpT98pnCJvHMPErSEOEnHWj2cFQXDVS31gssT/9cWfHx+tS2d1uhDpuBc+sptpVOphA6L9woqP7CQf5zX0+4Y8cfpg2el5bpY1s3vXtUa+pLZdgBC233MjMo3x9CimUfLg2uyB9PR7MqKRYTPMMq5ySWIh3VUL34fY4F6dXOYJKYsPJoiiy38AFJQrFKiTBr6FvkCMkQzfyeGhiX5Er3qP1rNxsmLey5+Aa8ikDqvC8Yzuyq8VP/WLnE9AffV4hafPYaSfFaKDjIkgWxRsZSzQ5PZw+s/aKkprJtcpRpXu7lAUhSuGSszl7pCFTyW6VsTx75q+8hZk/NIsFGm8H3ANkuaxhNn6q108NQJHyKaIon6WXjQ=','sat_prevInternalCampaign':'','sat_prevExtCmp':'no%20value','bm_sv':'853C11F62E3082B8374D143B5057F672~YAAQFBQgF/dAHz2FAQAAmzEEhRIwIGNnGl31h71eodZDV1q4M/7D++8yyUpWHOOuAnHCBlqxzDbqdKk8VlfPz9MV42ICsuIwEg+QGkEMZUjjb8nB9apM1ZCuwwxZ7aYCwBhsax1E0ZUrZOCFuWjoSI/RkReiSf0EbZbo2bAitCUH+zd/3I3ri0C2pw7AxyF9UcWrUUNSljvNNC/Gg4GQ/O8s2d65OVu67tyKxzNsGRWggCh2fv/fnb71vrGEuqYv~1','rh_user':'eddie.huang%40adventlabs.com|Eddie|P|','rh_locale':'en_us','rh_user_id':'55779225','rh_sso_session':'1','rh_jwt':'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICItNGVsY19WZE5fV3NPVVlmMkc0UXhyOEdjd0l4X0t0WFVDaXRhdExLbEx3In0.eyJleHAiOjE2NzI5NzQ4MDIsImlhdCI6MTY3Mjk3MzkwMiwiYXV0aF90aW1lIjoxNjcyOTczOTAxLCJqdGkiOiJkOTA4YzBmMi0zMWU5LTRiOGYtODk4NS1lMzIwOWUzZDJkNjkiLCJpc3MiOiJodHRwczovL3Nzby5yZWRoYXQuY29tL2F1dGgvcmVhbG1zL3JlZGhhdC1leHRlcm5hbCIsImF1ZCI6ImN1c3RvbWVyLXBvcnRhbCIsInN1YiI6ImY6NTI4ZDc2ZmYtZjcwOC00M2VkLThjZDUtZmUxNmY0ZmUwY2U2OmVkZGllLmh1YW5nQGFkdmVudGxhYnMuY29tIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiY3VzdG9tZXItcG9ydGFsIiwibm9uY2UiOiI3ZTY2YWY0Yi1lOTFkLTQ5ODEtYWU4Ny1hMDMxNWZhOGZkNzIiLCJzZXNzaW9uX3N0YXRlIjoiOTA2ZWU2NDktMDA3OC00MTZkLTllZDAtNDRhNDgyZDNmYTYyIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZHhwLWRjcC1wcm9kLmFwcHMuZXh0LXdhZi5zcG9rZS5wcm9kLnVzLXdlc3QtMi5hd3MucGFhcy5yZWRoYXQuY29tIiwiaHR0cHM6Ly9keHAtZG9jcy5leHQudXMtd2VzdC5hd3MucHJvZC5wYWFzLnJlZGhhdC5jb20iLCJodHRwczovL2R4cC1kb2NwLXByb2QuYXBwcy5leHQtd2FmLnNwb2tlLnByb2QudXMtd2VzdC0yLmF3cy5wYWFzLnJlZGhhdC5jb20iLCJodHRwczovL3Byb2QuZm9vLnJlZGhhdC5jb206MTMzNyIsImh0dHBzOi8vd3d3LnJlZGhhdC5jb20iLCJodHRwczovL2R4cC1qdXByLXByb2QuYXBwcy5leHQtd2FmLnNwb2tlLnByb2QudXMtd2VzdC0yLmF3cy5wYWFzLnJlZGhhdC5jb20iLCJodHRwczovL2FjY2Vzcy5yZWRoYXQuY29tIiwiaHR0cHM6Ly9keHAtZHhzcC1wcm9kLmFwcHMuZXh0LXdhZi5zcG9rZS5wcm9kLnVzLXdlc3QtMi5hd3MucGFhcy5yZWRoYXQuY29tIiwiaHR0cHM6Ly9keHAtZHBwLXByb2QuYXBwcy5leHQtd2FmLnNwb2tlLnByb2QudXMtd2VzdC0yLmF3cy5wYWFzLnJlZGhhdC5jb20iXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImF1dGhlbnRpY2F0ZWQiLCJpZHBfYXV0aGVudGljYXRlZCIsInBvcnRhbF9tYW5hZ2Vfc3Vic2NyaXB0aW9ucyIsIm9mZmxpbmVfYWNjZXNzIiwiYWRtaW46b3JnOmFsbCIsInVtYV9hdXRob3JpemF0aW9uIiwicG9ydGFsX21hbmFnZV9jYXNlcyIsInBvcnRhbF9zeXN0ZW1fbWFuYWdlbWVudCIsInBvcnRhbF9kb3dubG9hZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7InJoZC1kbSI6eyJyb2xlcyI6WyJyaHVzZXIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIExlZ2FjeV9JRFBfT3BlbklEIiwic2lkIjoiOTA2ZWU2NDktMDA3OC00MTZkLTllZDAtNDRhNDgyZDNmYTYyIiwiUkVESEFUX0xPR0lOIjoiZWRkaWUuaHVhbmdAYWR2ZW50bGFicy5jb20iLCJsYXN0TmFtZSI6Ikh1YW5nIiwiY291bnRyeSI6IlVTIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZWRkaWUuaHVhbmdAYWR2ZW50bGFicy5jb20iLCJmaXJzdE5hbWUiOiJFZGRpZSIsImFjY291bnRfaWQiOiIxNjYzNTMzNiIsInVzZXJfaWQiOiI1NTc3OTIyNSIsIm9yZ2FuaXphdGlvbl9pZCI6IjAwRG0wMDAwMDAwMTE2QyIsInNpdGVJZCI6InJlZGhhdCIsInNpdGVJRCI6InJlZGhhdCIsInBvcnRhbF9pZCI6IjA2MDYwMDAwMDAwRDBhZiIsImxhbmciOiJlbl91cyIsInJlZ2lvbiI6IlVTIiwiZW1haWwiOiJlZGRpZS5odWFuZ0BhZHZlbnRsYWJzLmNvbSIsIlJIQVRfTE9HSU4iOiJlZGRpZS5odWFuZ0BhZHZlbnRsYWJzLmNvbSIsInVzZXJuYW1lIjoiZWRkaWUuaHVhbmdAYWR2ZW50bGFicy5jb20ifQ.bnpmpwSG9dLSIM7BbQhJwMZ1m8A_vkG56n1Sl3UGTFzx_I_5DE9QF7rkVaYS5vob7xdb-QGd9GbIVDAFWHiBhAo1M4vEpyiySJppol1g5da4mOLhQ4-qUhoBuxoM3kNGrzC6Lbygm_IHUlv4DRe_mAU5bLe07-JiMY_ktVXDutOGag6k00eHIgAuyjqStbfa5jfdDYGCLg3Wbi7cPKaVvHmK9N0HRVYjL0sC20HjmcyVqOfXJ069Ab_hHhdMUiy6kP-7Vk-Y5oW5kivDp1vMKW4_OVpc5BKZSByPP3nlJ-vyKNaDQJ2UOoLnbPQSdjGuYOFnIIVV9II0jENuOFLylNTxd5o1hM5GG9oMXIOAMXrZne49rk1nkMYEuPPHmzgPAwbX7h7VfsSvEeUL76p0NHXaosmb059tBbacSzO37iP3TWKXM8dzwwgfMkGRw9xbMWnE-oMEZQYLT3XOfD3-mPbybpGyi3ciOq_nGk6kdVoEQD5jGxYf8pOHbQD6Xm-OIU6pxfaXhDt5kJQj2EVJRI1UAs91aOzD27PpVPu_ybTZTXrwh1tYZpX5l-9WCj0OQ5mUPDlQkr4Sal4uJV9yFSfBsJ-Ock905KR_55JQfqHoj_D5XswoVG5hiqOBfCcDWigKMQUyVwBrf_iI8LbZA8rXMCOLzGMvjwOjLBMIb4c','SSESSe82ddad2d63e5504fdf78cf492d69542':'H67NXte_NJKC7svqI5Q_rk_R3-qOHFNDsJuGeBNGpKQ','dtm_cpReg':'yes','_abck':'272951805842DFF1D23668F53AEF99CE~-1~YAAQFBQgF/FAHz2FAQAAWC8EhQnRlrYtIAH3KJo9DHi7TnZe3bYtoVp5mjPYthY40wUY/8q5S9ah2Ll/wyMIZaH0t0NNdGHxVpOVJi/b57rBy/rki5O9/mJHmPmV7eBSBIdJjhnhaYf1ozaUZkPIK+HJFRdd7mpiHI2mgQ2WL7NDD4TQ+OekiB1D7odSlNtX/8lF0xFAhuV38VreeLaHphhueD0jNJNxDMVrCO+HrDCOpb/cljGT8Qg23Aol6mT+GzAlhA9cuYk+u/Ce87MlWifGd3EhWVidYvLgfBAJVFfUSeq5KulXFvsvi/s+aU4zRBd+xkCe61sZlEbJ7rCbx9G5oWHLZaLzntmP1jn+QKgPr67mSh6eLhsSa2Ct~-1~-1~-1','bm_sz':'14D80D7CB24F00B14DDFC1A6035D7A1D~YAAQFBQgF/NAHz2FAQAAWC8EhRLOU+4fAAX2jUsrPSjd3P42/OZBDUK4FjUWLM5MvBTUueOlv8t2/5BF4k3yKBVSZFhLMBPSk599rae1i+nLwz0cDBELkf1+6xVuNSwfN+iNf/fHxubVL9yjKFMRnwd+Db47CjS01k6Iue1F8msTpGtVLv4DpH+wpLlO2Bvl3Nru+e66g/GUdP3L+ljl0Rz1eKa6uzwH/HAlAgpIN8UDVu32ga0QI6JMB1iG8H9a0IYYYx9DkHJd7BPBVy5IyrwuEnFrOSnQnDLfb/qx9bbmi6w=~3158853~4407857'}
    start_urls=['https://access.redhat.com/discussions']
    def parse(self, response):
        Data=response.xpath('//div[@id="doc"]//li//h3/a/@href').getall()
        for row in Data:
            url='https://access.redhat.com'+row
            Referer='https://access.redhat.com/webassets/avalon/j/includes/session/scribe/?redirectTo='+quote(url)
            self.headers['Referer']=Referer
            yield scrapy.Request(url,callback=self.parse_content,headers=self.headers,cookies=self.cookies)
        next_page=response.xpath('//li[@class="pager-next"]/a/@href').get()
        if next_page:
            url='https://access.redhat.com'+next_page
            yield scrapy.Request(url,callback=self.parse)
    def parse_content(self,response):
        item={}
        item['Discussion URL']=response.url
        item['Discussion Title']=str(response.xpath('//h1[@class="title"]/text()').get()).strip()
        item['Started Date']=str(response.xpath('//div[@class="user-info"]//time[@class="moment_date"]/@datetime').get()).split('T')[0]
        item['Latest Response Date']=str(response.xpath('//div[@class="header-meta"]//time[@class="moment_date"]/@datetime').get()).split('T')[0]
        item['Author URL']='https://access.redhat.com'+response.xpath('//div[@class="discussion-author"]//a/@href').get()
        item['Responder URLs']=''
        item['# of Responses']=str(response.xpath('//a[contains(@href,"#comment-now")]//span[@class="action-nav-text"]//text()').get()).strip()
        item['# of Thumbs Up']=str(response.xpath('//a[@rh-action-sheet-toggler="helpfulActionSheet"]//span[@class="action-nav-text"]//text()').get()).strip()
        URLs=response.xpath('//div[@id="comments"]/div[contains(@id,"comment-wrapper-")]')
        Responder_URLs=[]
        for URL in URLs:
            url='https://access.redhat.com'+URL.xpath('.//a[contains(@class,"thumbnail")]/@href').get()
            if not url in Responder_URLs:
                Responder_URLs.append(url)
        next_page=response.xpath('//li[@class="pager-next"]/a/@href').get()
        if next_page:
            url='https://access.redhat.com'+next_page
            Referer='https://access.redhat.com/webassets/avalon/j/includes/session/scribe/?redirectTo='+quote(url)
            self.headers['Referer']=Referer
            yield scrapy.Request(url,callback=self.parse_next,headers=self.headers,cookies=self.cookies,meta={'item':item,'Responder_URLs':Responder_URLs},dont_filter=True)
        else:
            item['Responder URLs']=', '.join(Responder_URLs)
            yield(item)
    def parse_next(self,response):
        item=response.meta['item']
        Responder_URLs=response.meta['Responder_URLs']
        URLs=response.xpath('//div[@id="comments"]/div[contains(@id,"comment-wrapper-")]')
        for URL in URLs:
            url='https://access.redhat.com'+URL.xpath('.//a[contains(@class,"thumbnail")]/@href').get()
            if not url in Responder_URLs:
                Responder_URLs.append(url)
        next_page=response.xpath('//li[@class="pager-next"]/a/@href').get()
        if next_page:
            url='https://access.redhat.com'+next_page
            Referer='https://access.redhat.com/webassets/avalon/j/includes/session/scribe/?redirectTo='+quote(url)
            self.headers['Referer']=Referer
            yield scrapy.Request(url,callback=self.parse_next,headers=self.headers,cookies=self.cookies,meta={'item':item,'Responder_URLs':Responder_URLs},dont_filter=True)
        else:
            item['Responder URLs']=', '.join(Responder_URLs)
            yield(item)

