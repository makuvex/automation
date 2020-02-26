from pyscheduler import PyScheduler
from pylog import PyLog
from mySqlService import mySqlService as MySqlService

class NewsMySql:
	log = PyLog()
	log = log.setHandler("ERROR")
	sqlService = MySqlService()
	query_count = 10
	
	def __init__(self):
		self.log.debug("__init__")
		
	def loadNews(self, lastIndex=0):
		return self.sqlService.selectWithDate(lastIndex, self.query_count)
		#select sno, title from google where sno > 3;
