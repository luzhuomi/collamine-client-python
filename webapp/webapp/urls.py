from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover() 
from django.conf import settings

from django.views.generic import TemplateView

import os

import crawler.views

urlpatterns = patterns('',
	url(r'^$', 'crawler.views.index'),
	url(r'^crawler/stats/$', 'crawler.views.stats'),
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.BASE_DIR, 'static/')}),
)
