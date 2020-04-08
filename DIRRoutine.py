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
        my_dir = user.dir
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


class MKDRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """MKD, It is used to create a file or directory.\n\t"""

    def service(self, req, user):
        if req["routine"] == "MKD":
            return self.mkd_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def mkd_service(self, req, user):
        mypath = os.path.join(self.base, user.dir)
        if len(req["args"]) == 0:
            raise Exception("bad arguments")
        
        #check if address is local 
        if req["args"][0][0] == '/':
            dirpath = os.path.join(self.base, req["args"][0][1:])
        else:
            dirpath = os.path.join(mypath, req["args"][0])

        print("++", dirpath)
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
        
        print("This dir contains:",[f for f in listdir(mypath)])
        return Res(257, dirpath, user.sid)


class RMDRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """RMD, It is used to delete a file or directory.\n\t"""

    def service(self, req, user):
        if req["routine"] == "RMD":
            return self.rmd_service(req ,user)
        else:
            raise Exception("request not supported")
    
    def rmd_service(self, req, user):
        mypath = os.path.join(self.base, user.dir)
        if len(req["args"]) == 0:
            raise Exception("bad arguments")
        
        #check if address is local 
        if req["args"][0][0] == '/':
            dirpath = os.path.join(self.base, req["args"][0][1:])
        else:
            dirpath = os.path.join(mypath, req["args"][0])
        
        print("++", dirpath)
        if req["flags"] == ['-f']:
            # rmv dir
            try:
                os.rmdir(dirpath)
                print("Dir " , dirpath ,  " Deleted ") 
            except FileNotFoundError:
                print("Dir " , dirpath ,  " Dir doesnt exist or is not empty")
                return Res(500, msg="Dir doesnt exist or is not empty")
        else:
            #rmv file
            try:
                os.remove(dirpath)
                print("Dir " , dirpath ,  " Deleted ") 
            except FileExistsError:
                print("Dir " , dirpath ,  " doesnt exist")
                return Res(500, msg="File doesnt exist")
        
        print("This dir contains:",[f for f in listdir(mypath)])
        return Res(250, dirpath, user.sid)

class CWDRoutine(base):
    def __init__(self, base_path):
        super().__init__()
        self.base = base_path

    @staticmethod
    def help_str():
        return """CWD, It is used to change the working directory.\n\t"""

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
        
        #check if address is local 
        if req["args"][0][0] == '/':
            user.dir = os.path.join(".", req["args"][0][1:])
        else:
            user.dir = os.path.join(user.dir, req["args"][0])
        
        mypath = os.path.join(self.base, user.dir)
        # check if it is a valid dir
        if os.path.exists(mypath):
            pass
        else:
            user.dir = last_dir
            raise Exception("Dir doesnt exist")
        print("This dir contains:",[f for f in listdir(mypath)])
        return Res(212, msg="Successful change.", sid=user.sid)