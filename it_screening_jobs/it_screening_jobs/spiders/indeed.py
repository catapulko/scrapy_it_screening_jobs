# -*- coding: utf-8 -*-
import logging
import scrapy
from time import gmtime, strftime
from it_screening_jobs.items import IndeedItem

class IndeedSpider(scrapy.Spider):

    name = "indeed"
    date_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def start_requests(self):
        base_url = 'http://' + self.website + '/jobs?q='
        f = open('it_screening_jobs/search_items', 'r')
        search_term = f.readline().rstrip()
        while (search_term <> '') and (not search_term.startswith('#')):
            yield scrapy.Request(base_url+search_term, callback=self.parse_indeed_response, meta={'search_term':search_term})
            search_term = f.readline().rstrip()

    def parse_indeed_response(self, response):
        i = IndeedItem()
        i['search_term'] = response.meta.get('search_term')
        if (len(response.selector.xpath('//*[@id="searchCount"]')) == 0):
            i['jobs_number'] = 0
        else:
            i['jobs_number'] = int(response.selector.xpath('//*[@id="searchCount"]').extract()[0].replace(' offerte di lavoro','').split().pop().replace('</div>','').replace(',','').replace('.',''))
        i['search_date_time'] = self.date_time
        i['website'] = self.website
        i['country'] = self.country
        logging.info(i)
        yield i

    def __init__(self, indeed_website=None, country=None, *args, **kwargs):
        super(IndeedSpider,self).__init__(*args, **kwargs)
        self.country = country
        self.website = indeed_website
        self.allowed_domains = [ indeed_website ]