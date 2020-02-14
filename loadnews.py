from pyscheduler import PyScheduler
from pylog import PyLog
from mySqlService import mySqlService as MySqlService

class NewsMySql:
	log = PyLog()
	log = log.setHandler("DEBUG")
	sqlService = MySqlService()
	query_count = 3
	
	def __init__(self):
		self.log.debug("__init__")
		
	def loadNews(self, lastIndex=0):
		return self.sqlService.selectWithIndex(lastIndex, self.query_count)
		#select sno, title from google where sno > 3;
