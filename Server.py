from ATHRoutine  import ATHRoutine  as ATH
from PWDRoutine  import PWDRoutine  as PWD
from LISTRoutine  import LISTRoutine as LST
from MKDRoutine  import MKDRoutine  as MKD
from RMDRoutine  import RMDRoutine  as RMD
from CWDRoutine  import CWDRoutine  as CWD
from HELPRoutine import HELPRoutine as HLP
from DLRoutine   import DLRoutine   as DL
from Request     import SRequest    as Req
from Response    import SRecponse   as Res
from User        import User
from Log         import Log
from _thread import *
import os
import socket 
import threading
import json

class Server():
    def __init__(self, queue_size=10):
        self.QSize_ = queue_size

        self.init_addr()
        self.init_dir(str(self.port_))
        self.config()
        self.init_socks()

    def init_socks(self):
        self.lstn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lstn_sock.bind((self.ip_, self.port_))
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock.bind((self.ip_, self.dport_))
        print("socket binded to %s" %(self.port_))

    def init_addr(self):
        self.ip_ = ''
        with open("config.json") as config:
            data = json.load(config)
            self.port_ = data["commandChannelPort"]
            self.dport_ = data["dataChannelPort"]
        

    def init_dir(self, dirname):
        parent_dir = os.getcwd()
        new_path = os.path.join(parent_dir, dirname)
        try:
            os.mkdir(new_path)
        except:
            pass

        self.dir = new_path

    def config(self):
        self.routines = {}
        with open("config.json") as config:
            data = json.load(config)

            # ath unit
            ath = ATH(data["users"])
            self.routines["USER"] = ath
            self.routines["PASS"] = ath
            self.routines["QUIT"] = ath
            
            #Directory routines
            pwd = PWD()
            self.routines["PWD"]  = pwd
            
            lst = LST(self.dir)
            self.routines["LIST"] = lst

            mkd = MKD(self.dir)
            self.routines["MKD"] = mkd

            rmd = RMD(self.dir)
            self.routines["RMD"] = rmd

            cwd = CWD(self.dir)
            self.routines["CWD"] = cwd

            dl = DL(self.dir,"config.json")
            self.routines["DL"] = dl

            #HELP
            hlp = HLP(self.routines)
            self.routines["HELP"] = hlp

            #log
            self.log = Log(data["logging"])
            

    def portal(self, c, addr):
        self.client_hand_shake(c, addr)
        # try:
        #     self.client_hand_shake(c, addr)
        # except Exception as e:
        #     print("client offline:", e)
    
    def run(self):
        self.lstn_sock.listen(self.QSize_)
        print("socket is listening")

        while True:
            client, addr = self.lstn_sock.accept()
            print('Got connection from', addr)
            start_new_thread(self.portal, (client,addr,))
            
    def client_hand_shake(self, c, addr):
        # make new sockets { data_sock}
        s_data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_data_sock.bind((self.ip_, 0))

        # listen on data_port
        s_data_sock.listen(1)
        # send port numbers to client
        msg = str(s_data_sock.getsockname()[1])
        c.send(msg.encode())
        # recieve ACK
        msg = c.recv(1024).decode()
        print("ACK recieved")
        if not msg == "ACK":
            c.close()
            raise Exception("connection lost")
       
        # accept client data port {c_data_port}
        c_data_sock, addr = s_data_sock.accept() 
        # send ACK
        c_data_sock.send("ACK".encode())
        # recieve ACK
        msg = c_data_sock.recv(1024).decode()
        if not msg == "ACK":
            raise Exception("connectin lost")
        print("data socket set up succesfully")

        user = User(c, c_data_sock)
        
        self.req_handler(user)

    def req_handler(self, user):
        while True:
            msg = user.cmnd_sock.recv(1024)
            if msg.decode() == "":
                continue
            req = Req(msg)
            self.log(user, req)
            print("command recieved: ", req.__repr__())
            res = None
            try:
                self.ath_check(req)
                res = self.routine_handler(req, user)
            except Res as r:
                res = r
            self.log(user, res)
            self.service(res, user)
            if res == user.end_res: user.exit()

    def ath_check(self, req):
        if req["sid"] is not None:
            self.routines["USER"].check(req)

        elif (req["routine"] == "USER") or (req["routine"] == "PASS") or (req["routine"] == "HELP"):
            pass

        else:
            raise Res(530)

    def routine_handler(self, req, user):
        if req["routine"] in self.routines:
            return (self.routines[req["routine"]]).service(req, user)
        else:
            return Res(502)

    def service(self, res, user):
        user.cmnd_sock.send(res.__repr__()) # send response
        msg = user.cmnd_sock.recv(1024).decode()     # receive ACK
        if not msg == "ACK":
            self.exit()
        user.cmnd_sock.send("ACK".encode()) # send ACK
        # send file whenever necessarry
        if "file" in res:
            print("-------- sending file ------------")
            self.send_file(res, user)

    
    def exit(self):
        raise NotImplementedError()

    def send_file(self, res, user):
        user.data_sock.send(res.data()) # send file
        msg = user.data_sock.recv(1024).decode()     # receive ACK
        if not msg == "ACK":
            self.exit()
        user.data_sock.send("ACK".encode()) # send ACK

    

        

    

