from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from File     import File
from Path     import Path
import uuid
import os
from os import listdir
from os.path import isfile, join

class MKDRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """MKD, It is used to create a file or directory.\n"""

    def service(self, req, user):
        if req["routine"] == "MKD":
            return self.mkd_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def mkd_service(self, req, user):
        mypath = os.path.join(self.base, user.dir)
        if len(req["args"]) == 0:
            return Res(501)
        
        # #check if address is local 
        # if req["args"][0][0] == '/':
        #     dirpath = os.path.join(self.base, req["args"][0][1:])
        # else:
        #     dirpath = os.path.join(mypath, req["args"][0])
        dirpath = Path().join(self.base, req["args"][0], user.dir)

        if req["flags"] == ['-i']:
            # make file
            try:
                os.mknod(dirpath)
                print("File " , dirpath ,  " Created ") 
            except FileExistsError:
                print("File " , dirpath ,  " already exists")
                return Res(500, msg="File already exists")
        else:
            #make dir
            try:
                os.mkdir(dirpath)
                print("Directory " , dirpath ,  " Created ") 
            except FileExistsError:
                print("Directory " , dirpath ,  " already exists")
                return Res(500, msg="Dir already exists")
        
        # print("This dir contains:",[f for f in listdir(mypath)])
        return Res(257, dirpath, user.sid)