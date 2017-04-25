# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

fieldnames = ["title", "url", "date", "desc"]
csvfile = open('data/scrapy.csv', 'w', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()


class Lesson01Pipeline(object):
    def process_item(self, item, spider):
        # 处理数据通常是存储到数据库，如mysql，mongodb, csv等
        # 这里实现存储到csv格式的功能
        global writer, csvfile
        writer.writerow(item)
        csvfile.flush()  # 注意：需要flush才会写到文件

        # 返回可以提供给其他的pipeline继续使用
        return item
