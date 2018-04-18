#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="mydb") 
cursor = db.cursor()
sql1="insert into  family values('zt','123456',10,'123456','123456')"
sql2="select username from family where account=5"
try:
   cursor.execute(sql1)
   
   db.commit()
except:
    db.rollback()
#data=cursor.fetchone()
#print data
cursor.close()



db.close()
