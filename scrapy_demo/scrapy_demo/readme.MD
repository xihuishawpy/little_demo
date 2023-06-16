1. 创建项目： scrapy startproject scrapy_demo
2. 在spiders目录下，新建test.py，里面主要是解析逻辑
3. 在items.py 中定义好需要爬取的item
4. test.py解析逻辑，主要是初始化类，需要爬取的start_urls，通过parse函数解析网页并返回item

在写parse逻辑的时候，可以在项目根目录下，通过 `scrapy shell "url"`的方式调试。
或者，在根目录下，cmd运行 `scrapy crawl A` (这里的A是定义的spider类的name值) 

https://scrapy-chs.readthedocs.io/zh_CN/latest/intro/tutorial.html

   