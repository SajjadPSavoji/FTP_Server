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
    def __init__(self):
        super().__init__()

    @staticmethod
    def help_str():
        return """PWD, It is used to check the current working directory.\n"""

    def service(self, req, user):
        if req["routine"] == "PWD":
            return self.pwd_service(req ,user)
        else:
            raise Exception("request not supported")

    def pwd_service(self, req, user):
        my_dir = user.dir
        return Res(214, my_dir)


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
        # mypath = self.base
        file_and_dirs = listdir(mypath)
        onlyfiles = [f for f in file_and_dirs if isfile(join(mypath, f))]
        names = ""
        for f in file_and_dirs:
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