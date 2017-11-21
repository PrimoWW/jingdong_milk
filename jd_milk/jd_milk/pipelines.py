# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy.exceptions import DropItem


class GoodsPipeline(object):
    def __init__(self):
        self.csvwriter = csv.writer(open('items.csv', 'w', newline=''), delimiter=',')

    def process_item(self, item, spider):
        if item['id']:
            row = [item['id'], item['name'], item['url'], item['price'], item['comment_count'], item['good_rate']]
            if self.csvwriter.writerow(row):
                print('write successfully!')
            return item
        else:
            return DropItem
