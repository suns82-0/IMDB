# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from IMDB.items import ImdbItem
from scrapy.shell import inspect_response
from scrapy import shell
from bs4 import BeautifulSoup

class IMDBSpider(CrawlSpider):
    name = "IMDB"
    allowed_domains = ["imdb.com"]
    start_urls = ['https://www.imdb.com/feature/genre']

    rules={
        Rule(LinkExtractor(allow='/search/',restrict_xpaths="//*[@id='main']/div[6]/span/div"), follow=True),
        Rule(LinkExtractor(allow="\&start=\d+\&tref_=",restrict_xpaths="//*[@id='main']/div/div[4]"),follow=True),
        Rule(LinkExtractor(allow="/title/",restrict_xpaths="//*[@id='main']/div"),callback='parse_item')
    }
    def parse_item(self,response):
        '''
        this part for debug
        '''

        from scrapy.shell import inspect_response
        inspect_response(response, self)


        item=ImdbItem()
        soup = BeautifulSoup(response.text)


        try:
            genre = list(map(lambda x:x.text,soup.find("div",{"class":"subtext"}).findAll("a")))
        except:
            genre = None
        item["genre"] = genre
        #
        try:
            name = soup.find("div",{"class":"title_wrapper"}).find("h1").contents[0]
        except:
            name = None
        item['name'] = name
        #
        try:
            year = soup.find("div",{"class":"title_wrapper"}).find("h1").span.text.strip("(").strip(")")
        except:
            year = None
        item['year'] = year
        #
        try:
            director = list(map(lambda x:x.text,soup.find("div",{"class":"credit_summary_item"}).findAll("a")))
        except:
            director = None
        item["director"] = director
        #
        try:
            score = int(soup.find("div",{"class":"ratingValue"}).contents[1].text)
        except:
            score = None
        item["score"] = score
        #
        try:
            stars = list(map(lambda x:x.text,soup.findAll("div",{"class":"credit_summary_item"})[-1].findAll("a")))
        except:
            stars = None
        item["stars"] = stars


        yield item

