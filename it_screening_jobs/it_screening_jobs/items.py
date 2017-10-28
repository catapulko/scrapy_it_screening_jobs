# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class IndeedItem(Item):
    search_date_time = Field()
    search_term = Field()
    website = Field()
    country = Field()
    jobs_number = Field()