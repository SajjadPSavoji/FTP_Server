import socket
import json
from Request import CRequest as Req
from Response import CRecponse as Res
from Response import bcolors
from File import File
import os
prompt_command = f"{bcolors.OKBLUE}[---]{bcolors.ENDC}: "
prompt_init    = f"{bcolors.OKBLUE}>>>>>{bcolors.ENDC}:"

class Client():
    def __init__(self, ip='', server_listen_port=8000):
        self.ip_ = ip
        self.port_ = server_listen_port
        self.sid = None

    def init_dir(self, port):
        parent_dir = os.getcwd()
        new_path = os.path.join(parent_dir, str(port))
        try:
            os.mkdir(new_path)
        except:
            pass
        os.chdir(new_path)

    def reset(self):
        self.sid = None

    def update_sid(self, res):
        if res["sid"] is not None:
            self.sid = res["sid"]

    def run(self):
        while True : 
            cmnd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_sock   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cmnd_sock.bind((self.ip_, 0))
            self.init_dir(str(cmnd_sock.getsockname()[1]))
            # listen on data port on client
            data_sock.listen(1)
            # connect to server
            cmnd_sock.connect((self.ip_, self.port_))
            # send data port to server
            msg = str(data_sock.getsockname()[1]).encode()
            cmnd_sock.send(msg)
            # accept incoming connection
            s_data_sock, _ = data_sock.accept() 
           
            self.server_hand_shake(s_data_sock, cmnd_sock)
            self.command_handler()
            self.reset()
            
    def server_hand_shake(self, s_data_sock, s_cmnd_sock):
        self. s_cmnd_sock = s_cmnd_sock 
        self. s_data_sock = s_data_sock 
        print(prompt_init,"connection established.")
    
    def command_handler(self):
        while(True):
            req = Req(input(prompt_command), self.sid)
            quit_check = self.service(req)
            if quit_check == 1:
                return 1

    def service(self, req):
        self.s_cmnd_sock.send(req.__repr__())
        msg = self.s_cmnd_sock.recv(1024)
        res = Res(msg)
        # check stuff
        self.s_cmnd_sock.send("ACK".encode())
        self.s_cmnd_sock.recv(1024)

        self.update_sid(res)
        print(res)

        if "file" in res:
            self.rcv_file(req, res)

        if res["code"] == 221: 
            return 1
        return 0

    def rcv_file(self, req, res):
        msg = self.s_data_sock.recv(res["file"])
        file = Res(msg)
        # check stuff
        self.s_data_sock.send("ACK".encode())
        self.s_data_sock.recv(1024)
        self.file_service(req, file)

    def file_service(self, req , file):
        if req["routine"]=="LIST":
            self.list_handler(file)
        elif req["routine"]=="DL":
            self.dl_handler(file)
        else:
            raise NotImplementedError()

    def list_handler(self, file):
        f = File()
        f.load(file)
        print(f)
    
    def dl_handler(self, file):
        f = File()
        f.load(file)
        print(f)
        f.save()
        

    

