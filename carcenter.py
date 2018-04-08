import dump_station
import threading
import time
import hashlib
import pymysql.cursors
import random
class CarCenter(threading.Thread):
          '''
	cars = []
	freeCars = []
	busyCars = []
	'''
        car_center_id = ''
        address = ''
	carCondition = threading.Condition()

	def __init__(self,car_center_id,address):
		super().__init__()
		'''
		self.cars = []
		self.freeCars = []
		self.busyCars = []
		'''
		self.carCondition = threading.Condition()
                self.car_center_id = car_center_id
                self.address = address
	def addCar(self, userName,garbageType):
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
                        #car_id已被使用

                
                cursor.close()
                db.close()
                '''
		if(c not in self.cars and self.carCondition.acquire()):
			self.cars.append(c)
			self.freeCars.append(c)
			#表car中加入car的条目,状态为空闲，garbageType为-1



			
			self.carCondition.release()
			return 1
		else:
			return 0
		'''

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
                
                '''
		if(c in self.freeCars and self.carCondition.acquire()):
			self.freeCars.remove(c)
			self.cars.remove(c)
			#表car中删除car的条目
			self.carCondition.release()
			return 1
		else:
			return 0
               '''
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
                '''
		if(userName in self.busyCars and self.carCondition.acquire()):
			self.busyCars.remove(userName)
			self.freeCars.append(userName)
			#将车的状态改为空闲
			self.carCondition.release()
			return 1
		else:0
			return 0
		'''
	def busy(self, userName,collector_id):
                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                
                
                sql = "update car set car_state='%s' where car_id='%s' and car_state=='0' "%(collector_id,userName)
                try:
                        cursor.execute(sql)
                        db.commit()
                except:
                        db.rollback()
                

                
                cursor.close()
                db.close()
                '''
		if(userName in self.freeCars and self.carCondition.acquire()):
			self.freeCars.remove(userName)
			self.busyCars.append(userName)
			#将车的状态改为collector的address
			self.carCondition.release()
			return 1
		else:0
			return 0
               '''

	def run(self):
		while(True):
                        db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                        cursor = db.cursor()
                        
                        sql1 ="select garbage_collector_id from garbage,garbage_collector where garbage_type=0 and state=0 and garbage_collector_id=collector_id having count(garbage_id)>damage_capacity*threshold"
                        cursor.execute(sql1)
                        data=cursor.fetchone()
                        for row in data:
                                   damagefullcollector=row
                        if(data == None):
                                flag1 = 0
                        else:
                                flag1 = 1
                        sql2 = "select  car_id from car where car_state='0' and garbage_type=0"
                        cursor.execute(sql2)
                        data=cursor.fetchone()
                        for row in data:
                                garbagecar_id = row
                        if(data == None):
                                flag2 = 0
                        else:
                                flag2 = 1

                              
                        if(flag1 == 1 and flag2 == 1):
                                
                              busy(garbagecar_id,damagefullcollector)
                              sql3 = "update garbage set state=1 where garbage_collector_id='%s' and garbage_type='%d'"%(damagefullcollector,0)
                              try:
                                      cursor.execute(sql3)
                                      db.commit()
                              except:
                                      db.rollback()



                        sql1 ="select garbage_collector_id from garbage,garbage_collector where garbage_type=1 and state=0 and garbage_collector_id=collector_id having count(garbage_id)>organ_capacity*threshold"
                        cursor.execute(sql1)
                        data=cursor.fetchone()
                        for row in data:
                                   organfullcollector=row
                        if(data == None):
                                flag1 = 0
                        else:
                                flag1 = 1
                        sql2 = "select  car_id from car where car_state='0' and garbage_type=1"
                        cursor.execute(sql2)
                        data=cursor.fetchone()
                        for row in data:
                                garbagecar_id = row
                        if(data == None):
                                flag2 = 0
                        else:
                                flag2 = 1

                              
                        if(flag1 == 1 and flag2 == 1):
                                
                              busy(garbagecar_id,organfullcollector)
                              sql3 = "update garbage set state=1 where garbage_collector_id='%s' and garbage_type='%d'"%(organfullcollector,1)
                              try:
                                      cursor.execute(sql3)
                                      db.commit()
                              except:
                                      db.rollback()


                        sql1 ="select garbage_collector_id from garbage,garbage_collector where garbage_type=2 and state=0 and garbage_collector_id=collector_id having count(garbage_id)>inorgan_capacity*threshold"
                        cursor.execute(sql1)
                        data=cursor.fetchone()
                        for row in data:
                                   inorganfullcollector=row
                        if(data == None):
                                flag1 = 0
                        else:
                                flag1 = 1
                        sql2 = "select  car_id from car where car_state='0' and garbage_type=2"
                        cursor.execute(sql1)
                        data=cursor.fetchone()
                        for row in data:
                                garbagecar_id = row
                        if(data == None):
                                flag2 = 0
                        else:
                                flag2 = 1

                              
                        if(flag1 == 1 and flag2 == 1):
                                
                              busy(garbagecar_id,damagefullcollector)
                              sql3 = "update garbage set state=1 where garbage_collector_id='%s' and garbage_type='%d'"%(inorganfullcollector,2)
                              try:
                                      cursor.execute(sql3)
                                      db.commit()
                              except:
                                      db.rollback()
                        

                        cursor.close()
                        db.close()
                        time.sleep(3.0)
                        '''
                        if(garbageDamageFull is not empty):#对数据库中表garbageDamageFull进行判断是否非空
			
				global  garbageDamageFullCondition
				if garbageDamageFullCondition.acquire() and self.carCondition.acquire():
					if(freecar is not empty):#car中type=0的freecar非空
                                                #查询一辆空闲且garbageType = 0的车 username
                                                address为garbageDamageFull中的第一个地址。
						busy(username,address)
					self.carCondition.release()
					garbageDamageFullCondition.release()
			if(garbageOrganFull is not empty):#对数据库中表garbageOrganFull进行判断是否非空
			
				global  garbageOrganFullCondition
				if garbageOrganFullCondition.acquire() and self.carCondition.acquire():
					if(freecar is not empty):#car中type=0的freecar非空
                                                #查询一辆空闲且garbageType = 0的车 username
                                                address = garbageOrganFull中的第一个地址
						busy(username,address)
					self.carCondition.release()
					garbageOrganFullCondition.release()
			if(garbageInorgFull is not empty):#对数据库中表garbageInorgFull进行判断是否非空
			
				global  garbageInorgFullCondition
				if garbageInorgFullCondition.acquire() and self.carCondition.acquire():
					if(freecar is not empty):#car中type=0的freecar非空
                                                #查询一辆空闲且garbageType = 0的车 username
                                                address为garbageInorgFull中的第一个地址。
						busy(username,address)
					self.carCondition.release()
					garbageDamageFullCondition.release()
			
			time.sleep(2.0)
			'''
garbagecarcenter = carcenter()


class DumpStation(threading.Thread):

    address = ''
    garbageCondition = threading.Condition()
    

    
    def __init__(self, address):
		super().__init__()
		self.address = address
		
		self.state = 0
		self.garbageCondition = threading.Condition()
		
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
                               return 0
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
                              sql5 = "update garbage set state=2 where garbage_collector_id='%s' and garbage_type='%d'"%(collector_id,garbagetype)
                              try:
                                      cursor.execute(sql5)
                                      db.commit()
    
                              except:
                                      db.rollback()
                              free(userName)
                    
 
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
                            raiseReward(family_id)
                        
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
                            
                    raisePenalty(family_id)
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
