from django.shortcuts import render


from django import template

from crawler.models import HTML

from django.db import connections
from django.conf import settings


# Create your views here.
def index(request):
	print settings.BASE_DIR
	return render(request, 'index.html',{ 'settings' :settings } )




def crawler_stats(request):
	''' ORM makes it slow
	htmls = HTML.objects.all()
	result = { 'original' : 0, 'collamine' : 0}
	for html in htmls:
		if html.source == 'collamine':
			result['collamine'] += 1
		else:
			result['original'] += 1
	'''
	cursor = connections['default'].cursor()
	cursor.execute("SELECT count(id) FROM crawler_html where source = 'collamine'");
	collamine_cnt = cursor.fetchall()[0][0]

	cursor.execute("SELECT count(id) FROM crawler_html where source <> 'collamine'");
	original_cnt = cursor.fetchall()[0][0]
	return render(request, 'ajax/stats.xml', 
		{ 'settings' : settings, 
		  'results' : [ { 'name' : 'original', 'style' : '0000FF', 'count' : original_cnt },
						{ 'name' : 'collamine', 'style' : '0000F0', 'count' : collamine_cnt }]
		})

