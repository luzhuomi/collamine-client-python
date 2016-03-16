# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
if scrapy.version_info[0:2] < (1,1):
        from scrapy.contrib.djangoitem import DjangoItem
else:
        from scrapy_djangoitem import DjangoItem # sudo easy_install scrapy_djangoitem
from scrapy.item import Field

from crawler.models import  HTML

'''
class ScrapybotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
'''

class ScrapybotItem(DjangoItem):
	django_model = HTML
