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
        for course in response.css('li.public'):
            item=ShiyanlougithubItem()
            item["name"]=course.css("h3 a::text").re_first('[^\S]*(\S+)[^\S]*')
            item["update_time"]=course.css("div.f6.text-gray.mt-2 relative-time::attr(datetime)").extract_first()
            
            url=response.urljoin(course.css("a::attr(href)").extract_first())
            print('#'*20+url)
            #print(item)
            request=scrapy.Request(url,callback=self.parse_pro,dont_filter=True)
            request.meta['item']=item
            yield request
    def parse_pro(self,response):
        item=response.meta['item']
        print(item)
        for num in response.css('ul.numbers-summary li'):
            type_text=num.xpath('.//a/text()').re_first('\n\s*(.*)\n')
            number_text=num.xpath('.//span[@class="num text-emphasized"]/text()').re_first('\n\s*(.*)\n')
#            print("^^^^^^^^"+type_text)
#            print("--------"+number_text)
            if type_text and number_text:
                number_text=number_text.replace(',','')
                if type_text in ('commit','commits'):
                    item['commits']=int(number_text)
                elif type_text in ('branch','branches'):
                    item['branches']=int(number_text)
                elif type_text in ('release','releases'):
                    item['releases']=int(number_text)
        yield item
