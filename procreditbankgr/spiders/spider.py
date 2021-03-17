import scrapy

from scrapy.loader import ItemLoader

from ..items import ProcreditbankgrItem
from itemloaders.processors import TakeFirst


class ProcreditbankgrSpider(scrapy.Spider):
	name = 'procreditbankgr'
	start_urls = ['http://www.procreditbank.gr/el/nea/page/81']

	def parse(self, response):
		post_links = response.xpath('//div[@class="newsTitle newsTitleNoImage"]/h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date dateLong"]/text()').get()

		item = ItemLoader(item=ProcreditbankgrItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
