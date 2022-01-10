import scrapy 

# quote = //div[@class="standardText"]/p/text()
# author = //div[@class="standardText"]/p/em/text()

class PhrasesSpider(scrapy.Spider):
  name ="phrases"
  start_urls =[
    'https://www.inc.com/sujan-patel/101-inspiring-quotes-from-the-most-successful-people-in-history.html'
  ]

  custom_settings = {
      'FEEDS':{
          'phrases.json':{
              'format':'json',
              'encoding': 'utf8',
              'indent':2,
          }
      },
      'USER_AGENT':"WADE",
      'ROBOTSTXT_OBEY':True,
      'CONCURRENT_REQUESTS':24,
  }

  def parse(self,response):
    quotes = response.xpath('//div[@class="standardText" and position()>=2]/p/text()').getall()
    authors = response.xpath('//div[@class="standardText"]/p/em/text()').getall()

    complete = [] 
    complete.extend(zip(quotes,authors))

    yield {
      'quotes': quotes,
      'authors': authors,
    }