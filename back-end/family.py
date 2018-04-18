import dump_station
import threading
import time
import hashlib
import pymysql.cursors

class familyoperate:
    userName = ''
    password = ''
    account = 0
    address = ''
    phonenum= ''
    def __init__(self,userName,password,account,address,phonenum):
        self.userName = ''
        self.password = ''
        self.account = 0
        self.address = ''
        self.phonenum = ''

        
      #注册
    def signup(self,userName,password,account,address,phonenum):
        if(userName==''or password==''):
            #注册失败 用户名密码不能为空
            return 0

        else:
            db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb") 
            cursor = db.cursor()
            sql1 = "select * from family where username='%s'"%(userName)
            cursor.execute(sql1)
            data=cursor.fetchone()
            if(data==None):
                sql2 = "insert into family values('%s','%s','%d','%s','%s')"%(userName,password,account,address,phonenum)
                try:
                    cursor.execute(sql2)
                    db.commit()
                except:
                    db.rollback()
            else:
                 #该用户名已存在。。。。。。、
         
                 return 0


                 
            cursor.close()
            db.close()




        
    def logIn(self, userName, passWord):
         if(self.userName == ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              sql1 = "select * from family where username='%s'"%(userName)
              cursor.execute(sql1)
              data = cursor.fetchone()
              if(data==None):
                    #帐号未注册


                  return 0
                    
              else:
                    sql2 = "select password from family where username='%s'"%(userName)
                    sql3 = " select account from family where username='%s'"%(userName)
                    sql4 = "select phonenum from family where username='%s'"%(userName)
                    sql5 = "select familycol from family where username='%s'"%(userName)
                    cursor.execute(sql2)
                    data1=cursor.fetchone()
                    for row in data1:
                        if(row != passWord):
                            #密码错误



                            return 0
                        else:
                            self.userName = userName
                            self.password = passWord
                            cursor.execute(sql3)
                            data1=cursor.fetchone()
                            for r in data1:
                                self.account = r
                            cursor.execute(sql4)
                            data1=cursor.fetchone()
                            for r in data1:
                                self.phonenum = r
                            cursor.execute(sql5)
                            data1=cursor.fetchone()
                            for r in data1:
                                self.address = r
  
                    

         
              cursor.close()
              db.close()

             
         else:
             #已有帐号 登录失败




             return 0
    def logout(self):
        if(self.userName == ''):
            return 0



        else:


             self.userName = ''
             self.password = ''
             self.account = 0
             self.address = ''
             self.phonenum = ''




    def showaccount(self):
        if(self.userName != ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              sql = " select account from family where username='%s'"%(self.userName)
              cursor.execute(sql)
              data= cursor.fetchone()
              for row in data:
                        self.account = row

              cursor.close()
              db.close()


              return self.account    
        else:
            return 0
            #账户未登录

    
    def recharge(self,money):#充值
        if(self.userName != ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              sql1 = " select account from family where username='%s'"%(self.userName)
              cursor.execute(sql1)
              data= cursor.fetchone()
              for row in data:
                        self.account = row + money

              
              
              sql2 = "update family set account='%d' where username='%s'"%(self.account,self.userName)
              try:
  
   
                   cursor.execute(sql2)
   
                   db.commit()
              except:
                  
                   db.rollback()
              cursor.close()
              db.close()
        else:
            return 0
            #账户未登录






    def showaddress(self):
        if(self.userName != ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              sql = " select address from family where username='%s'"%(self.userName)
              cursor.execute(sql)
              data= cursor.fetchone()
              for row in data:
                        self.address = row

              cursor.close()
              db.close()


              return self.address


    def changeaddress(self,address):
        if(self.userName != ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              self.address = address

              
              
              sql = "update family set familycol='%d' where username='%s'"%(address,self.userName)
              try:
  
   
                   cursor.execute(sql)
   
                   db.commit()
              except:
                  
                   db.rollback()
              cursor.close()
              db.close()
        else:
            return 0
            #账户未登录




    def showphonenum(self):
        if(self.userName != ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              sql = " select phonenum from family where username='%s'"%(self.userName)
              cursor.execute(sql)
              data= cursor.fetchone()
              for row in data:
                        self.phonenum = row

              cursor.close()
              db.close()


              return self.phonenum


    
    def changephone(self,newphone):
        if(self.userName != ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              self.phonenum = newphone

              
              
              sql = "update family set phonenum='%d' where username='%s'"%(newphone,self.userName)
              try:
  
   
                   cursor.execute(sql)
   
                   db.commit()
              except:
                  
                   db.rollback()
              cursor.close()
              db.close()
        else:
            return 0
            #账户未登录




    def changepassword(self,password):
        if(self.userName != ''):
              db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
              cursor = db.cursor()
              self.password = password

              
              
              sql = "update family set password='%d' where username='%s'"%(password,self.userName)
              try:
  
   
                   cursor.execute(sql)
   
                   db.commit()
              except:
                  
                   db.rollback()
              cursor.close()
              db.close()
        else:
            return 0
            #账户未登录
    def garbageinformation(self):
        if(self.userName != ''):
            db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mydb")
            cursor = db.cursor()
            sql1 = "select count(*) from garbage where username='%s'and state=3"%(self.userName)
            sql2 = "select count(*) from garbage where username='%s'and state=4"%(self.userName)
            cursor.execute(sql1)
            data = cursor.fetchone()
            for row in data:
                garbage_correct_count = row
                #正确分类的垃圾数量
            cursor.execute(sql2)
            data = cursor.fetchone()
            for row in data:
                garbage_wrong_count = row
                #错误分类的垃圾数量
            
            sql3 = "select garbage_id,username,garbage_collector_id from garbage where username='%s' and state=3"%(self.userName)
            sql4 = "select garbage_id,username,garbage_collector_id from garbage where username='%s' and state=4"%(self.userName)
            cursor.execute(sql3)
            data = cursor.fetmany(garbage_correct_count)
            for garbage_data in data:
                print(garbage_data[0])#garbage_id
                print(garbage_data[1])#username
                print(garbage_data[2])#garbage_collector_id

            cursor.execute(sql4)
            data = cursor.fetmany(garbage_wrong_count)
            for garbage_data in data:
                print(garbage_data[0])#garbage_id
                print(garbage_data[1])#username
                print(garbage_data[2])#garbage_collector_id
            



            
            cursor.close()
            db.close()
        else:
            return 0
            






         
