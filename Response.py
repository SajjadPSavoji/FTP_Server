import json

class SRecponse(Exception):
    def __init__(self, number, msg=None, sid=None, file=None):
        self.__dict__ = {"code": number, "msg" : code_mapper(number, msg).code_map(),
                          "sid": sid   , "file": file}
        if file is None:
            self.__dict__.pop("file")
    
    def __repr__(self):
        if "file" in self.__dict__:
            temp = self.__dict__["file"]
            self.__dict__["file"] = temp.size + 1024
            ret = json.dumps(self.__dict__).encode()
            self.__dict__["file"] = temp
        else:
            ret = json.dumps(self.__dict__).encode()
        return ret
    
    def data(self):
        if not "file" in self.__dict__:
            return self.__repr__()
        self.__dict__["file"] = repr(self.__dict__["file"])
        return json.dumps(self.__dict__).encode()

    def __contains__(self, key):
        return key in self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]

    def __eq__(self, res):
        return self.__dict__ == res.__dict__

class CRecponse(Exception):
    def __init__(self, str):
        self.__dict__ = json.loads(str.decode())
    
    def __repr__(self):
        return json.dumps(self.__dict__).encode()

    def __contains__(self, key):
        return key in self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        code_color = self.get_code_color()
        return f"{code_color}[{self.__dict__['code']}]{bcolors.ENDC}: {self.__dict__['msg']}"

    def get_code_color(self):
        code = self.__dict__["code"]
        if code < 400:
            return bcolors.OKGREEN
        if code >= 400 and code<600:
            return bcolors.FAIL
        else: return bcolors.WARNING

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class code_mapper():
    mapping = { 331 : "User name okay, need password.",
                230 : "User logged in, proceed.",
                530 : "Not logged in.",
                503 : "Bad sequence of commands.",
                536 : "Pass needed.",
                430 : "Invalid username or password",
                257 : "created.", #
                250 : "deleted.", #
                226 : "File transfer done.",
                # 250 : "Successful change.",
                # 226 : "Successful Download.",
                214 : "",
                221 : "Successful Quit.",
                332 : "Need account for login.",
                501 : "Syntax error in parameters or arguments.",
                500 : "Error.",
                425 : "Can't open data connection.",
                502 : "Command not implemented.", 
                550 : "File unavailable.",
                535 : "Session id invalid",
                404 : ""}

    def __init__(self, number, msg):
        self.number = number
        self.msg = msg
    def code_map(self):
        if self.msg == None:
            if self.number in [250, 257]:
                raise Exception("Not possible")
            else:
                return self.mapping[self.number]
        else:
            if self.number in [250, 257]:
                return self.msg + self.mapping[self.number]
            else:
                return self.msg
