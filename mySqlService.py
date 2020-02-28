import pymysql
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preference import preference
import json
from pprint import pprint

class mySqlService:
    cur = None
    con = None
	
    def __init__(self):
        #print('__init__')
        self.con = pymysql.connect(host=preference.host, 
                              user=preference.user, 
                              password=preference.passwd, 
                              db=preference.db_name, 
                              charset='utf8')
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()
        
    def insert(self, json):
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ insert')
        #v = json['site']
        #print(f'@@@ insert {v}')
        sql = f"""insert into {preference.table_name}(description, image, link, media, site, site_name, title, date, url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cur.execute(sql, (json['description'] if 'description' in json else "", 
							   json['image'] if 'image' in json else "", 
							   json['link'] if 'link' in json else "", 
							   json['media'] if 'media' in json else "", 
							   json['site'] if 'site' in json else "", 
							   json['site_name'] if 'site_name' in json else "",
							   json['title'] if 'title' in json else "",
							   json['date'] if 'date' in json else "",
							   json['url'] if 'url' in json else ""))
        self.con.commit()

    def selectAll(self):
        #print('selectLink')
        sql = "select * from " + preference.table_name
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def deleteAllRow(self):
        sql = "DELETE FROM " + preference.table_name
        self.cur.execute(sql)
        self.con.commit()
        
    def existsUrl(self, url):
        #sql = f"select EXISTS (select * from {preference.table_name} where url={url}) as isChk"
        sql = f"SELECT * FROM {preference.table_name} WHERE url LIKE '%{url}%' LIMIT 1"
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result != None

    def selectWithDate(self, lastIndex = 0, count = 3):
        self.con = pymysql.connect(host=preference.host, 
                              user=preference.user, 
                              password=preference.passwd, 
                              db=preference.db_name, 
                              charset='utf8')
        self.cur = self.con.cursor()

        if(lastIndex == 0):
            sql = "select * from " + preference.table_name + " ORDER BY date DESC LIMIT " + str(count)
        else:
            sql = "select * from " + preference.table_name + " WHERE sno < " + str(lastIndex) + " ORDER BY date DESC LIMIT " + str(count)
			
        #print(f'sql selectWithIndex {sql}')
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        
        pprint(f'mySqlService fetch result {rows[0]}')
        resultJson = {'status': '200', 'results': None}
        
        if(len(rows) == 0):
            return resultJson
        
        array = []
        i = 0
        for row in rows:
            img = row[2].split('=-p')[0]
            #print('@@@ row[2] %s\n img %s'%(row[2], img))
            array.append({'sno': row[0], 
                          'description': row[1],
                          'image': img if img != None else row[2],
                          'link': row[3],
                          'media': row[4],
						  'site': row[5],
						  'site_name': row[6],
						  'title': row[7],
						  'date': row[8],
						  'url': row[9]})
            i += 1
        #print(f'count {len(array)}')
        self.con.close()
        return {'status': '200', 'results': array}
	
    def selectAllToJson(self, count = 10):
        sql = "select * from " + preference.table_name + " LIMIT " + count
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        
        resultJson = {'status': '200', 'results': None}
        
        if(len(rows) == 0):
            return resultJson
        
        array = []
        i = 0
        for row in rows:
            img = row[2].split('=-p')[0]
            #print('@@@ row[2] %s\n img %s'%(row[2], img))
            array.append({'sno': row[0], 
                          'description': row[1],
                          'image': img if img != None else row[2],
                          'link': row[3],
                          'media': row[4],
						  'site': row[5],
						  'site_name': row[6],
						  'title': row[7],
						  'date': row[8],
						  'url': row[9]})
            i += 1

        return {'status': '200', 'results': array}
        
        
if __name__ == "__main__":
	sql = mySqlService()
	pprint(sql.selectWithDate(3))
        
