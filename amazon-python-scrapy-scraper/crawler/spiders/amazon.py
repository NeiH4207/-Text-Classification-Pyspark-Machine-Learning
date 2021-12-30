# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import json
queries = ['soft sweaters', 'tshirt for men', 'bottle water', 'iphone', 'laptop', 'smartphone', 'pen', 'milk', 'food', 'led', 
           'television', 'asus', 'wireless earbuds', 'samsung', 'apple', 'food', 'toys', 'clock', 'tree', 'rocket', 'guitar', 'piano']    ##Enter keywords here ['keyword1', 'keyword2', 'etc']
API = 'ea6a51e37db608ee5ca4c8a99874d025'                        ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup


def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class AmazonSpider(scrapy.Spider):
    name = "amazon"

    def start_requests(self):
        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract()
            for _asin in asin:
                product_url = f"https://www.amazon.com/dp/{_asin}"
                yield scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})
            
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.com",next_page)
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)
        else:
            # Inspired by your browsing history, Amazon has suggested that you visit the following pages:
            url = 'https://www.amazon.com/gp/yourstore/home/ref=nav_yourstore_ya_ya'
            # click on the first suggested link
            url = urljoin
            
    def contains_not_ascii(self, s):
        return any(ord(c) >= 128 for c in s)
    

    def parse_product_page(self, response):
        #yield response
        reviews = response.css('.review-title').extract()       
        sentiments = response.css('.review-rating').extract()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        image = re.search('"large":"(.*?)"',response.text).groups()[0]
        asin = response.meta['asin']
        if not price:
            price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
                    response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first()
        size = 'S'
        color = 'black'
        temp = response.xpath('//*[@id="twister"]')
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
            di = json.loads(json_acceptable)
            size = di.get('size_name', [])
            color = di.get('color_name', [])
        
        #Give the extracted content row wise
        for item in zip(reviews, sentiments):
            #create a dictionary to store the scraped info
            review = BeautifulSoup(item[0]).text.replace('\n', '')
            rate = int(float(BeautifulSoup(item[1]).text.replace(' out of 5 stars', '')))

            # if self.contains_not_ascii(review):
            #     continue
            yield {
                'asin': asin, 
                'title': title, 
                'image': image, 
                'review': review,
                'sentiment' : 'positive' if rate > 3 else 'negative',
                'price' : price,
                'size' : size,
                'color' : color,
                'asin' : asin
            }
        



