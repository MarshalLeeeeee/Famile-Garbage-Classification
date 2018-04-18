import threading
import time
import hashlib
import pymysql.cursors
import random
class garbage_examination:
    address = ''
    id = ''
    def __init__(self, id,address):
        self.id = id
        self.address = address
        self.state = 0


    def run(self):
            while(True):
                    db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                    cursor = db.cursor()
                    score = random.random()
                    
                    sql1 = "select garbage_id from garbage where state=2"
                    cursor.execute(sql1)
                    data1 = cursor.fetchone()
                    flag = 0
                    if(data1 == None):
                        flag = 0
                    else:
                        flag = 1
                    if(flag == 1):
                      for row in data1:
                            id = row
                      score = random.random()
                      if(score > 0.1):#奖励
                            sql2 = "select username from garbage where garbage_id='%s'"%(id)
                            cursor.execute(sql2)
                            data2 = cursor.fetchone()
                            # print(data2)
                            for row in data2:
                                    family_id = row
                                    print(family_id)
                            sql3 = "update garbage set state=3 where garbage_id='%s'"%(id)
                            try:
                                  cursor.execute(sql3)
                                  print("exam successfully")
                                  db.commit()
                            except:
                                    db.rollback()
                            self.raiseReward(family_id)
                        
                      else:#罚款
                            sql2 = "select username from garbage where garbage_id='%s'"%(id)
                            cursor.execute(sql2)
                            data2 = cursor.fetchone()
                            for row in data2:
                                    family_id = row
                            sql3 = "update garbage set state=4 where garbage_id='%s'"%(id)
                            try:
                                  cursor.execute(sql3)
                                  print("exam successfully")
                                  db.commit()
                            except:
                                    db.rollback()
                            
                            self.raisePenalty(family_id)
                    cursor.close()
                    db.close()
                    time.sleep(2)


    
    def raisePenalty(self,userName):
        db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
        cursor = db.cursor()
        sql = "update family set account=account-10 where username='%s'"%(userName)
        try:
                cursor.execute(sql)
                db.commit()
        except:
                        
                db.rollback()
        cursor.close()
        db.close()
                

    def raiseReward(self,userName):
        db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
        cursor = db.cursor()
        sql = "update family set account=account+10 where username='%s'"%(userName)
        try:
                cursor.execute(sql)
                db.commit()
        except:
                        
                db.rollback()

        cursor.close()
        db.close()

exam = garbage_examination('123456','123456')
exam.run()
