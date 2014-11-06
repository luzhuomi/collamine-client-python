from django.db import models

# Create your models here.

class HTML(models.Model):
	url     = models.CharField(max_length=255,unique=True)
	domain  = models.CharField(max_length=512)
	content = models.TextField()
	source  = models.CharField(max_length=512)
	crawled_date = models.DateTimeField()


'''
$ PYTHONPATH=~/git/collamine-client-python/webapp/ DJANGO_SETTINGS_MODULE=webapp.settings scrapy shell
>>> from scrapybot.items import ScrapybotItem
>>> import datetime
>>> h = ScrapybotItem(url='http://www.google.com',crawled_date=datetime.datetime.now())
>>> h.save()
'''	


