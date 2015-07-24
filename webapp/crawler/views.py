from django.shortcuts import render


from django import template

from crawler.models import HTML

from django.db import connections
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
import time
from datetime import datetime, timedelta

from django.utils import timezone

import json



# Create your views here.
def index(request):
	print settings.BASE_DIR
	return render(request, 'index.html',{ 'settings' :settings } )

def pie_chart(request):
	return render(request, 'piechart.html',{ 'settings' :settings } )

def graph_chart(request):
	return render(request, 'graphchart.html',{ 'settings' :settings } )

def home(request):
	return render(request, 'home.html',{ 'settings' :settings } )

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
	cursor.execute("	");
	collamine_cnt = cursor.fetchall()[0][0]

	cursor.execute("SELECT count(id) FROM crawler_html where source <> 'collamine'");
	original_cnt = cursor.fetchall()[0][0]
	return render(request, 'ajax/stats.xml', 
		{ 'settings' : settings, 
		  'results' : [ { 'name' : 'original', 'style' : '0000FF', 'count' : original_cnt },
						{ 'name' : 'collamine', 'style' : '0000F0', 'count' : collamine_cnt }]
		})



def crawler_stats_json(request):
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
	response_data = {
		  "chart":{
		    "caption":"Download distribution",
		    "palette":"2",
		    "showpercentvalues":"1"
		  },
		  "data":[{
		      "label":"original",
		      "value":original_cnt
		    },
		    {
		      "label":"collamine",
		      "value":collamine_cnt
		    }
		  ]
		}
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def crawler_stats_Piejson(request):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT count(id) FROM crawler_html where source = 'collamine'");
	collamine_cnt = cursor.fetchall()[0][0]

	cursor.execute("SELECT count(id) FROM crawler_html where source = 'original'");
	original_cnt = cursor.fetchall()[0][0]

	pie_data = {
		"cols": [
	        {"id":"items","label":"Items","pattern":"","type":"string"},
	        {"id":"downloads","label":"Downloads","pattern":"","type":"number"}
      	],

  		"rows": [
	        {"c":[{"v":"Original","f":None},{"v":original_cnt,"f":None}]},
	        {"c":[{"v":"CollaMine","f":None},{"v":collamine_cnt,"f":None}]},
      	]

	}

	return HttpResponse(json.dumps(pie_data), content_type="application/json")

def crawler_stats_Chartjson(request):
	since = (timezone.now()-timedelta(0,10)).strftime("%Y-%m-%d %H:%M:%S")
	cursor = connections['default'].cursor()
	cursor.execute("SELECT count(id) FROM crawler_html where source = 'collamine' AND crawled_date >= %s", [since]);
	collamine_cnt = cursor.fetchall()[0][0]

	cursor.execute("SELECT count(id) FROM crawler_html where source <> 'collamine' AND crawled_date >= %s", [since]);
	original_cnt = cursor.fetchall()[0][0]
	
	'''
	chart_data = {
		"cols": [
			{"id":"t","label":"downloads","type":"string"},
			{"id":"o","label":"Original","type":"number"},
			{"id":"c","label":"Collamine","type":"number"}
			],
		"rows": [
			{"c":[{"v":"","f":None},{"v":original_cnt,"f":None}, {"v":collamine_cnt,"f":None}]},
			],

	}
	'''

	chart_data = {
		'curr_time' : since,
		'original_count' : original_cnt,
		'collamine_count' : collamine_cnt
	}

	return HttpResponse(json.dumps(chart_data), content_type="application/json")

def Total_Collamine(request):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT count(source) FROM crawler_html WHERE source ='collamine' ")
	total_C = cursor.fetchall()[0][0]

	total_data = {
			"source":total_C
	}

	return HttpResponse(json.dumps(total_data), content_type="application/json")

def Total_Original(request):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT count(source) FROM crawler_html WHERE source ='original' ")
	total_O = cursor.fetchall()[0][0]

	total_data = {
			"source":total_O
	}

	return HttpResponse(json.dumps(total_data), content_type="application/json")

