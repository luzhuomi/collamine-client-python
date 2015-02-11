from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover() 
from django.conf import settings

from django.views.generic import TemplateView

import os

import crawler.views

urlpatterns = patterns('',
	url(r'^$', 'crawler.views.index'),
	url(r'^/$', 'crawler.views.index'),
	url(r'^piechart$', 'crawler.views.pie_chart'),
	url(r'^graphchart$', 'crawler.views.graph_chart'),
	url(r'^home$', 'crawler.views.home'),
	url(r'^crawler/stats/$', 'crawler.views.crawler_stats'),
	url(r'^crawler/stats/json/$', 'crawler.views.crawler_stats_json'),	
	url(r'^crawler/stats/piejson/$', 'crawler.views.crawler_stats_Piejson'),
	url(r'^crawler/stats/chartjson/(?P<since>.*)$', 'crawler.views.crawler_stats_Chartjson'),
	url(r'^crawler/stats/totalcollamine/$', 'crawler.views.Total_Collamine'),	
	url(r'^crawler/stats/totaloriginal/$', 'crawler.views.Total_Original'),
	url(r'^crawler/stats/totalboth/$', 'crawler.views.Total_Both'),
	url(r'^crawler/stats/url/$', 'crawler.views.Total_Url'),
	url(r'^crawler/stats/Rurl/$', 'crawler.views.Total_RUrl'),
	url(r'^crawler/stats/ping/$', 'crawler.views.ping'),	
	url(r'^crawler/realtime/stats/(?P<since>.*)$', 'crawler.views.crawler_realtime_stats'),
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.BASE_DIR, 'static/')}),
)
