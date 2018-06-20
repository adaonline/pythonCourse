#突破反爬虫策略爬取豆瓣电影
Scrapy 文档中有介绍到几个策略：

1. 切换 UserAgent
2. 禁用 Cookies （详见 COOKIES_ENABLED  https://doc.scrapy.org/en/master/topics/downloader-middleware.html），因为有些网站会根据用户 cookies 确定用户行为
3. 设置延迟，避免对网站短时间大量请求(详见 DOWNLOAD_DELAY https://doc.scrapy.org/en/master/topics/settings.html)
4. 使用 IP 代理
5. 构建分布式下载系统



策略 1情况需要动态的设置每个请求的 UserAgent，这就需要使用到 Scrapy 的中间件（Middlewares）。scrapy.downloadermiddlewares 中提供了很多中间件可以改变 Scrapy 的请求和响应，这次是要重写一个 UserAgentMiddleware。一定要在sessing里配置


1. 如果启用了新的 Middleware，需要在 settings.py 中把老的 Middleware 对应的数值设为 None
2. DOWNLOAD_DELAY 参数可以到 setting.py 配置文件中设置


CrawlSpider 类可以参考文档
COOKIES_ENABLED 参数需要了解

不要忘了https的s，少打了s，只会查找第一个，暂时不明白为什么