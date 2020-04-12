### User is a container for thread specific data
from Response import SRecponse as Res
class User():
    def __init__(self, c_cmnd_sock, c_data_sock, dir = "."):
        self.username = None
        self.password = None
        self.sid = None

        self.cmnd_sock = c_cmnd_sock
        self.data_sock = c_data_sock
        self.ip = c_cmnd_sock.getsockname()[0]
        self.port = c_cmnd_sock.getsockname()[1]
        # each thread needs emulated working directory
        self.dir = dir
        self.end_res = Res(230, "Logged out")

    def __str__(self):
        return f"user:{self.username}, ip:{self.ip}, port:{self.port}"

    def set_username(self, username):
        self.username= username

    def set_password(self, password):
        self.password = password

    def set_sid(self, sid):
        self.sid = sid

    def exit(self):
        self.cmnd_sock.close()
        self.data_sock.close()
        self.username = None
        self.password = None
        self.sid = None
        self.cmnd_sock = None
        self.data_sock = None
        exit()
