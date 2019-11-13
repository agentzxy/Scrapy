# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from lxml import etree
from douban.items import movieItem
#from douban.pipelines import DoubanPipeline


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250?start='+str(i*25) for i in range(10)]

    def parse(self, response):
        html=response.text
        html=etree.HTML(html)
        #pattern1=re.compile(r'<span class="title">[\u4e00-\u9fa5]+</span>')
        #pattern2=re.compile(r'<span class="inq">(.*?)</span>')
        #pattern3=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
        order=html.xpath('//ol[@class="grid_view"]/li/div/div/em')#序号
        title=html.xpath('//ol[@class="grid_view"]/li/div/div[@class="pic"]/a/img/@alt')#电影名
        inq=html.xpath('//ol[@class="grid_view"]/li/div/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span')#电影标签
        rating_num=html.xpath('//ol[@class="grid_view"]/li/div/div[@class="info"]/div[@class="bd"]/div/span[@class="rating_num"]')#电影评分
        image_url=html.xpath('//ol[@class="grid_view"]/li/div/div[@class="pic"]/a/img/@src')#剧照
        item=movieItem()
        #a=pattern1.findall(html)
        #for i in range(24):
            #a[i]=a[i][20:-7]
        item['nums']=order
        item['names']=title
        item['tags']=inq
        item['scores']=rating_num
        item['images']=image_url
        yield item
        #pipe=DoubanPipeline()
        #pipe.process_item(item,spider)
        
