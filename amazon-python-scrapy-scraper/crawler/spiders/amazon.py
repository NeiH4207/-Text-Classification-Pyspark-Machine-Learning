# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import json
queries = ['tshirt for men', 'bottle water', 'iphone', 'laptop']    ##Enter keywords here ['keyword1', 'keyword2', 'etc']
API = '68099f74faec69f2e5ca7b1806a657ff'                        ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup


def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def start_requests(self):
        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.com/dp/{asin}"
            yield scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})
            
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.com",next_page)
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)

    def contains_not_ascii(self, s):
        return any(ord(c) >= 128 for c in s)
    
    def parse_product_page(self, response):
        #yield response
        title = response.css('.review-title').extract()       
        reviews = response.css('.review-rating').extract()
       
        #Give the extracted content row wise
        for item in zip(title, reviews):
            #create a dictionary to store the scraped info
            rate = int(float(BeautifulSoup(item[1]).text.replace(' out of 5 stars', '')))
            review = BeautifulSoup(item[0]).text.replace('\n', '')
            if self.contains_not_ascii(review):
                continue
            yield {
                'review': review,
                'sentiment' : 'positive' if rate > 3 else 'negative'
            }
        



