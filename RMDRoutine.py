from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from File     import File
from Path     import Path
import uuid
import os
from os import listdir
from os.path import isfile, join

class RMDRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """RMD, It is used to delete a file or directory.\n"""

    def service(self, req, user):
        if req["routine"] == "RMD":
            return self.rmd_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def rmd_service(self, req, user):
        mypath = os.path.join(self.base, user.dir)
        if len(req["args"]) == 0:
            return Res(501)
        
        # #check if address is local 
        # if req["args"][0][0] == '/':
        #     dirpath = os.path.join(self.base, req["args"][0][1:])
        # else:
        #     dirpath = os.path.join(mypath, req["args"][0])
        dirpath = Path().join(self.base, req["args"][0], user.dir)
        
        if req["flags"] == ['-f']:
            # rmv dir
            try:
                if os.path.isdir(dirpath):
                    if not os.listdir(dirpath):
                        os.rmdir(dirpath)
                        print("Dir " , dirpath ,  " Deleted ")
                    else:
                        print(dirpath ,  " is not a empty")
                        return Res(500, msg="is not a empty")    
                else:
                    print(dirpath ,  " is not a directory")
                    return Res(500, msg="is not a directory")

            except FileNotFoundError:
                print("Dir " , dirpath ,  " Dir doesnt exist or is not empty")
                return Res(500, msg="Dir doesnt exist or is not empty")
        else:
            #rmv file
            try:
                if os.path.isfile(dirpath):
                    os.remove(dirpath)
                    print("Dir " , dirpath ,  " Deleted ")
                else:
                    print(dirpath ,  " is not a file")
                    return Res(500, msg="is not a file")

            except FileExistsError:
                print("Dir " , dirpath ,  " doesnt exist")
                return Res(500, msg="File doesnt exist")
        
        # print("This dir contains:",[f for f in listdir(mypath)])
        return Res(250, dirpath, user.sid)