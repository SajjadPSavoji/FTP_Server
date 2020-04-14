from Routine      import Routine      as base
from Response     import SRecponse    as Res
from Request      import SRequest     as Req
from Athorization import Athorization as Athor
from Path         import Path
from File         import File
from Accounting   import Accounting
import os

class DLRoutine(base):
    def __init__(self, base_dir, config_path):
        super().__init__()
        self.base = base_dir
        self.accounting = Accounting(config_path)
        self.athor = Athor(self.base, config_path)

    @staticmethod
    def help_str():
        return """DL <file> will download the file "file".\n"""

    def service(self, req, user):
        if req["routine"] == "DL":
            self.check_syntx(req)
            return self.dl_service(req ,user)
        else:
            raise Exception("request not supported")

    def check_syntx(self, req):
        if len(req["args"]) > 1 : raise Res(501)
        if len(req["flags"])> 0 : raise Res(501)

    def check_athor(self, req, user):
        path = self.get_file_path(req, user)
        self.athor(path, user)
    
    def check_accounting(self, user, file):
        self.accounting(user, file)

    def dl_service(self, req, user):
        path = self.get_file_path(req, user)
        file = File(path)
        self.check_athor(req, user)
        self.check_accounting(user, file)
        return Res(226, file=file)
        

    def get_file_path(self, req, user):
       return Path().join(self.base, req["args"][0], user.dir)
        