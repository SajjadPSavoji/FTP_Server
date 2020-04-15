import socket

mail_port = 25
ending = "\r\n"


class Email():
    def __init__(self):
        self.default_mail = "sinasharifi@ut.ac.ir"
        self.default_id = "c2luYXNoYXJpZmkK"
        self.default_pass = "UzFuYTk4MDY="
        self.default_msg = "YOU ARE OUT OF CREDIT"  

    def __call__(self, user_info):
        try:
            self.send_mail(self.default_mail, user_info["email"], self.default_id, self.default_pass, self.default_msg)
        except Exception as msg:
            print(msg.args)
        

    def send_mail(self, email_from, email_to, AUTH_USER, AUTH_PASS, message):
        # print("from, to:", email_from, email_to)
        email_from = "<"+email_from+">"
        email_to = "<"+email_to+">"
        mail_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mail_socket.connect(("mail.ut.ac.ir", mail_port))
        print("connecting to mail.ut.ac.ir")
        msg = mail_socket.recv(1024).decode()
        if msg[0:3] != '220':
            raise Exception("server not responding")

        mail_socket.send(("HELO SINA" + ending).encode())
        print("sending HELO")
        msg = mail_socket.recv(1024).decode()
        if msg[0:3] != '250':
            raise Exception("server not responding")

        mail_socket.send(("MAIL FROM: " + email_from + ending).encode())
        # print("MAIL FROM: <sinasharifi@ut.ac.ir>")
        msg = mail_socket.recv(1024).decode()
        if msg[0:3] != '250':
            raise Exception("User not found")

        mail_socket.send(("AUTH LOGIN" + ending).encode())
        # print("Authentication:")
        mail_socket.recv(1024).decode()

        mail_socket.send((AUTH_USER + ending).encode())
        mail_socket.recv(1024).decode()

        mail_socket.send((AUTH_PASS + ending).encode())
        msg = mail_socket.recv(1024).decode()
        print(msg)
        if msg[0:3] != '235':
            raise Exception("Authentication failed")

        mail_socket.send(("RCPT TO: " + email_to + ending).encode())
        msg = mail_socket.recv(1024).decode()
        if msg[0:3] != '250':
            raise Exception("User not found")

        mail_socket.send(("DATA" + ending).encode())
        msg = mail_socket.recv(1024).decode()
        if msg[0:3] != '354':
            print(msg)
            raise Exception("Data failed")

        mail_socket.send((message + ending + "." + ending).encode())
        msg = mail_socket.recv(1024).decode()
        print(msg)
        if msg[0:3] != '250':
            raise Exception("Sending failed")

        mail_socket.send(("QUIT" + ending).encode())
        print(mail_socket.recv(1024).decode())
        return 0
