import scrapy
from scrapy_project.items import QuoteItem, AuthorItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            quote_item = QuoteItem()
            quote_item['tags'] = quote.xpath("div[@class='tags']/a/text()").getall()
            quote_item['author'] = quote.xpath("span/small[@class='author']/text()").get()
            quote_item['quote'] = quote.xpath("span[@class='text']/text()").get()

            author_url = quote.xpath("span/a/@href").get()
            author_request = response.follow(author_url, self.parse_author)
            author_request.meta['quote_item'] = quote_item
            yield author_request

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        author_item = AuthorItem()
        author_item['fullname'] = response.xpath("//h3[@class='author-title']/text()").get().strip()
        author_item['born_date'] = response.xpath("//span[@class='author-born-date']/text()").get().strip()
        author_item['born_location'] = response.xpath("//span[@class='author-born-location']/text()").get().strip()
        author_item['description'] = response.xpath("//div[@class='author-description']/text()").get().strip()

        yield quote_item
        yield author_item