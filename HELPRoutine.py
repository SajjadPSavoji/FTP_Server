from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from ATHRoutine import ATHRoutine as ATH
from DIRRoutine import PWDRoutine as PWD
from DIRRoutine import LISTRoutine as LST
import uuid

class HELPRoutine(base):
    def __init__(self, routines):
        super().__init__()
        self.routines = routines

    def service(self, req, user):
        if req["routine"] == "HELP":
            return self.help_service(req ,user)
        else:
            raise Exception("request not supported")

    def help_service(self, req, user):
        help_msg = ""
        for routine in self.routines:
            help_msg += self.routines[routine].help_str()
        return Res(214, help_msg, user.sid)