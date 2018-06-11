#爬虫爬取实验楼课程

生成scrapy项目
```
scrapy startproject shiyanlou
```
查看项目结构
```
tree shiyanlou
```
```
shiyanlou/
    scrapy.cfg            # 部署配置文件
    shiyanlou/            # 项目名称
        __init__.py
        items.py          # 项目 items 定义在这里
        pipelines.py      # 项目 pipelines 定义在这里
        settings.py       # 项目配置文件
        spiders/          # 所有爬虫写在这个目录下面
            __init__.py
```
快速初始化一个爬虫模版

```
scrapy genspider <name> <domain>
```
具体操作
```
cd /shiyanlou/shiyanlou  #跟项目结构对照一下看看
scrapy genspider courses shiyanlou.com
```
会在shiyanlou/shiyanlou/spiders下新建一个courses.py,其中的内容是
```python
# -*- coding: utf-8 -*-
import scrapy

class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['shiyanlou.com'] #allow_domains 可以是一个列表或字符串，包含这个爬虫可以爬取的域名
    start_urls = ['http://shiyanlou.com/']

    def parse(self, response):
        pass
```

然后我们可以自己编写start_urls方法，记得加上@property
```python
# -*- coding: utf-8 -*-
import scrapy


class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))
```

##item的使用
scrapy 推荐使用 Item 容器来存放爬取到的数据。
```python
import scrapy

class CourseItem(scrapy.Item):
      """定义 Item 非常简单，只需要继承 scrapy.Item 类，将每个要爬取
    的数据声明为 scrapy.Field()。下面的代码是我们每个课程要爬取的 4个数据。
    """
    name = scrapy.Field()
    description = scrapy.Field()
    type = scrapy.Field()
    students = scrapy.Field()
```

有了 CourseItem，就可以将 parse 方法的返回包装成它:
```python
# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import CourseItem


class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))

    def parse(self, response):
        for course in response.css('div.course-body'):
            # 将返回结果包装为 CourseItem 其它地方同上一节
            item = CourseItem({
                'name': course.css('div.course-name::text').extract_first(),
                'description': course.css('div.course-desc::text').extract_first(),
                'type': course.css('div.course-footer span.pull-right::text').extract_first(default='免费'),
                'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
            })
            yield item
```
scrapy 想象成一个产品线，spider 负责从网页上爬取数据，Item 相当于一个包装盒，对爬取的数据进行标准化包装，然后把他们扔到Pipeline 流水线中。
主要在 Pipeline 对 Item 进行这几项处理：

1. 验证爬取到的数据 (检查 item 是否有特定的 field)
2. 检查数据是否重复
3. 存储到数据库

首先建立好数据库
新建model.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


engine = create_engine('mysql+mysqldb://root@localhost:3306/shiyanlou?charset=utf8')
Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    description = Column(String(1024))
    type = Column(String(64), index=True)
    students = Column(Integer)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
```

然后就可以用pipeline 编写代码将 爬取到的每个 item 存入数据库中

```python
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, engine


class ShiyanlouPipeline(object):

    def process_item(self, item, spider):
        # 提取的学习人数是字符串，把它转换成 int
        item['students'] = int(item['students'])
        # 根据 item 创建 Course Model 对象并添加到 session
        # item 可以当成字典来用，所以也可以使用字典解构, 相当于
        # Course(
        #     name=item['name'],
        #     type=item['type'],
        #     ...,
        # )
        self.session.add(Course(**item))
        return item

    def open_spider(self, spider):
        """ 在爬虫被开启的时候，创建数据库 session
        """
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        """ 爬虫关闭后，提交 session 然后关闭 session
        """
        self.session.commit()
        self.session.close()

```
需要在settings.py中开启pipline
```python
# 默认是被注释的
ITEM_PIPELINES = {
    'shiyanlou.pipelines.ShiyanlouPipeline': 300
}
```
ITEM_PIPELINES 里面配置需要开启的 pipeline，它是一个字典，key 表示 pipeline 的位置，值是一个数字，表示的是当开启多个 pipeline 时它的执行顺序，值小的先执行，这个值通常设在 100~1000 之间。

在 scrapy 项目中启动爬虫使用 crawl 命令，需要指定爬虫的 name

```
cd /home/shiyanlou/Code/shiyanlou/shiyanlou
scrapy crawl courses
```

item过滤
```python
from scrapy.exceptions import DropItem

class ShiyanlouPipeline(object):

    def process_item(self, item, spider):
        item['students'] = int(item['students'])
        if item['students'] < 1000:
            # 对于不需要的 item，raise DropItem 异常
            raise DropItem('Course students less than 1000.')
        else:
            self.session.add(Course(**item))
```