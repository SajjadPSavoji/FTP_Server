from mail_test import send_mail

default_mail = "sinasharifi.ut.ac.ir"
default_id = "c2luYXNoYXJpZmkK"
default_pass = "UzFuYTk4MDY="
default_msg = "YOU ARE OUT OF CREDIT"

class Email():
    def __init__(self):
        '''
        any necessary fileds
        !!! UPDATE Acounting.py line 13 when you are done
        '''
        pass
    def __call__(self, user_info):
        try:
            send_mail(default_mail, user_info["email"], default_id, default_pass, default_msg)
        except Exception as msg:
            print(msg.args)
        '''
        user_info is a dict containing the following fields: "user", "size", "email", "alert"

        DELTE THIS COMMENT WHEN YOUR DONE!!!
        REMEMBER THAT MULTIPLE THREADS WILL ATTEMPT TO USER THIS SINGLE OBJECT, 
        IN CASE OF RACE CONDITION HANDLE IT YOUR SOMEWAY
        '''
        pass
