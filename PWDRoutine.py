from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from File     import File
from Path     import Path
import uuid
import os
from os import listdir
from os.path import isfile, join

class PWDRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """PWD, It is used to check the current working directory.\n"""

    def service(self, req, user):
        if req["routine"] == "PWD":
            return self.pwd_service(req ,user)
        else:
            raise Exception("request not supported")

    def pwd_service(self, req, user):
        mypath = os.path.join(self.base, user.dir)
        if os.path.exists(mypath) == 0:
            user.dir = '.'
        
        my_dir = user.dir
        return Res(214, my_dir)