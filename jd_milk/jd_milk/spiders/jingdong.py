# -*- coding: utf-8 -*-
from scrapy import  Spider, Request
from ..items import GoodsItem
import re

class JingdongSpider(Spider):
    name = 'jingdong'
    allowed_domains = ['www.jd.com']
    start_url = ['httP://www.jd.com']

    start_search_url = 'https://list.jd.com/list.html?cat=1320,5019,12215'

    price_url = 'https://p.3.cn/prices/mgets?callback=jQuery184837&ext=11000000&pin=&type=1&area=1_72_2799_0&skuIds=J_{id}&pdbp=0&pdtk=&pdpin=&pduid=1503079363&source=list_pc_front&_=1511188511767'

    comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds={id}&callback=jQuery1258667&_=1511249865078'

    def start_requests(self):
        yield Request(self.start_search_url, callback=self.parse)

    def parse(self, response):

        for number in range(1, 31):
            goods = GoodsItem()

            goods['id'] = response.xpath('//*[@id="plist"]/ul/li[{number}]/div/@data-sku'.format(number=number)).extract()[0]

            goods['name'] = response.xpath('//*[@id="plist"]/ul/li[{number}]/div/div[3]/a/em/text()'.format(number=number)).extract()[0].strip()

            goods['url'] = 'http:' + response.xpath('//*[@id="plist"]/ul/li[{number}]/div/div[1]/a/@href'.format(number=number)).extract()[0]

            yield Request(self.price_url.format(id=goods['id']), meta={'goods': goods}, callback=self.parse_price)

    def parse_price(self, response):
        goods = response.meta['goods']
        goods['price'] = re.search('\"p\":\"(.*?)\"', response.text).group(1)
        print(goods)
        yield Request(self.comment_url.format(id=goods['id']), meta={'goods': goods}, callback=self.parse_comment)

    def parse_comment(self, response):
        goods = response.meta['goods']
        goods['comment_count'] = re.search('\"CommentCount\":(.*?),', response.text).group(1)
        print(goods['comment_count'])
        goods['good_rate'] = re.search('\"GoodRate\":(.*?),', response.text).group(1)
        print(goods['good_rate'])
        return goods




