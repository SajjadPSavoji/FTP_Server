from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from File     import File
from Path     import Path
import uuid
import os
from os import listdir
from os.path import isfile, join

class LISTRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """LIST, It is used to find out the files in current directory.\n"""

    def service(self, req, user):
        if req["routine"] == "LIST":
            return self.list_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def list_service(self, req, user):
        mypath = os.path.join(self.base, user.dir)

        if os.path.exists(mypath) == 0:
            user.dir = '.'
            return Res(214, msg="Dir doesnt exist")

        # mypath = self.base
        file_and_dirs = listdir(mypath)
        onlyfiles = [f for f in file_and_dirs if isfile(join(mypath, f))]
        names = ""
        for f in file_and_dirs:
            names += f
            names += "\n"
        # return Res(226)
        return Res(226, file=File(str=names))