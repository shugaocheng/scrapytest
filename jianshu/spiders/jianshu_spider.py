import scrapy
from scrapy.http import Request
from jianshu.items import JianshuItem
from scrapy.selector import Selector

class PostSpider(scrapy.spiders.Spider):
    name = 'post'
    # 为每个url创建一个scrapy.http.request,并将爬虫的parse方法指定为回调函数
    # 这些request被调度并执行,之后通过parse方法返回scrapy.http.response对象,并反馈给爬虫
    # allowed_domains = ["www.jianshu.com"]
    start_urls = ['http://www.jianshu.com']
    url = 'http://www.jianshu.com'
    remenurl = 'http://www.jianshu.com/trending/weekly?'

    def parse(self,response):
        selector = Selector(response)
        articles = selector.xpath('//ul[@class="note-list"]/li')
        for article in articles:
            url = article.xpath('div/div/a/@href').extract()
            likeNum = article.xpath('div/div/span[2]/text()').extract()
            item = JianshuItem()
            posturl = "http://www.jianshu.com"+url[2]
            item['url'] = "http://www.jianshu.com"+url[2]
            if likeNum == []:
                item['likeNum'] = 0
            else:
                item['likeNum'] = int(likeNum[0].split(' ')[-1])

            # yield item
            request = Request(posturl,callback=self.parse_donate)
            request.meta['item'] = item
            yield request

        # next_link = selector.xpath('//a[@class="load-more"]/@href').extract()[0]
        # for pages in range(5):
            # remen = self.remenurl + 'page'+'='+ str(pages)
            # yield Request(remen,callback=self.parse)
        # if next_link:
            # next_link = self.url + str(next_link)
            # yield Request(next_link,callback=self.parse)
        # for pages in range(1,5):
        #     next_link = self.url + 'page' + '=' + str(pages)
        #     yield Request(next_link,callback=self.parse)
        # next_link = selector.xpath('//a[@class="load-more"]/@href').extract()[0]
        # if next_link:
        #     next_link = self.url + str(next_link)
        #     yield Request(next_link,callback=self.parse)

    def parse_donate(self,response):
        # selector = Selector(response)
        donate = response.xpath('//h1[@class="title"]/text()').extract()
        item = response.meta['item']
        if len(str(donate)) == 0:
            item['quote'] = ""
        else:
            item['quote'] =str(donate[0])
        return item