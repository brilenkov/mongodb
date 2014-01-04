#! /usr/bin/python
#! -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
import re
from mongodb.items import MongodbItem, MongodbItemCategory
from datetime import date, timedelta

from scrapy.http import Response, Request

class MongodbSpider(CrawlSpider):
    name = "sinful"
    
    allowed_domains = ["http://www.sinful.dk", "http://www.sinful.dk", "www.www.sinful.dk", "www.sinful.dk"]
    start_urls = ['http://www.sinful.dk/']
    
    #hxs.select('//div[@class="homepage-left-nav"]/ul/li/a').extract()
    #hxs.select('//div[@class="homepage-left-nav"]/ul/li/ul/li/a').extract()
    #hxs.select('//div[@class="pname-div"]/a').extract()
    #hxs.select('//div[@class="toolbar-bottom"]/div/div/div/ol/li/a').extract()
    #hxs.select('//div[@class="cats cboth mt4"]/span/a').extract()
    rules = (
        #Rule(SgmlLinkExtractor(restrict_xpaths=('/div[@class="homepage-left-nav"]/ul/li/a','//div[@class="homepage-left-nav"]/ul/li/ul/li/a','//div[@class="toolbar-bottom"]/div/div/div/ol/li/a',)),),
        Rule(SgmlLinkExtractor(restrict_xpaths=('/div[@class="homepage-left-nav"]/ul/li/a','//div[@class="homepage-left-nav"]/ul/li/ul/li/a','//div[@class="toolbar-bottom"]/div/div/div/ol/li/a','//div[@class="cats cboth mt4"]/span/a',)),callback='parse_category'),
        #Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pname-div"]/a',)),callback='parse_item'),
    )
    
    def parse_category(self, response):
        yield Request(response.url+'?limit=all',callback=self.parse_all_in_category) 
        
    def parse_all_in_category(self, response):
        itemcat = MongodbItemCategory()
        hxs = HtmlXPathSelector(response)
        try:
            #breadcrumbs = hxs.select('//div[@class="breadcrumbs f10"]/ul/li/a/text()').extract()
            breadcrumbs = hxs.select('//div[@class="breadcrumbs f10"]/ul/li').select('./*/text()').extract()
        except:
            breadcrumbs = []
            
        itemcat['sourceid'] = breadcrumbs[-1]
        
        itemcat['urls'] = response.url
           
        itemcat['createddatetime'] = str(date.today())
        
        itemcat['name'] = breadcrumbs[-1]
        
        itemcat['source'] = "sinful"
        
        try:
            #itemcat['description'] = re.sub('\s+', ' ', re.sub('<[^<>]+>|&[a-z]+;', ' ', hxs.select('//div[@class="category-description std f12"]')[0].extract().replace('<br>','\n')).strip())
            itemcat['description'] = re.sub('\s+', ' ', re.sub('<[^<>]+>|&[a-z]+;', ' ', hxs.select('//div[@class="col-main"]')[0].extract().replace('<br>','\n')).strip())
        except:
            itemcat['description'] = None
        
        try:
            itemcat['productlinks'] = hxs.select('//div[@class="pname-div"]/a/@href').extract()
        except:
            itemcat['productlinks'] = None
        
        try:
            itemcat['imagelinks'] = hxs.select('//div[contains(@onmouseover,"showQuickInfo")]/a/img/@src').extract()
        except:
            itemcat['imagelinks'] = None
            
        #for u in itemcat['productlinks']:
        #reqs = []
        for product_url in hxs.select('//div[@class="pname-div"]/a/@href').extract():
            yield Request(product_url,callback=self.parse_item) 
            #reqs.append(Request(product_url,callback=self.parse_item))
        
        #return itemcat, reqs
        if 'http://www.sinful.dk/brands' not in response.url:
            yield itemcat
        
    def parse_item(self, response):
        item = MongodbItem()
        hxs = HtmlXPathSelector(response)
        
        try:
            breadcrumbs = hxs.select('//div[@class="breadcrumbs f10"]/ul/li/a/text()').extract()
        except:
            breadcrumbs = []
            
        item['sourceid'] = breadcrumbs[-1]
        
        item['source'] = "sinful"
        
        #item['raw_document'] = response.body
        
        item['urls'] = response.url
        
        item['createddatetime'] = str(date.today())
        
        try:
            item['name'] = hxs.select('//h1/span[@itemprop="name"]/text()').extract()[0]
        except:
            item['name'] = None
            
        try:
            #item['onstock'] = u'P\xc5 LAGER' in hxs.select('//p[@class="availability in-stock"]/span/text()').extract()
            item['onstock'] = u'P\xc5 LAGER' in hxs.select('//div[@class="pname-avail fleft"]/div/p[@class="availability in-stock"]/span/text()').extract()
            #item['onstock'] = u'IKKE P\xc5 LAGER' in hxs.select('//p[@class="availability out-of-stock f12 fbold"]/span/text()').extract()
        except:
            item['onstock'] = None

        try:
            item['mainimage'] = hxs.select('//img[@class="pimg"]/@src').extract()[0]
        except:
            item['mainimage'] = None
            
        try:
            item['otherimages'] = hxs.select('//a[@class="other-images-small"]/@href').extract()
        except:
            item['otherimages'] = None
            
        try:
            item['shortdescription'] = re.sub('\s+', ' ', re.sub('<[^<>]+>|&[a-z]+;', ' ', hxs.select('//div[@class="short-description"]')[0].extract().replace('<br>','\n')).strip())
        except:
            item['shortdescription'] = None
            
        try:
            item['description'] = re.sub('\s+', ' ', re.sub('<[^<>]+>|&[a-z]+;', ' ', hxs.select('//span[@itemprop="description"]')[0].extract().replace('<br>','\n')).strip())
        except:
            item['description'] = None
            
        try:
            item['details'] = re.sub('\s+', ' ', re.sub('<[^<>]+>|&[a-z]+;', ' ', hxs.select('//div[@id="descdiv3"]')[0].extract().replace('<br>','\n')).strip())
        except:
            item['details'] = None
            
        try:
            item['relatedlinks'] = None
        except:
            item['relatedlinks'] = None
        try:
            item['upselllinks'] = None
        except:
            item['upselllinks'] = None
            
        try:
            item['price'] = float(hxs.select('//p[@class="old-price pbox-oprice"]/span/text()').re('[\d\.\,]+')[0].replace('.','').replace(',','.'))
        except:
            item['price'] = None
        if not item['price']:
            try:
                item['price'] = float(hxs.select('//span[@class="regular-price fbold"]/span/text()').re('[\d\.\,]+')[0].replace('.','').replace(',','.'))
            except:
                item['price'] = None            
        
        try:
            item['specialprice'] = float(hxs.select('//p[@class="special-price pricebox fbold"]/span/text()').re('[\d\.\,]+')[0].replace('.','').replace(',','.'))
        except:
            item['specialprice'] = None
            
        try:
            #item['currency'] = hxs.select('//p[@class="special-price pricebox fbold"]/span[@class="price"]/text()').re('\w+')[0]
            item['currency'] = 'DKK'
        except:
            item['currency'] = None
            
        return item
