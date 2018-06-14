# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from shiyanlougithub.model import Repository,engine
from datetime import datetime
class ShiyanlougithubPipeline(object):
    def process_item(self, item, spider):
        UTC_FOR="%Y-%m-%dT%H:%M:%SZ"
        item['update_time']=datetime.strptime(item['update_time'],UTC_FOR).date()
        self.session.add(Repository(**item))
        return item
    def open_spider(self,spider):
        Session=sessionmaker(bind=engine)
        self.session=Session()
    def close_spider(self,spider):
        self.session.commit()
        self.session.close()
