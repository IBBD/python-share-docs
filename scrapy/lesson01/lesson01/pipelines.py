# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Lesson01Pipeline(object):
    def process_item(self, item, spider):
        # 处理数据通常是存储到数据库，如mysql，mongodb, csv等
        # 为了演示方便，这里只是简单的print
        print("===> in pipeline")
        print(item)

        return item
