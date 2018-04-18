import threading
import time
import hashlib
import pymysql.cursors
import random


class CarCenter(threading.Thread):
    car_center_id = ''
    address = ''

    def __init__(self, car_center_id , address):

            self.car_center_id = car_center_id
            self.address = address

    def addCar(self, userName ,garbageType):
                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                sql1 = "select * from car where car_id='%s'"%(userName)
                cursor.execute(sql1)
                data=cursor.fetchone()
                if(data == None):
                        flag = 1
                else:
                        flag = 0
                if(flag == 1):
                        sql2 = "insert into car values('%s','123456','0','%d','%s','%s')"%(userName,garbageType,self.car_center_id,userName)
                        try:
                                cursor.execute(sql2)
                                db.commit()
                        except:
                                db.rollback()
                else:
                        return 0

                
                cursor.close()
                db.close()


    def deleteCar(self, userName):

                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                sql = "delete from car where car_id='%s' and car_state='0' "%(userName)
                try:
                        cursor.execute(sql)
                        db.commit()
                except:
                        db.rollback()
                

                
                cursor.close()
                db.close()
                

    def free(self, userName):
                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                
                
                sql = "update car set car_state='0'where car_id='%s' and car_state<>'0' "%(userName)
                try:
                        cursor.execute(sql)
                        db.commit()
                except:
                        db.rollback()
                

                
                cursor.close()
                db.close()

    def busy(self, userName,collector_id):
                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                
                print("run busy")
                sql = "update car set car_state='%s' where car_id='%s' "%(collector_id,userName)
                print(userName,collector_id)
                try:
                        cursor.execute(sql)
                        
                        db.commit()
                except:
                        print("fail")
                        db.rollback()
                

                
                cursor.close()
                db.close()


    def run(self):
                while(True):
                        db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                        cursor = db.cursor()
                        flag1 = 0
                        sql1 ="select count(*),garbage_collector_id,threshold,damage_capacity from garbage,garbage_collector where garbage_collector_id=collector_id and garbage_type=0 and state=0 group by garbage_collector_id"
                        cursor.execute(sql1)
                        data=cursor.fetchall()
                        for row in data:
                               
                                   if(row[2]*row[3]<=row[0]):
                                       
                                       flag1 = 1
                                       damagefullcollector=row[1]
                                       break
                        sql2 = "select  car_id from car where car_state='0' and garbage_type=0"
                        cursor.execute(sql2)
                        data=cursor.fetchone()
                        
                        if(data == None):
                                flag2 = 0
                        else:
                                flag2 = 1
                                for row in data:
                                
                                        garbagecar_id = row

                        
                        if(flag1 == 1 and flag2 == 1):
                              
                              self.busy(garbagecar_id,damagefullcollector)
                              
                              #sql = "update car set car_state='%s' where car_id='%s' "%(damagefullcollector,garbagecar_id)
                              #sql = "update car set car_state='%s' where car_id='%s' "%(damagefullcollector,garbagecar_id)
                              
                    
                              sql3 = "update garbage set state=1 where garbage_collector_id='%s' and garbage_type='%d' and state=0"%(damagefullcollector,0)
                              try:
                                      cursor.execute(sql3)
                                      db.commit()
                              except:
                                      db.rollback()



                        flag1 = 0
                        sql1 ="select count(*),garbage_collector_id,threshold,organ_capacity from garbage,garbage_collector where garbage_collector_id=collector_id and garbage_type=1 and state=0 group by garbage_collector_id"
                        cursor.execute(sql1)
                        data=cursor.fetchall()
                        for row in data:
                                   if(row[2]*row[3]<=row[0]):
                                       print(row)
                                       flag1 = 1
                                       organfullcollector=row[1]
                                       break
                        sql2 = "select  car_id from car where car_state='0' and garbage_type=1"
                        cursor.execute(sql2)
                        data=cursor.fetchone()
                        
                        if(data == None):
                                flag2 = 0
                        else:
                                flag2 = 1
                                for row in data:
                                      garbagecar_id = row

                        
                        if(flag1 == 1 and flag2 == 1):
                                
                              self.busy(garbagecar_id,organfullcollector)
                              sql3 = "update garbage set state=1 where garbage_collector_id='%s' and garbage_type='%d'and state=0"%(organfullcollector,1)
                              try:
                                      cursor.execute(sql3)
                                      db.commit()
                              except:
                                      db.rollback()


                        flag1 = 0
                        sql1 ="select count(*),garbage_collector_id,threshold,inogran_capacity from garbage,garbage_collector where garbage_collector_id=collector_id and garbage_type=2 and state=0 group by garbage_collector_id"
                        cursor.execute(sql1)
                        data=cursor.fetchall()
                        for row in data:
                            
                                   if(row[2]*row[3]<=row[0]):
                                       
                                       flag1 = 1
                                       inorganfullcollector=row[1]
                                       break
                        sql2 = "select  car_id from car where car_state='0' and garbage_type=2"
                        cursor.execute(sql2)
                        data=cursor.fetchone()
                        
                        if(data == None):
                                flag2 = 0
                        else:
                                flag2 = 1
                                for row in data:
                                       garbagecar_id = row

                        
                        if(flag1 == 1 and flag2 == 1):
                                
                              self.busy(garbagecar_id,inorganfullcollector)
                              sql3 = "update garbage set state=1 where garbage_collector_id='%s' and garbage_type='%d'and state=0"%(inorganfullcollector,2)
                              try:
                                      cursor.execute(sql3)
                                      db.commit()
                              except:
                                      db.rollback()
                        

                        cursor.close()
                        db.close()
                        time.sleep(3.0)

global garbagecarcenter
garbagecarcenter = CarCenter('12345','12345')
garbagecarcenter.run()
