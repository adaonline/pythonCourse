# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis
import json
from scrapy.exceptions import DropItem

class DoubanMoviePipeline(object):
    def process_item(self, item, spider):
        item['summary']=re.sub('\s+',' ',item['summary'])
        if not float(item['score'])>8.0:
            raise DropItem('less score')
        self.redis.lpush('douban_movie:items',json.dumps(dict(item)))
        return item
    def open_spider(self,spider):
        self.redis=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
