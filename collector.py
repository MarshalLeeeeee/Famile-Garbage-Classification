import dump_station
import threading
import time
import hashlib
import pymysql.cursors


   
class Collector(threading.Thread):
    address = ''
    state = 0
    collector_id = ''
    
    # 0: idle state
    # 1: family loggin
    # 2: collector loggin
    # 3: repair max loggin
    
    space = [100,100,100]
    # in our simulation the space is discrete
    usedSpace = [0,0,0]


    
    
    threshold = 0.5
    timeGap = 2.0
    currentUser = ''

    def __init__(self, id,address, space = [100,100,100], threshold = 0.5, state = 0, debug = False, timeGap = 2.0):
		super().__init__()
		self.address = address
		self.space = space[:3]
		self.collector_id = id

		if(threshold > 0 and threshold <= 1):
			self.threshold = threshold
		else:
			self.threshold = 0.5

		if(debug):
			self.state = state
		else:
			self.state = 0


		self.currentUser = ''
		self.timeGap = timeGap
                


    def run(self):
               
                   
        '''
		global timeStampCondition, timeStamp
		while(1):
			if timeStampCondition.acquire():
				timeStamp[address] = time.time()
				timeStampCondition.release()
			time.sleep(timeGap)

       '''
    
    def logIn(self, userName, passWord,type):
                # type = 1 -> family type = 2 -> cardriver type = 3 -> repaircrew

                if (state == 0):
                     db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                     cursor = db.cursor()
                     if(type == 1):
                           sql1 = "select * from family where username='%s'"%(userName)
                           
                           cursor.execute(sql1)
                           data = cursor.fetchone()
                           if(data == None):
                               #帐号未注册
                               return 0
                           else:
                               sql2 = "select password  from family where username='%s'"%(userName)
                               cursor.execute(sql2)
                               data1 = cursor.fetchone()
                               for row in data1:
                                   if(row != passWord):
                                       #密码错误
                                       return 0

                                    
                                   else:
                                       self.state = 1
                                       self.currentUsr = usrName


                     elif(type == 2):
                         
                           sql1 = "select * from car where car_id='%s'"%(userName)
                           cursor.execute(sql1)
                           data = cursor.fetchone()
                           if(data == None):
                                #帐号未注册
                                return 0
                           else:
                               sql2 = "select password  from car where car_id='%s'"%(userName)
                               cursor.execute(sql2)
                               data1 = cursor.fetchone()
                               for row in data1:
                                   if(row != passWord):
                                       #密码错误
                                       return 0

                                    
                                   else:
                                       self.state = 2
                                       self.currentUsr = usrName
                               
                     elif(type == 3):
                            
                           sql1 = "select * from crew where crew_id='%s'"%(userName)
                           cursor.execute(sql1)
                           data = cursor.fetchone()
                           if(data == None):
                                #帐号未注册
                                return 0
                           else:
                               sql2 = "select password  from crew where crew_id='%s'"%(userName)
                               cursor.execute(sql2)
                               data1 = cursor.fetchone()
                               for row in data1:
                                   if(row != passWord):
                                       #密码错误
                                       return 0

                                    
                                   else:
                                       self.state = 3
                                       self.currentUsr = usrName
                    
                     cursor.close()
                     db.close()
                     
               

                '''
		usr = returnUsr(usrName) # implement returnUsr in database related, return dictionary
		if(hashlib.sha224(passWord.encode('utf-8')).hexdigest() == usr['encrypt']):
			self.state = usr['identity']
			self.currentUsr = usrName
			return 1
		else:
			# the password and the username is not correct
			return 0
                '''
     
    def logOut(self):
                '''
		if(state == 3):
			global errorFlagCondition, errorFlag, crewCenter
			if errorFlagCondition.acquire():
				errorFlag[self.address] = False
				errorFlagCondition.release()
			crewCenter.free(account(self.currentUsr))
			'''
                
		self.state = 0
		self.currentUsr = ''


	#数据库中查找self.currentUsr的条目，并修改相关信息。
    


         
    def dumpgarbage(self,garbageType):
                if (self.state != 1):
                        return [-1,'']
                else:
                     db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                     cursor = db.cursor()
                     
                     sql1 = " select account from family where username='%s'"%(self.currentUser)
                     cursor.execute(sql1)
                     data=cursor.fetchone()
                     for row in data:
                         currentaccount = row

                     if(row < 0):


                         
                          return 0
                         #账户余额不足
                     else:
                         self.usedSpace[garbageType] += 1
                         sql0 = "select count(*) from garbage"
                         cursor.execute(sql0)
                         data0=cursor.fetchone()
                         for row0 in data0:
                              garbage_size = row0
                         
                         garbage_id = str(garbage_size+1)#生成一个字符串
                         sql2 = "insert into garbage values('%s','%d',0,'null','%s','%s')"%(garbage_id,garbageType,self.currentUser,self.collector_id)
                         try:
  
                             cursor.execute(sql2)
                             db.commit()
                         except:

                             
                             db.rollback()
                         examSpace()
                         
                     
                     cursor.close()
                     db.close()
                     
 

                    '''
                    if .....: #若当前家庭账户余额为负，则不能扔垃圾。
                         return 0;
                    
                    else:       
                    
                        self.usedSpace[garbageType] += 1
                        #.....

                        #往表garbage中加入垃圾种类 ，username，collector address
                        examSpace()
                        return [garbageType,self.currentUsr]
                    '''

    def examSpace(self):
                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                
                sql0 = "select count(*) from garbage where garbage_type=0 and state=0 and garbage_collector_id='%s'"%(self.collector_id)
                cursor.execute(sql0)
                data=cursor.fetchone()
                for row in data:
                    self.usedSpace[0]=row

                    
                sql1 = "select count(*) from garbage where garbage_type=1 and state=0 and garbage_collector_id='%s'"%(self.collector_id)
                cursor.execute(sql1)
                data=cursor.fetchone()
                for row in data:
                    self.usedSpace[1]=row

                    
                sql2 = "select count(*) from garbage where garbage_type=2 and state=0 and garbage_collector_id='%s'"%(self.collector_id)
                cursor.execute(sql2)
                data=cursor.fetchone()
                for row in data:
                    self.usedSpace[2]=row

                
                cursor.close()
                db.close()
                '''
		for i in range(3):
			if(self.usedSpace[i] > self.space[i] *self. threshold):
				callCar(i)
    
               '''
                '''
    def callCar(self, garbageType):
		if(garbageType == 0):
			global garbageDamageFull, garbageDamageFullCondition
			if self.address not in garbageDamageFull:
				if garbageDamageFullCondition.acquire():
					garbageDamageFull.append(self.address)
                                        #.....


					
					#将collector的地址加入表garbageDamageFull中
					garbageDamageFullCondition.release()
		if(garbageType == 1):
			global garbageOrganFull, garbageOrganFullCondition
			if self.address not in garbageOrganFull:
				if garbageOrganFullCondition.acquire():
					garbageOrganFull.append(self.address)
					#.....
 


					
					#将collector的地址加入表garbageOrganFull中
					garbageOrganFullCondition.release()
		if(garbageType == 2):
			global garbageInorgFull, garbageInorgFullCondition
			if self.address not in garbageInorgFull:
				if garbageInorgFullCondition.acquire():
					garbageInorgFull.append(self.address)
					#.....



					
					#将collector的地址加入表garbageInorgFull中
					garbageInorgFullCondition.release()

       '''
     def spaceSet(self,space):
		if(self.state != 3):
			return 0
		for i in range(3):
                        examspace()
			if(space[i] < self.usedSpace[i]):
				flag = 0
				break
		if(flag):
			self.space = space[:3]
			db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
			cursor = db.cursor()



                        sql ="update garbage_collector set damage_capacity='%d',organ_capacity= '%d',inorgan_capacity='%d' where collector_id='%s'"%(space[0],space[1],space[2],self.collector_id)
                        try:
                            
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                        
			
			cursor.close()
                        db.close()
			return 1
		else:
			return 0

     def thresholdSet(self, threshold):
		if(self.state != 3):
			return 0
		if(threshold > 0 and threshold <= 1):
			self.threshold = threshold
			db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
			cursor = db.cursor()



                        sql ="update garbage_collector set threshold='%d' where collector_id='%s'"%(threshold,self.collector_id)
                        try:
                            
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                        
			
			cursor.close()
                        db.close()
			return 1
			
		else:
			return 0

		    
     def returnSpace(self):
		if(self.state != 3):
			return [-1,-1,-1]
		else:
			return self.space



     def returnUsedSpace(self):
		if(self.state != 3):
			return [-1,-1,-1]
		else:
                        examspace()
			return self.usedSpace

     def collectGarbage(self, garbageType):
		if(self.state != 2):
			return 0
		else:
			self.usedSpace[garbageType] = 0
			
			
     
                                                


    
