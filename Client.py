import socket
import json
from Request import CRequest as Req
from Response import CRecponse as Res
from Response import bcolors
from File import File
import os
prompt_command = f"{bcolors.OKBLUE}[---]{bcolors.ENDC}: "

class Client():
    def __init__(self, ip='127.0.0.1', server_listen_port=1234):
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
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.init_dir(client_sock.getsockname()[1])
            client_sock.connect((self.ip_, self.port_))

            msg = list(map(int, client_sock.recv(1024).decode().split()))
            print("message from server recieved: ",msg)
            client_sock.send("ACK".encode())
            client_sock.close()
            self.server_hand_shake(msg[0], msg[1])
            self.command_handler()
            self.reset()
            
    def server_hand_shake(self, cmnd_port, data_port):
        # make new sockets {cmnd_sock , data_sock}
        s_cmnd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #connecting to command socket
        # result = s_cmnd_sock.connect_ex(('127.0.0.1',cmnd_port)) ---> checks if port is open
        # print(result)
        s_cmnd_sock.connect((self.ip_, cmnd_port))
        msg = s_cmnd_sock.recv(1024).decode()
        if not msg == "ACK":
            s_cmnd_sock.close()
            raise Exception()
        s_cmnd_sock.send("ACK".encode())
        print("command socket set up succesfully")

        #connecting to data socket
        s_data_sock.connect((self.ip_, data_port))
        msg = s_data_sock.recv(1024).decode()
        if not msg == "ACK":
            s_cmnd_sock.close()
            s_data_sock.close()
            raise Exception()
        s_data_sock.send("ACK".encode())

        self. s_cmnd_sock = s_cmnd_sock 
        self. s_data_sock = s_data_sock 
        print("data socket set up succesfully")
    
    def command_handler(self):
        print("Ready for command:")
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
            print("file in res")
            self.rcv_file(req, res)

        if res["code"] == 221: #or res.sid == None:
            return 1
        return 0

    def rcv_file(self, req, res):
        msg = self.s_data_sock.recv(res["file"])#res{"file"} now contais size
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
        

    

