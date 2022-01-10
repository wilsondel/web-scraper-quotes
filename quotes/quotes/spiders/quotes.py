import scrapy


# quote = //span[@class="text"]/text()
# author = //small[@class="author"]/text()
# url = response.url
# next_page_link = //li[@class="next"]/a[contains(.,"Next")]/@href


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/']

    custom_settings = {
        'FEEDS':{
            'quotes.json':{
                'format':'json',
                'encoding': 'utf8',
                'indent':2,
            }
        },
        'USER_AGENT':"WADE",
        'ROBOTSTXT_OBEY':True,
        'CONCURRENT_REQUESTS':24,
    }

    def parse_quotes(self,response,**kwargs):
        complete_quote =[]
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']
        
        quotes.extend(response.xpath('//span[@class="text"]/text()').getall())
        authors.extend(response.xpath('//small[@class="author"]/text()').getall())

        next_page_link = response.xpath('//li[@class="next"]/a[contains(.,"Next")]/@href').get()

        if next_page_link:
            yield response.follow(next_page_link,callback=self.parse_quotes, cb_kwargs={'quotes': quotes,'authors': authors})
        else:
            complete_quote.extend(zip(quotes,authors))
            yield {
                'complete_quote': complete_quote
            }


    def parse(self,response):
        quotes = response.xpath('//span[@class="text"]/text()').getall()
        authors = response.xpath('//small[@class="author"]/text()').getall()

        # yield {
        #     'quotes': quotes,
        #     'authors': authors,
        # }

        next_page_link = response.xpath('//li[@class="next"]/a[contains(.,"Next")]/@href').get()
        if next_page_link:
            yield response.follow(next_page_link,callback=self.parse_quotes, cb_kwargs={'quotes': quotes,'authors': authors})


