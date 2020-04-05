#import libs
import socket 
from _thread import *
import threading

listen_port = 1230

class Server():
    def __init__(self, ip='', listen_port=1234, queue_size=10):
        self.ip_ = ip
        self.port_ = listen_port
        self.QSize_ = queue_size


    def run(self):
        lstn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lstn_sock.bind((self.ip_, self.port_))
        print("socket binded to %s" %(self.port_))
        lstn_sock.listen(self.QSize_)
        print("socket is listening")

        while True:
            client, addr = lstn_sock.accept()
            print('Got connection from', addr)
            start_new_thread(self.client_hand_shake, (client,addr,))
            
    def client_hand_shake(self, c, addr):
        # make new sockets {cmnd_sock , data_sock}
        s_cmnd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_cmnd_sock.bind((self.ip_, 0))
        s_data_sock.bind((self.ip_, 0))

        # listen on cmnd_port
        s_cmnd_sock.listen(1)
        # listen on data_port
        s_data_sock.listen(1)
        
        # send port numbers to client
        msg = str(s_cmnd_sock.getsockname()[1]) +" "+ str(s_data_sock.getsockname()[1])
        c.send(msg.encode())
        # recieve ACK
        msg = c.recv(1024).decode()
        print("ACK recieved")
        if not msg == "ACK":
            c.close()
            raise Exception()
        # close current connection
        c.close()
        
        # accept client command port {c_cmnd_port}
        c_cmnd_sock, addr = s_cmnd_sock.accept()  
    
        # send ACK
        c_cmnd_sock.send("ACK".encode())
        # recieve ACK
        msg = c_cmnd_sock.recv(1024).decode()
        if not msg == "ACK":
            raise Exception()
        print("command socket set up succesfully")


        # accept client data port {c_data_port}
        c_data_sock, addr = s_data_sock.accept() 

        # send ACK
        c_data_sock.send("ACK".encode())
        # recieve ACK
        msg = c_data_sock.recv(1024).decode()
        if not msg == "ACK":
            raise Exception()
        print("data socket set up succesfully")
        
        #redirect to a function that handles requests :))

if __name__ == "__main__":
    server = Server(listen_port=listen_port)
    server.run()