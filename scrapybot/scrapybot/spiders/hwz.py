from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapybot.items import ScrapybotItem
from scrapybot.utils import normalizeFriendlyDate

import datetime
from dateutil.parser import parse


class HwzSpider(CrawlSpider):
    name = "hwz"
    allowed_domains = ["hardwarezone.com.sg"]
    domain = "www.hardwarezone.com" # for collamine upload
    start_urls = [
        "http://forums.hardwarezone.com.sg/current-affairs-lounge-17/"
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('current\-affairs\-lounge\-17/.*\.html', )), callback='parse_item', follow=True),
    )	
    """
    When writing crawl spider rules, avoid using parse as callback, since the CrawlSpider uses the parse method itself to implement its logic. So if you override the parse method, the crawl spider will no longer work.
    """
    def parse_item(self, response):
        source="orginal"
        if ((response.flags) and ("collamine" in response.flags)):
            source="collamine"
        i = ScrapybotItem(url=response.url,
            domain=self.allowed_domains[0],
            source=source,
            content=response.body.decode(response.encoding),
            crawled_date=datetime.datetime.now())
        i.save()
