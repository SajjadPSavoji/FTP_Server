from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
from ATHRoutine import ATHRoutine as ATH
from DIRRoutine import PWDRoutine as PWD
from DIRRoutine import LISTRoutine as LST
import uuid

class HELPRoutine(base):
    def __init__(self, users):
        self.__dict__ = self.gen_dict(users)
        self.sids_ = []

    # def __str__(self):
    #     return """ HELP, it helps :)) """

    def service(self, req, user):
        if req["routine"] == "HELP":
            return self.help_service(req ,user)
        else:
            raise Exception("request not supported")

    def help_service(self, req, user):
        help_msg = ATH.help_str()
        help_msg += PWD.help_str()
        help_msg += LST.help_str()
        return Res(214, help_msg, user.sid)

    def gen_dict(self, users):
        new_dic = {}
        for user in users:
            new_dic[user["user"]] = user["password"]
        return new_dic
