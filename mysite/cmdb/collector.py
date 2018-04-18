#import dump_station
import threading
import time
import hashlib
import pymysql.cursors


   
class Collector:
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
    currentUsr = ''

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


        self.currentUsr = ''
        self.timeGap = timeGap
                


    # def run(self):
               
                   
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

                if (self.state == 0):
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
                                       return 1

                                    
                                   else:
                                       self.state = 1
                                       self.currentUsr = userName


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
                                       return 1

                                    
                                   else:
                                       self.state = 2
                                       self.currentUsr = userName
                               
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
                                       return 1

                                    
                                   else:
                                       self.state = 3
                                       self.currentUsr = userName
                    
                     cursor.close()
                     db.close()
                     
               

         
     
    def logOut(self):
        
        self.state = 0
        self.currentUsr = ''


#数据库中查找self.currentUsr的条目，并修改相关信息。
    


         
    def dumpgarbage(self,garbageType):
                if (self.state != 1):
                        return -1
                else:
                     db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                     cursor = db.cursor()
                     sql1 = " select account from family where username='%s'"%(self.currentUsr)
                     cursor.execute(sql1)
                     data=cursor.fetchone()
                     for row in data:
                         currentaccount = row

                         
                     flag1 = 0
                     flag2 = 0
                     self.examSpace()
                     self.examSpace0()

                     
                     if(currentaccount < 0):
                           flag1 = 0
                           return 0
                     else:
                           flag1 = 1

                           
                     if(self.usedSpace[garbageType] >= 2*self.threshold*self.space[garbageType]):
                           flag2 = 0
                           return 1
                     else:
                           flag2 = 1

                     if(flag1 == 1 and flag2 == 1):
                          self.usedSpace[garbageType] += 1
                          sql0 = "select count(*) from garbage"
                          cursor.execute(sql0)
                          data0=cursor.fetchone()
                          for row0 in data0:
                              garbage_size = row0
                         
                          garbage_id = str(garbage_size+1)#生成一个字符串
                          sql2 = "insert into garbage values('%s','%d',0,'123456','%s','%s')"%(garbage_id,garbageType,self.currentUsr,self.collector_id)
                          # print(garbage_id)
                          # print(self.currentUsr)
                          # print(self.collector_id)
                          try:
                             cursor.execute(sql2)
                             db.commit()
                             print('exactly')
                          except:
                             print('fail')
                             db.rollback()
                         
                     else:
                          return 0
                         
                         
                     
                     cursor.close()
                     db.close()
                     
 


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

                    
    def examSpace0(self):
                db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
                cursor = db.cursor()
                sql3 = "select damage_capacity,organ_capacity,inogran_capacity from garbage_collector where collector_id='%s'"%(self.collector_id)
                cursor.execute(sql3)
                data = cursor.fetchone()

                self.space[0] = data[0]
                self.space[1] = data[1]
                self.space[2] = data[2]
                cursor.close()
                db.close()


                
    def spaceSet(self,space):
        if(self.state != 3):
            return 0
        for i in range(3):
            self.examSpace()
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
            self.examSpace0()
            return self.space

    def returnUsedSpace(self):
            self.examSpace()
            return self.usedSpace

    def collectGarbage(self, garbageType):
        if(self.state != 2):
            return 0
        else:
            self.usedSpace[garbageType] = 0
