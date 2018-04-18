import socket
import pickle

class packet():
    def __init__(self,int,string):
        self.int = int
        self.string = string
       
    def getint(self):
        return self.int
    def getstring(self):
        return self.string

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect(('localhost', 6002))
message = packet(1,"helloworld")
sendmessage = pickle.dumps(message)
sock.send(sendmessage)
print("successfully")

