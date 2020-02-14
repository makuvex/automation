from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler
#from pylog import PyLog

class PyScheduler:
	def __init__(self):
		self.scheduler = BlockingScheduler()

	def runInterval(self, func, interval):
		func()
		self.scheduler.add_job(func, 'interval', seconds=interval)
		self.scheduler.start()