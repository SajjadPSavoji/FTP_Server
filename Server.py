import socket 
from _thread import *
import threading
import json
from Request import SRequest as Req
from Response import SRecponse as Res

class Server():
    def __init__(self, ip='', listen_port=1234, queue_size=10):
        self.ip_ = ip
        self.port_ = listen_port
        self.QSize_ = queue_size

        self.config()

    def config(self):
        self.routines = {}
        # read json file and make appropriate routines
        return
        raise NotImplementedError()
    
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
            raise Exception("connection lost")
        # close current connection
        c.close()


        # accept client command port {c_cmnd_port}
        c_cmnd_sock, addr = s_cmnd_sock.accept()  
        # send ACK
        c_cmnd_sock.send("ACK".encode())
        # recieve ACK
        msg = c_cmnd_sock.recv(1024).decode()
        if not msg == "ACK":
            raise Exception("connection lost")
        print("command socket set up succesfully")


        # accept client data port {c_data_port}
        c_data_sock, addr = s_data_sock.accept() 
        # send ACK
        c_data_sock.send("ACK".encode())
        # recieve ACK
        msg = c_data_sock.recv(1024).decode()
        if not msg == "ACK":
            raise Exception("connectin lost")
        print("data socket set up succesfully")

        # hal nadashtam ino doros konam badan doros mikonam
        self.c_cmnd_sock = c_cmnd_sock
        self.c_data_sock = c_data_sock
        
        self.req_handler()

    def req_handler(self):
        while True:
            msg = self.c_cmnd_sock.recv(1024)
            req = Req(msg)
            print("command recieved: ", req.__repr__())
            #redirect to a function that handles requests :))
            res = None
            try:
                self.ath_check(req)
                res = self.routine_handler(req)
            except Res as r:
                print("in except block")
                res = r
            self.log(res)
            self.service(res)

    def ath_check(self, req):
        if ("sid" in req) or (req["routine"] == "USER") or (req["routine"] == "PASS"):
            pass
        raise Res(530, "Not loged in")

    def routine_handler(self, req):
        if req["routine"] in self.routines:
            return self.routines[[req["routine"]]].service(req)
        else:
            return Res(502, "Command not implemented")

    def log(self, res):
        return
        raise NotImplementedError()

    def service(self, res):
        self.c_cmnd_sock.send(res.__repr__()) # send response
        msg = self.c_cmnd_sock.recv(1024).decode()     # receive ACK
        if not msg == "ACK":
            self.exit()
        self.c_cmnd_sock.send("ACK".encode()) # send ACK

        # send file whenever necessarry
        if "file" in res:
            self.send_file(res)

    
    def exit(self):
        self.c_data_sock.close()
        self.c_cmnd_sock.close()
        exit()

    def send_file(self, res):
        raise NotImplementedError()

    

        

    
