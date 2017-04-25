# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv


class Lesson01Pipeline(object):
    def __init__(self):
        fieldnames = ["title", "url", "date", "desc"]
        self.csvfile = open('data.csv', 'wb')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        # 处理数据通常是存储到数据库，如mysql，mongodb, csv等
        # 这里实现存储到csv格式的功能
        item['title'] = item['title'].encode("utf-8")
        item['desc'] = item['desc'].encode("utf-8")
        self.writer.writerow(item)
        self.csvfile.flush()  # 注意：需要flush才会写到文件
        
        return item

    def __del__(self):
        self.csvfile.close()
