# -*- coding: utf-8 -*-
import requests
from jingdong.items import JingdongItem
from lxml import etree
import scrapy
import re
import json
from scrapy import Request


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']
    page=1
    url = "https://search.jd.com/Search?keyword=笔记本&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=笔记本&page=%d&click=0"
    #next_url = "https://search.jd.com/Search?keyword=笔记本&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=笔记本&page=%d&scrolling=y&show_items=%s"
    #headers = {'referer': "https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC&page=1&s=1&click=0"}
    """
    if self.page < 200 and self.page > 1:
        if self.page % 2 !=0:
             self.page +=1
             yield scrapy.Request(self.next_url % (self.page, ','.join(ids)),callback=self.parsefirstPage, headers=headers)
        
        else:
            self.page +=1
            yield scrapy.Request(self.url % (self.page), callback=self.parsefirstPage)
    """

    def start_requests(self):
        yield scrapy.Request(self.url % (self.page), callback=self.parsefirstPage)

    def parsefirstPage(self, response):
        infos = response.xpath('//li[@class="gl-item"]/div/div[@class="p-img"]/a')
        for info in infos:
            item = JingdongItem()
            url = info.xpath('@href').extract()
            goods_link = response.urljoin(url[0])
            item['link'] = goods_link  # 商品链接
            for link in url:
                url = response.urljoin(link)
                yield Request(url, meta={'meta': item}, callback=self.parsegoods)
            if self.page<200:    
                self.page +=2 #翻页
                yield scrapy.Request(self.url % (self.page), callback=self.parsefirstPage)
    
                




    def parsegoods(self, response):
        item = response.meta['meta']
        id= response.xpath('//a[@class="compare J-compare J_contrast"]/@data-sku').extract()[0] # 商品id
        #ids = []
        #ids.append(''.join(id))
        item['goods_id'] = id
        item['goods_name'] = response.xpath('//div[@class="sku-name"]/text()').extract()[0].strip() # 名称
        shop_name= response.xpath('//div[@class="name"]/a/text()').extract()[0] # 商店名称
        print("----------------------",shop_name,"----------------------")
        item['shop_name']=shop_name
        
        
      

        price_url = "https://p.3.cn/prices/mgets?callback=jQuery7726740&skuIds=" + str(id)
        price = requests.get(price_url).text
        money = re.findall(r'\"p\"\:\"(.*?)\"}]\)', price)
        item['price'] = money[0]

      
        comments = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(id)
        yield scrapy.Request(comments, meta={'item': item}, callback=self.parse_getCommentnum)
   
       

    def parse_getCommentnum(self, response):
        item = response.meta['item']
        date = json.loads(response.text)  #解析json
        item['comments']= date['CommentsCount'][0]['CommentCountStr']   # 评论数量
        

    
    
    
            

        
        # for field in item.fields:
        #     try:
        #         item[field] = eval(field)
        #     except:
        #         print('Field is not defined', field)
        yield item
