# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()  # 商品ID
    link = scrapy.Field()  # 商品链接
    goods_name = scrapy.Field()  # 商品名字
    shop_name = scrapy.Field()  # 店家名字
    price = scrapy.Field()  # 电脑价格
    comments = scrapy.Field()  # 评论数量
    
