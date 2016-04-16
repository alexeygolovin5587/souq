import scrapy
from shopscraper.items import ShopscraperItem
import math

class SouqSpider(scrapy.Spider):
	name = "souq"
	allowed_domains = ["uae.souq.com"]
	basic_url = "http://uae.souq.com/ae-en"
	start_urls = ["http://uae.souq.com/ae-en/mobile-phone/apple/new/a-7-c/l/?sortby=sr"]

	page = 1
	page_size = 0

	product_urls = []

	def parse(self, response):
		if self.page == 1:
			total_product = self.check_value(response.xpath("//div[@class='listing-page-text']/text()"))
			total_product = int(total_product.encode('utf8').split('\xc2\xa0')[0])

			self.page_size = int(math.ceil(total_product / 15.0))
		
		if self.page <= self.page_size:
			products = response.xpath("//div[@class='placard']")
			for product in products:
				product_url = product.xpath(".//a[1]/@href")[0].extract().strip()
				if not product_url is None:
					self.product_urls.append(product_url)

			self.page += 1
			url = "http://uae.souq.com/ae-en/mobile-phone/apple/new/a-7-c/l/?sortby=sr&page=%d" % self.page
			request = scrapy.Request(url, callback=self.parse, dont_filter=True)
			yield request

		else:
			for url in self.product_urls:
				request = scrapy.Request(url, callback=self.parse_product_info, dont_filter=True)
				yield request
		

	# parse product info in a page which has 48 products.
	def parse_product_info(self, response):
		item = ShopscraperItem()

		item['name'] = self.check_value(response.xpath("//h1[@itemprop='name']/text()"))
		
		if item['name'] is None:
				item['name'] = self.check_value(response.xpath("//h6[@itemprop='name']/text()"))

		item['price'] = self.check_value(response.xpath("//h3[@class='price']/text()"))
		item['url'] = response.url

		yield item

	def check_value(self, value):
		if len(value) > 0:
			return value[0].extract().strip()
		else:
			return None
		

		
