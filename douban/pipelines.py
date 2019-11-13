# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import douban.settings
import urllib3
import os
import Tools
from urllib import request
from douban.items import movieItem

class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class mysqlPipeline(object):
    def __init__(self,host,user,password,dbname):
        self.host=host
        self.user=user
        self.password=password
        self.dbname=dbname
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            dbname=crawler.settings.get('MYSQL_DBNAME'),
        )

    def open_spider(self,spider):
        self.db=pymysql.connect(self.host,self.user,self.password,self.dbname,charset='utf8')
        self.cursor=self.db.cursor()
    
    #item迭代返回对象
    def process_item(self,item,spider):
        for i in range(24):
            sql="INSERT INTO top250(NUM,NAME,TAG,SCORE) VALUES(%s,%s,%s,%s)"
            num=item['nums'][i].text
            name=item['names'][i]
            tag=item['tags'][i].text
            score=item['scores'][i].text
            s=(num,name,tag,score)
            self.cursor.execute(sql,s)
        self.db.commit()
        return item
        
    def close_spider(self, spider):
        self.db.close()

#将剧照存入文件
class imagePipeline(object):
    def process_item(self,item,spider):
        for i in range(24):
            splitPath=item['images'][i].split('.')
            fTail=splitPath.pop()
            fileName=item['names'][i]+"."+fTail
            filepath="D:/ddddd/"+fileName
            request.urlretrieve(item['images'][i],filepath)
