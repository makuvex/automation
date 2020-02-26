import mysql.connector
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from preference import preference

def create_table(db_name, table_name):
    mydb = mysql.connector.connect(
      host = "localhost",
      user = preference.user,
      passwd= preference.passwd,
      database = db_name
    )

    mycursor = mydb.cursor()

    query = "CREATE TABLE " + table_name + " (sno int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
												description text,\
												image text,\
												link VARCHAR(255),\
												media VARCHAR(255),\
												site VARCHAR(255),\
												site_name VARCHAR(255),\
												title VARCHAR(255),\
												date VARCHAR(255),\
												url text)"
	
    mycursor.execute(query)
    
'''
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| sno        | int(11)      | NO   | PRI | NULL    |       |
| province   | varchar(255) | YES  |     | NULL    |       |
| street     | varchar(255) | YES  |     | NULL    |       |
| dispensary | varchar(255) | YES  |     | NULL    |       |
| tel        | varchar(255) | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+      
'''  
