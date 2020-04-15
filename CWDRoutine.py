from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from File     import File
from Path     import Path
import uuid
import os
from os import listdir
from os.path import isfile, join

class CWDRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """CWD, It is used to change the working directory.\n"""

    def service(self, req, user):
        if req["routine"] == "CWD":
            return self.cwd_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def cwd_service(self, req, user):
        last_dir = user.dir
        if len(req["args"]) == 0:
            user.dir = "."
            return Res(212, msg="Successful change.", sid=user.sid)
        
        # #check if address is local 
        # if req["args"][0][0] == '/':
        #     norm_path = os.path.join(".", req["args"][0][1:])
        # else:
        #     norm_path = os.path.join(user.dir, req["args"][0])
        # # Normalizes the path -> ../..
        # norm_path = os.path.normpath(norm_path)
        dirpath = Path().join(self.base, req["args"][0], user.dir) #final destination
        norm_path = Path().join_user_dir(req["args"][0], user.dir)
        user.dir = norm_path

        mypath = os.path.join(self.base, user.dir)
        # check if it is a valid dir
        if os.path.exists(mypath) == 0:
            user.dir = last_dir
            return Res(214, msg="Dir doesnt exist")
        # elif user.dir[:2] == "..":
        #     user.dir = "."
        #     mypath = os.path.join(self.base, user.dir)
        #     return Res(214)
        elif os.path.isdir(mypath) == 0:
            user.dir = last_dir
            return Res(214, msg="is not a Dir")
            
        # print("This dir contains:",[f for f in listdir(mypath)])
        return Res(212, msg="Successful change.", sid=user.sid)