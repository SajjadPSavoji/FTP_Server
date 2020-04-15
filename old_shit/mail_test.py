import socket

mail_port = 25
ending = "\r\n"

def send_mail(email_from, email_to, AUTH_USER, AUTH_PASS, message):

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

# send_mail("sinasharifi@ut.ac.ir", "salimnia.ah@ut.ac.ir", 
#             "c2luYXNoYXJpZmkK", "UzFuYTk4MDY=", "YOU ARE OUT OF CREDIT")