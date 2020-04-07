from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from Routine  import Routine
import uuid

class HELPRoutine(base):
    def __init__(self, routines):
        super().__init__()
        self.routines = routines

    def service(self, req, user):
        if req["routine"] == "HELP":
            return self.help_service(req)
        else:
            raise Exception("request not supported")

    def help_service(self, req):
        help_msg = ""
        for routine in self.routines:
            help_msg += self.routines[routine].help_str()
        return Res(214, help_msg)

    @staticmethod
    def help_str():
        return """
        HELP <no arg> shows all the available commands

        """