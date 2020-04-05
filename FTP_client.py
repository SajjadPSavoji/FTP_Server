# Import socket module 
import socket
import json
from Request import CRequest as Req

server_port = 1230


class Client():
    def __init__(self, ip='127.0.0.1', server_listen_port=1234):
        self.ip_ = ip
        self.port_ = server_listen_port


    def run(self):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((self.ip_, self.port_))

        msg = list(map(int, client_sock.recv(1024).decode().split()))
        print("message from server recieved: ",msg)
        client_sock.send("ACK".encode())
        client_sock.close()
        self.server_hand_shake(msg[0], msg[1])
        self.command_handler()
            
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
            req = Req(input())
            self.s_cmnd_sock.send(req.__repr__())


if __name__ == "__main__":
    client = Client(server_listen_port=server_port)
    client.run()