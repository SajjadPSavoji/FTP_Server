### User is a container for thread specific data
class User():
    def __init__(self, c_cmnd_sock, c_data_sock):
        self.username_ = None
        self.password_ = None
        self.sid_ = None

        self.cmnd_sock = c_cmnd_sock
        self.data_sock = c_data_sock
        # each thread needs emulated working directory
        self.dir_ = "./"

    def set_username(self, username):
        self.username_= username

    def set_password(self, password):
        self.password_ = password

    def set_sid(self, sid):
        self.sid_ = sid

    def exit(self):
        self.cmnd_sock.close()
        self.data_sock.close()
