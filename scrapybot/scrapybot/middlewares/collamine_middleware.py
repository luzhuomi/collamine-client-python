
import urllib
import urllib2
import socket
import datetime
import requests


from scrapy.http import Response
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest

class CollaMineDownloadMiddleware():
	def process_request(self, request, spider):
		collamine_response = try_collamine(request.url)
		if collamine_response:
			response = HtmlResposne(url=request.url, body=collamine_response,flags=["collamine"])
			return response
		else:
			return None

COLLAMINE_DOWNLOAD_URL="http://127.0.0.1:9000/download/html/"

def try_collamine(url):
	timeout = 20
	socket.setdefaulttimeout(timeout)
	req = urllib2.Request(COLLAMINE_DOWNLOAD_URL+urllib.quote_plus(url))
	print ("calling " + COLLAMINE_DOWNLOAD_URL+urllib.quote_plus(url))
	try:
		response = urllib2.urlopen(req)
		if response:
			body = response.read()
			if body == "not found":
				return None
			else:
				# create the proper response
				return body
		else:
			# not found
			return None
	except Exception as e:
		return None


class CollaMineUploadMiddleware():
	def process_spider_input(self,response,spider):
		if (response.flags and ("collamine" in response.flags)):
			return None
		else:
			upload_to_collamine(response.url,response.body.decode(response.encoding))
			return None

COLLAMINE_UPLOAD_URL = "http://127.0.0.1:9000/upload/html/multipart/"

def upload_to_collamine(url,content):
	dt = datetime.datetime.now()
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = dt - epoch

	formdata = {
		"domain": "www.hardwarezone.com",
		"url":url,
		"crawltime": int(delta.total_seconds()),
		"contributor": "test"
	}

	files = {"document":content}

	r = requests.post(COLLAMINE_UPLOAD_URL, data=formdata,files=files)

	print ("upload status: " + r.text)
	return r

