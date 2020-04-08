from Routine  import Routine   as base
from Response import SRecponse as Res
from Request  import SRequest  as Req
import uuid

class ATHRoutine(base):
    def __init__(self, users):
        self.__dict__ = self.gen_dict(users)
        self.sids_ = []

    @staticmethod
    def help_str():
        return """USER [name], Its argument is used to specify the user's string.
PASS [pass], Its argument is used to check user's validity and authentication.
QUIT, It is used to log the user out.\n"""

    def service(self, req, user):
        if req["routine"] == "USER":
            return self.user_service(req, user)
        elif req["routine"] == "PASS":
            return self.pass_service(req, user)
        elif req["routine"] == "QUIT":
            return self.quit_service(req, user)
        else:
            raise Exception("request not supported")

    def user_service(self, req, user):
        self.check_request(req, user)
        self.check_not_logged_in(req, user)
        if user.username is not None:
            return Res(536)
        if req["args"][0] in self.__dict__:
            user.username = req["args"][0]
            return Res(331)
        else:
            return Res(430)

    def pass_service(self, req, user):
        self.check_request(req, user)
        self.check_not_logged_in(req, user)
        if user.username is None:
            return Res(503)
        if user.password is not None:
            return Res(536, "Already logged in", user.sid)
        if req["args"][0] == self.__dict__[user.username]:
            user.password = req["args"][0]
            self.assign_sid(user)
            return Res(230, None, user.sid)
        else:
            return Res(430)

    def quit_service(self, req, user):
        # check logged in
        self.check_quit_request(req, user)
        self.check(req)
        self.sids_.remove(user.sid)
        return Res(221)

    def check_quit_request(self, req, user):
        if len(req["args"]) >= 1 or len(req["flags"])>=1:
            raise Res(501, None, user.sid)
        
    def assign_sid(self, user):
        new_sid = str(uuid.uuid1())
        user.sid = new_sid
        self.sids_.append(new_sid) 
            
    def check(self, req):
        if not req["sid"]in self.sids_:
            raise Res(535)

    def check_not_logged_in(self, req, user):
        if (user.username is not None) and (user.password is not None):
            raise Res(536, "Already logged in", user.sid)

        if "sid" not in req:
            return
        if req["sid"] in self.sids_:
            raise Res(536, "Already logged in", user.sid)

    def check_request(self, req, user):
        if not len(req["args"]) == 1:
            raise Res(501, None, user.sid)

    def gen_dict(self, users):
        new_dic = {}
        for user in users:
            new_dic[user["user"]] = user["password"]
        return new_dic


