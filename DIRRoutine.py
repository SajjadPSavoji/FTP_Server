from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from File     import File
import uuid
import os
from os import listdir
from os.path import isfile, join

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
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """LIST, It is used to find out the files in current directory.\n\t"""

    def service(self, req, user):
        if req["routine"] == "LIST":
            return self.list_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def list_service(self, req, user):
        mypath = os.path.join(self.base, user.dir)
        # mypath = self.base
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        names = ""
        for f in onlyfiles:
            names += f
            names += "\n"
        # return Res(226)
        return Res(226, file=File(str=names))


