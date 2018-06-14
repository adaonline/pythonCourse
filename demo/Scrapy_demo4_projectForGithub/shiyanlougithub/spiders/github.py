# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['https://github.com/shiyanlou?tab=repositories']
    start_urls = ['http://https://github.com/shiyanlou?tab=repositories/']

    @property
    def start_urls(self):
        url_tmp='https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmp.format(i) for i in range(1,4))
    def parse(self, response):
        for course in response.css('li[class="col-12 d-block width-full py-4 border-bottom public source"]'):
            item=ShiyanlougithubItem({
                "name":course.css("h3 a::text").re_first('[^\S]*(\S+)[^\S]*'),
                "update_time":course.css("div.f6.text-gray.mt-2 relative-time::attr(datetime)").extract_first()
            })
            print(item)
            yield item
