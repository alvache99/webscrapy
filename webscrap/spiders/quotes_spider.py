import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

class QuotesSpider(scrapy.Spider):
    name = "categoryMain"
    
    start_urls=[
        'http://dmoztools.net/'
     ]

    # def start_requests(self):
    #     urls = [
    #         'http://dmoztools.net/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
            
     
    #parse to extract all urls to crawl
    def parse(self, response):
        for category in response.xpath("//aside"):
            yield{
                'category': category.xpath(".//h2[@class='top-cat']/a/@href").extract_first()
            }

        #extract urls of cat and sub cat of main page
        s = Selector(response)
        urls = s.xpath("//h2[@class='top-cat']/a/@href").extract()
        urlsSub = s.xpath("//h3[@class='sub-cat']/a/@href").extract()
        #append list
        urlsjoined = urls + urlsSub
        for url in urlsjoined:
            #Append main url string with the extracted url
            varFront = "http://dmoztools.net"
            completeUrl = varFront + url
            #request, callback to another parse function that extracts title(with tag content), weburl 
            yield Request(completeUrl, callback=self.parse_following_urls, dont_filter=True)

    #parse to extract webtitle, and weburl
    def parse_following_urls(self, response):
        for subcat in response.xpath("//div[@class='site-item ']"):
            yield{
                'Webname' : subcat.xpath(".//div[@class='site-title']/text()").extract_first(),
                'Weburl'  : subcat.xpath(".//div[@class='title-and-desc']/a/@href").extract_first()
            }
           

        #  s = Selector(response)
        #  urls = s.xpath('//div[@id="example"]//a/@href').extract()
        #  for url in urls:
        #  yield Request(url, callback=self.parse_following_urls, dont_filter=True)
      
        #get subcategories
        # for subcat in response.xpath("//div[@class='cat-item']"):
        #         yield{
        #             'subcatein' : subcat.xpath(".//div[@class='browse-node']/text()").extract_first()
        #         }

        # for subcat in response.xpath("//div[@class='site-item ']"):
        #     yield{
        #         'Webname' : subcat.xpath(".//div[@class='site-title']/text()").extract_first(),
        #         'Weburl'  : subcat.xpath(".//div[@class='title-and-desc']/a/@href").extract_first()
        #     }
            
            

        #  next_page = response.xpath("//h2[@class='top-cat']/a/@href").extract_first()
        #  if next_page is not None:
        #      next_page_link = response.urljoin(next_page)
        #      yield scrapy.Request(url=next_page_link,callback=self.parse)
     


        