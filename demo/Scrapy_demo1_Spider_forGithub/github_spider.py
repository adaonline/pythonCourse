#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
class shiyanlouGithubSpider(scrapy.Spider):
    name='shiyanlou-github'
    @property
    def start_urls(self):
        url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,4))
    def parse(self,response):
        for course in response.css('li[class="col-12 d-block width-full py-4 border-bottom public source"]'):
            yield{
                "name":course.css("h3 a::text").re_first('[^\S]*(\S+)[^\S]*'),
                "update_time":course.css("div.f6.text-gray.mt-2 relative-time::attr(datetime)").extract()
            }

