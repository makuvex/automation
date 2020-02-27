import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preference import preference
from create_table_news import create_table
from create_db import create_db

create_db(preference.db_name)
create_table('news', 'google')
