# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import os


class ParseProjectPipeline(object):
    """
    Create table & Record scraped data
    """
    def process_item(self, item, spider):
        database = 'parsed_data.sqlite'
        db = create_engine('sqlite:///%s' % database, echo=False)
        metadata = MetaData(db)

        if not os.path.exists(database):
            table = Table('proxies', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('ip_address', String(15)),
                          Column('port', String(4)),
                          )
            table.create()
        else:
            table = Table('proxies', metadata, autoload=True)

        i = table.insert()
        i.execute(ip_address=item['ip_address'], port=item['port'])
