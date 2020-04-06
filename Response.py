import json

class SRecponse(Exception):
    def __init__(self, number, msg="ok"):
        self.__dict__ = {"code": number, "msg":msg}
    
    def __repr__(self):
        return json.dumps(self.__dict__).encode()

    def __contains__(self, key):
        return key in self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]

class CRecponse(Exception):
    def __init__(self, number, msg="ok"):
        self.__dict__ = {"code": number, "msg":msg}
    
    def __repr__(self):
        return json.dumps(self.__dict__).encode()

    def __contains__(self, key):
        return key in self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]