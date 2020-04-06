import json

class SRecponse(Exception):
    def __init__(self, number, msg="ok", sid=None):
        self.__dict__ = {"code": number, "msg":msg, "sid":sid}
    
    def __repr__(self):
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

