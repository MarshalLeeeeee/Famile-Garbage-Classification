import threading
import time
import hashlib
import pymysql.cursors
import random
class DumpStation:

    address = ''
    garbageCondition = threading.Condition()
    

    
    def __init__(self, address):
        self.address = address
        self.state = 0
        self.garbageCondition = threading.Condition()

    def free(self, userName):
        db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="mydb")
        cursor = db.cursor()
        sql = "update car set car_state='0'where car_id='%s' and car_state<>'0' " % (userName)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()
        db.close()


    def dump(self, userName, passWord):
                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                sql1 = "select * from car where car_id='%s'"%(userName)
                cursor.execute(sql1)
                data1 = cursor.fetchone()
                if(data1 == None):
                       #帐号未注册
                       return 0
                       
                else:
                       sql2 = "select password from car where car_id='%s'"%(userName)
                       cursor.execute(sql2)
                       data2 = cursor.fetchone()
                       for row in data2:
                               if(row == passWord):
                                       flag = 1
                               else:
                                       flag = 0

                       if(flag == 0):
                               return 1
                              #密码错误
                       else:
                              sql3 = "select garbage_type from car where car_id='%s'"%(userName)
                              cursor.execute(sql3)
                              data3 = cursor.fetchone()
                              for row in data3:
                                      garbagetype = row
                              sql4 = "select car_state from car where car_id='%s'"%(userName)
                              cursor.execute(sql4)
                              data4 = cursor.fetchone()
                              for row in data4:
                                      collector_id = row
                              sql5 = "update garbage set state=2 where garbage_collector_id='%s' and garbage_type='%d'and state=1"%(collector_id,garbagetype)
                              try:
                                      cursor.execute(sql5)
                                      db.commit()
    
                              except:
                                      db.rollback()
                              self.free(userName)
                    
 
                cursor.close()
                db.close()
                '''
		usr = returnUser(userName) # implement returnUser in database related, return dictionary
		if(userName.type == 2 and hashlib.sha224(passWord.encode('utf-8')).hexdigest() == usr['encrypt']):
                        garbagecarcenter.free(usrName)
			if self.garbageCondition.acquire():
				self.garbageForCheck += car.garbage
				#表garbageForCheck中加入垃圾条目
				self.garbageCondition.release()

			return 1
		else:
			# the password and the username is not correct
			return 0
		'''	

    def run(self):
            while(True):
                    db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                    cursor = db.cursor()
                    score = random.random()
                    
                    sql1 = "select garbage_id from garbage where state=2"
                    cursor.execute(sql1)
                    data1 = cursor.fetchone()
                    for row in data1:
                            id = row
                    score = random.random()
                    if(score > 0.1):#奖励
                            sql2 = "select username from garbage where garbage_id='%s'"%(id)
                            cursor.execute(sql2)
                            data2 = cursor.fetchone()
                            for row in data2:
                                    family_id = row
                            sql3 = "update garbage set state=3 where garbage_id='%s'"%(id)
                            try:
                                  cursor.execute(sql3)
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
                                  db.commit()
                            except:
                                    db.rollback()
                            
                    self.raisePenalty(family_id)
                    cursor.close()
                    db.close()
                    time.sleep(2)

            '''
		while(True):
			if len(garbageForCheck) and self.carCondition.acquire():#表garbageForCheck非空
				result = exam(garbageForCheck[0])
				upload(result)
				if (len(garbageForCheck) == 1):
					garbageForCheck = []
				else:
					garbageForCheck = garbageForCheck[1:]
				self.carCondition.release()
			time.sleep(2.1)
	'''

    
    def raisePenalty(userName):
        db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
        cursor = db.cursor()
        sql1 = "select account from family where  username='%s'"%(userName)
                
        cursor.execute(sql1)
        data = cursor.fetchone()
        for row in data:
            account = row
            account -= 10
            sql2 = "update family set account='%d' where username='%s'"%(account,userName)
            try:
                cursor.execute(sql2)
                db.commit()
            except:
                        
                db.rollback()


                
                cursor.close()
                db.close()
                

    def raiseReward(usrName):
        db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
        cursor = db.cursor()
        sql1 = "select account from family where  username='%s'"%(userName)
        cursor.execute(sql1)
        data = cursor.fetchone()
        for row in data:
            account = row
            account += 10
            sql2 = "update family set account='%d' where username='%s'"%(account,userName)
            try:
                cursor.execute(sql2)
                db.commit()
            except:
                db.rollback()
                cursor.close()
                db.close()
