from logging import handlers
import logging

'''
usage:
    log = PyLog()
    log = log.setHandler("CRITICAL")
    
    log.debug('debug 123')
    log.info('info 123')
    log.warning('warning 123')
    log.error('error 123')
    log.critical('critical 123')
'''

class PyLog:
    fileMaxByte = 1024 * 1024 * 100
    levels = {
        "DEBUG" : logging.DEBUG , 
        "INFO" : logging.INFO , 
        "WARNING" : logging.WARNING , 
        "ERROR" : logging.ERROR , 
        "CRITICAL" : logging.CRITICAL 
    }
    
    def __init__(self):
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    
    def setHandler(self, level, file = False):
        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamHandler)
        self.logger.setLevel(self.levels[level])
    
        if(file == True):
            fileHandler = logging.handlers.RotatingFileHandler(filename='./server.log', maxBytes=self.fileMaxByte, backupCount=10, mode='w')
            fileHandler.setFormatter(self.formatter)    
            self.logger.addHandler(fileHandler)
    
        return self.logger
    