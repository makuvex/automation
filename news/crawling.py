from urllib.request import urlopen, urlretrieve
import urllib.request 
from bs4 import BeautifulSoup
import ssl, os, pymysql, time, sys
from datetime import datetime
from pprint import pprint
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from pyscheduler import PyScheduler
from mySqlService import mySqlService
from datetime import datetime
from dateutil import tz
import pytz

crawling_count = 3

sqlService = mySqlService()

def utcToKst(time):
	try:
		time_format = '%Y-%m-%dT%H:%M:%SZ'
		nyc_dt_naive = datetime.strptime(time, time_format)
		local_tz = pytz.timezone('Asia/Seoul')
		local_dt = nyc_dt_naive.replace(tzinfo=pytz.utc).astimezone(local_tz)
		return local_tz.normalize(local_dt)

		#2020-02-15T06:29:04Z
		#print('@@@ input time %s'%time)
		#to_zone = tz.gettz('Asia/Seoul')
		#utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
		#return utc.astimezone(to_zone)
	except Exception as e:
		print("=========== Errror %s ==========="%e)
		return ""


def crawling():
	context = ssl._create_unverified_context()
	header_info = {'Connection': 'close'}
	request = urllib.request.Request('https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako', headers=header_info)
	with urlopen(request, context=context) as response:
		soup = BeautifulSoup(response, 'html.parser')
		size = 0
		articles = soup.find_all('article')
		#print(f'@@@ articleCount {len(articles)}')

		for article in articles:
			try:
				print(f'@@@ size {size}')
				'''
				if size > crawling_count:
					return
				'''
				atag = article.find('h3').find('a')
				#2020-02-15T09:03:32Z
				link =  'https://news.google.com' + atag.get('href')[1:]
				
				title = atag.text
				#print('@@@ title %s'%title)
				author =  article.find('time').parent.find('a').text
				#print('@@@ author %s'%author)
				time = article.find('time').get('datetime')
				#print('@@@ time %s'%time)
				
				time = utcToKst(time)
				#2020-02-15T06:29:04Z
				img = article.parent.find('figure').find('img').get('src')
				
				#print('@@@@@ link %s\n, title %s\n, img %s\n, author %s\n, time %s'%(link, title, img, author, time))
				#sql = f"""insert into {preference.table_name}(description, image, link, media, site, site_name, title, type, url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
				
				#print('@@@ exist %s'%(sqlService.existsUrl(link)))

				if(link != None and sqlService.existsUrl(link) == False):
					json = {'image': img,
						   'url': link,
						   'site_name': author,
						   'date': time,
						   'title': title}

					pprint('before insert %s'%json)
					sqlService.insert(json)
					size += 1
				
			except Exception as e:
				#print("=========== Errror %s ==========="%e) 
				continue
			#finally:
				#print("=========== finally %s ==========="%size) 
				#size += 1

if __name__ == "__main__":
	#crawling()
	PyScheduler().runInterval(crawling, 60*60)	#10분

 