def Total_Both(request):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT count(source) FROM crawler_html ")
	total_B = cursor.fetchall()[0][0]

	total_data = {
			"source":total_B
	}

	return HttpResponse(json.dumps(total_data), content_type="application/json")

def Total_Url(request):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT DISTINCT count(domain) AS 'total', domain FROM crawler_html GROUP BY domain order by count(domain) desc LIMIT 10 ")

	# we need to get a list of all domain names
	# we also need get list of domain names with counts, but list is not efficient in this settings, we need to look up the counts based on domain name
	# thus we need a hash table (dictionary)

	domains = [] # ['hwz', 'somethingelse'] 

	domain_counts = {} # { 'hwz' -> 9000, 'somethinelse' -> 10 }

	# for each record in the cursor, we take the 1st column as the count and 2nd column as the domain name

	for r in cursor.fetchall():
		domain = r[1]
		domains.append(domain)
		count  = r[0]
		domain_counts[domain] = count 

	# convert domains and domain_counts into rows
	# as a results the rows should look like something as follows,
	# [ {"c":[{"v": 'hwz', "f":none}, {"v", 9000, "f":None}]}
	# , {"c":[{"v": 'somethingelse', "f":none}, {"v", 10, "f":None}]}
	# ]

	rows = []

	for domain in domains:
		row = {"c":[{"v":domain,"f":None},{"v":domain_counts[domain],"f":None}]}
		rows.append(row)


	url_data = {
		"cols": [
	        {"id":"name","label":"Website Urls","type":"string"},
	        {"id":"urls","label":"Total Visited","type":"number"}
      	],

  		"rows": rows
	}

	return HttpResponse(json.dumps(url_data), content_type="application/json")


def Total_RUrl(request):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT url, source, crawled_date FROM djangocrawler.crawler_html ORDER BY crawled_date DESC LIMIT 10 ")

	links = [] # ['url', 'source', YY-MM-DD] 
	'''
	[
		{
		'url': 'abc.com.sg'
		'source': 'collamine'
		'date': '2015-01-01'
		}
	]
	'''
	for r in cursor.fetchall():
		link = {
		'url' : r[0],
		'source' : r[1],
		'date' : (r[2]).strftime("%Y-%m-%d %H:%M:%S"),
		}
		links.append(link)

	rows  = []

	for link in links:
		row = {"c":[{"v":link['url'],"f":None},{"v":link['source'],"f":None},{"v":link['date'],"f":None}]}
		rows.append(row)

	url_data = {
		"cols": [
	        {"id":"Rurl","label":"Recent Urls","type":"string"},
	        {"id":"s","label":"Source","type":"string"},
	        {"id":"d","label":"Date","type":"number"},
      	],

  		"rows": rows
	}

	return HttpResponse(json.dumps(url_data), content_type="application/json")


def ping(request):
	"""
	start_t1 = time.clock()#start time
	elapsed = time.clock() #end time

	overall_t3 = int(elapsed / start_t1) + (elapsed % start_t1 > 0)
	
	#overall_t3 = (end_t2 - start_t1) * 1000
	"""
	start = datetime.now()	
	end = datetime.now()

	minutes = (end - start).total_seconds() * 10000000

	total_data = {
				"test": minutes
	}

	return HttpResponse(json.dumps(total_data), content_type="application/json")


def crawler_realtime_stats(request,since):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT count(id) FROM crawler_html where source = 'collamine' AND crawled_date >= %s", [since]);
	collamine_cnt = cursor.fetchall()[0][0]

	cursor.execute("SELECT count(id) FROM crawler_html where source <> 'collamine' AND crawled_date >= %s", [since]);
	original_cnt = cursor.fetchall()[0][0]
	to_json = { 'original' : original_cnt,
				'collamine' : collamine_cnt }
		
	return HttpResponse(json.dumps(to_json))

