# -*- coding: utf-8 -*-

# Scrapy settings for scrapybot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapybot'

SPIDER_MODULES = ['scrapybot.spiders']
NEWSPIDER_MODULE = 'scrapybot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapybot (+http://www.yourdomain.com)'


DOWNLOADER_MIDDLEWARES = {
    'scrapybot.middlewares.collamine_middleware.CollaMineDownloadMiddleware': 543,
}

SPIDER_MIDDLEWARES = {
    'scrapybot.middlewares.collamine_middleware.CollaMineUploadMiddleware': 543,	
}