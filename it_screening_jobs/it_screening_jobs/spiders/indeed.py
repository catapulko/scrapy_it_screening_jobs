# -*- coding: utf-8 -*-
import logging
import scrapy
from time import gmtime, strftime
from it_screening_jobs.items import IndeedItem

class IndeedSpider(scrapy.Spider):

    name = "indeed"
    date_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def start_requests(self):
        f_websites = open('it_screening_jobs/indeed_websites','r')
        website_country = f_websites.readline().rstrip().split(',')
        logging.log(logging.DEBUG,website_country)
        while (len(website_country) > 0) and (not website_country[0].startswith('#')):
            website,country = website_country
            base_url = 'http://' + website + '/jobs?q='
            f_search_terms = open('it_screening_jobs/search_items', 'r')
            search_term = f_search_terms.readline().rstrip()
            while (search_term <> '') and (not search_term.startswith('#')):
                yield scrapy.Request(base_url+search_term, callback=self.parse_indeed_response, meta={'search_term':search_term, 'website': website, 'country': country})
                search_term = f_search_terms.readline().rstrip()
            f_search_terms.close()
            website_country = f_websites.readline().rstrip().split(',')
        f_websites.close()

    def parse_indeed_response(self, response):
        i = IndeedItem()
        i['search_term'] = response.meta.get('search_term')
        if (len(response.selector.xpath('//*[@id="searchCount"]')) == 0):
            i['jobs_number'] = 0
        else:
            i['jobs_number'] = int(response.selector.xpath('//*[@id="searchCount"]').extract()[0].replace(' offerte di lavoro','').split().pop().replace('</div>','').replace(',','').replace('.',''))
        i['search_date_time'] = self.date_time
        i['website'] = response.meta.get('website')
        i['country'] = response.meta.get('country')
        yield i