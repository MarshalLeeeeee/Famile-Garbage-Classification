#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql.cursors


db = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="mydb")

sql0="insert into  family values('cnm','123456',30,'123456','123456')"
sql1="insert into  family values('zt','123456',30,'123456','123456')"
sql2="insert into  family values('zcf','123456',30,'123456','123456')"
sql3="insert into  family values('lmc','123456',30,'123456','123456')"
sql4="insert into  dump_station values('123456','123456',0)"
sql5="insert into garbage_collector values('654321','654321',0.5,100,100,100,0)"
sql6="insert into car_center values('12345','12345')"
sql7="insert into car values('0','123456','0',0,'12345','0')"
sql8="insert into car values('1','123456','0',1,'12345','1')"
sql9="insert into car values('2','123456','0',2,'12345','2')"
sql10="insert into crew_center values('54321','54321')"
sql11="insert into crew values('0','123456','123456',0,0,'54321')"
sql12="insert into crew values('1','123456','123456',0,1,'54321')"
sql13="insert into crew values('2','123456','123456',0,2,'54321')"


cursor = db.cursor()

try: 
    cursor.execute(sql0)
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.execute(sql5)
    cursor.execute(sql6)
    cursor.execute(sql7)
    cursor.execute(sql8)
    cursor.execute(sql9)
    cursor.execute(sql10)
    cursor.execute(sql11)
    cursor.execute(sql12)
    cursor.execute(sql13)
    
    db.commit()
except:
    print(0)
    db.rollback()



'''

cursor.execute(sql16)
data=cursor.fetchall()

for row in data:
    print (row)
'''




cursor.close()
db.close()
