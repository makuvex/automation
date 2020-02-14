# -*- coding: utf-8 -*-
from gnewsclient_in import MyNewsClient
from pprint import pprint
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from pyscheduler import PyScheduler
from pylog import PyLog
from mySqlService import mySqlService
import json
import urllib.parse

query_count = 10

log = PyLog()
log = log.setHandler("WARNING")
sqlService = mySqlService()

def getNews():
	try:
		log.warning('@@@ start @@@')
		#client = MyNewsClient(language='korean', location='Republic of Korea', topic='Top Stories', max_results=5)
		client = MyNewsClient(language='korean', location='Republic of Korea', topic='Top Stories', use_opengraph=True, max_results=query_count)
		#pprint(client.get_news())
		#pprint(type(client.get_news()[0]))
		list = client.get_news()
		for json in list:
			if(json['url'] != None and sqlService.existsUrl(json['url']) == False):
				sqlService.insert(json)
				log.warning(f"@@@ add column {json['title']}")
			else:
				log.warning(f"@@@ exists column {json['title']}")
	except Exception as e:
		log.warning(f'@@@ error {e} @@@')

if __name__ == '__main__':
	PyScheduler().runInterval(getNews, 60*10)	# 10분
