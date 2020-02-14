import os
import sys

class preference:
    host = 'localhost'
    db_name = 'news'
    table_name = 'google'
    user = 'makuvex7'
    passwd = 'malice77'
    db_path = os.path.abspath(os.path.dirname(__file__)) + '/db'
    
