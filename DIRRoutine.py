from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
import uuid
import os

class PWDRoutine(base):
    def __init__(self):
        super().__init__()

    @staticmethod
    def help_str():
        return """PWD, It is used to check the current working directory.\n\t"""

    def service(self, req, user):
        if req["routine"] == "PWD":
            return self.pwd_service(req ,user)
        else:
            raise Exception("request not supported")

    def pwd_service(self, req, user):
        my_dir = user.dir_
        return Res(404, my_dir, user.sid)


# NOT COMPLETE YET
class LISTRoutine(base):
    def __init__(self, users):
        self.__dict__ = self.gen_dict(users)
        self.sids_ = []

    @staticmethod
    def help_str():
        return """LIST, It is used to find out the files in current directory.\n\t"""

    def service(self, req, user):
        if req["routine"] == "LIST":
            return self.list_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def list_service(self, req, user):
        print(user.dir_)
        for root, dirs, files in os.walk(user.dir_):
            print(root, dirs, files)
            for filename in files:
                print(filename)
        return Res(226, None , user.sid)

    def gen_dict(self, users):
        new_dic = {}
        for user in users:
            new_dic[user["user"]] = user["password"]
        return new_dic


