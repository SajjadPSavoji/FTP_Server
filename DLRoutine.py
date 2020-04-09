from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from Path     import Path
from File     import File
import os

class DLRoutine(base):
    def __init__(self, base_dir):
        super().__init__()
        self.base = base_dir

    @staticmethod
    def help_str():
        return """DL <file> will download the file "file".\n"""

    def service(self, req, user):
        if req["routine"] == "DL":
            self.check_syntx(req)
            self.check_athor()
            return self.dl_service(req ,user)
        else:
            raise Exception("request not supported")

    def check_syntx(self, req):
        if len(req["args"]) > 1 : raise Res(501)
        if len(req["flags"])> 0 : raise Res(501)

    def check_athor(self):
        return
        raise NotImplementedError()
        # for athorization checks
    
    def check_accounting(self):
        return
        raise NotImplementedError()
        # for accounting part

    def dl_service(self, req, user):
        path = self.get_file_path(req, user)
        file = File(path)
        return Res(226, file=file)
        

    def get_file_path(self, req, user):
       return Path().join(self.base, req["args"][0], user.dir)
        