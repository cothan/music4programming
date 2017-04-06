# -*- coding: utf-8 -*-
#from scrapy.http.request import Request
import scrapy


class Songs(scrapy.Item):
	"""docstring for Songs"""
	#def __init__(self, arg):
		#super(Songs, self).__init__()
	title = scrapy.Field()
	file_urls = scrapy.Field()
	files = scrapy.Field()
	

class MusicSpider(scrapy.Spider):1
	name = "music"
	allowed_domains = ["musicforprogramming.net"]
	start_urls = ['http://musicforprogramming.net/']

	count = 0 

	def parse(self, response):
		# The name alone contains u'musicForProgramming("47: Abe Mangger");'
		# So we strip out to get the name of the song only
		title = response.css('title::text').extract_first()[len('musicForProgramming("'):-3]
		src = response.xpath('//audio[@id="player"]/@src').extract_first() 

		self.count += 1
		if self.count >= 46:
			return

		yield Songs(title=title, file_urls=[src])

		next_url = response.xpath('//div[@id="episodes"]/a/@href').extract()[self.count]
		
		if next_url is not None:
			yield scrapy.Request(response.urljoin('http://musicforprogramming.net/' + next_url))
			
	def get_media_requests(self, item, info):
    	url = item['file_urls']
        meta = {'filename': item['title']}
        yield scrapy.Request(url, meta=meta)

		
