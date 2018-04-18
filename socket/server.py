import socket
import pickle

class packet():
    def __init__(self,int,type,):
        self.int = int
        self.string = string
       
    def getint(self):
        return self.int
    def getstring(self):
        return self.string
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('10.162.17.114', 6002))
sock.listen(5)
print('Server', socket.gethostbyname('localhost'), 'listening ...')
while True:  
    myconnection, addr = sock.accept()
    recvedMsg = myconnection.recv(1024)
    message=pickle.loads(recvedMsg)
    print(message.getint(),message.getstring())


    
