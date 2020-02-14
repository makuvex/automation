https://github.com/nikhilkumarsingh/gnewsclient

PyPI license

gnewsclient
An easy-to-use python client for Google News feeds.

Installation
To install gnewsclient, simply,

$ pip install gnewsclient
Usage
Create a NewsClient object:

>>> from gnewsclient import gnewsclient
>>> client = gnewsclient.NewsClient(language='hindi', location='india', topic='Business', max_results=3)
Get current parameter settings

>>> client.get_config()
{'location': 'india', 'language': 'hindi', 'topic': 'Sorts'}

Get news feed
>>> client.get_news()

Get news feed with OpenGraph data
>>> client = gnewsclient.NewsClient(language='hindi', location='india', topic='Business', use_opengraph=True, max_results=5)

Changing parameters
>>> client.location = 'india'
>>> client.language = 'hindi'
>>> client.topic = 'Sports'
>>> client.get_news()

Get list of available locations, languages and topics
>>> client.locations
>>> client.languages
>>> client.topics
