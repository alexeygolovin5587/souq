# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ShopscraperPipeline(object):
		def open_spider(self, spider):
				self.file = open("data.csv", 'wb')

				temp = '"%s","%s","%s"\n' % ("name", "url", "price")
				self.file.write(temp)

				# save results in csv file.
		def close_spider(self, spider):
				self.file.close()
		

		def process_item(self, item, spider):

				temp = '"%s","%s","%s"\n' % (item["name"], item["url"], item["price"])

				#unicode encoding
				temp = temp.encode('utf8')
				#write line
				self.file.write(temp)

				return item
