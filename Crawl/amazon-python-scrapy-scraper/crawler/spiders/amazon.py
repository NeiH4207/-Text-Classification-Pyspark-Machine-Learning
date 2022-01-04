# -*- coding: utf-8 -*-
import json
import requests
import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import json
import requests
from json import dumps
from hdfs import InsecureClient
import subprocess
client = InsecureClient('hdfs://namenode:9000', user='hienvq')
queries = ['cake', 'tshirt', 'bottle']    ##Enter keywords here ['keyword1', 'keyword2', 'etc']
API = 'ea6a51e37db608ee5ca4c8a99874d025'                        ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup


def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    

    def start_requests(self):
        self.counter = 0
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

            
    def contains_not_ascii(self, s):
        return any(ord(c) >= 128 for c in s)
    
    def append_file_into_hdfs(self, file_in='temp.json', file_out='reviews.json'):
        cmd = """
        echo "hadoop fs -appendToFile /mnt/{file_in} /data/input/{file_out}" \
            | docker exec -i namenode bash""".format(file_in=file_in, file_out=file_out)
        subprocess.call(cmd, shell=True)

    def parse_product_page(self, response):
        #yield response
        reviews = response.css('.review-title').extract()       
        sentiments = response.css('.review-rating').extract()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        image = re.search('"large":"(.*?)"',response.text).groups()[0]
        asin = response.meta['asin']
        reviewers_id = response.xpath('//*[@id="cm_cr-review_list"]').extract()
        verified_buyers = response.xpath('//*[@id="cm_cr-review_list"]').extract()
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
        records = []
        #Give the extracted content row wise
        for item in zip(reviews, sentiments):
            #create a dictionary to store the scraped info
            review = BeautifulSoup(item[0]).text.replace('\n', '')
            rate = int(float(BeautifulSoup(item[1]).text.replace(' out of 5 stars', '')))
            reviewer_id = BeautifulSoup(reviewers_id[0]).text.replace('\n', '')
            verified = BeautifulSoup(verified_buyers[0]).text.replace('\n', '')
            # if self.contains_not_ascii(review):
            #     continue
            records.append( {
                'asin': asin, 
                'title': title, 
                'image': image, 
                'reviewText': review,
                'reviewerID': reviewer_id,
                'verified': verified,
                'overall' : rate,
                'price' : price,
                'size' : size,
                'color' : color,
                'asin' : asin
            })  
        data = '\n'.join(json.dumps(record) for record in records)
        # dump into temp file
        with open('../data/temp.json', 'w') as f:
            f.write(data)
        # append to hdfs
        self.append_file_into_hdfs('temp.json', 'reviews.json')



