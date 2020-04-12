import json
class CRequest():
    def __init__(self, str, sid=None):
        self.__dict__ = self.parse(str)
        self.__dict__["sid"] = sid

    def parse(self, command):
        my_dict = {}
        command = command.split()
        my_dict["routine"] = command.pop(0)
        my_dict["flags"] = []
        my_dict["args"]  = []

        for part in command:
            if part[0] == '-':
                my_dict["flags"].append(part)
            else:
                my_dict["args"].append(part)

        return my_dict

    def __repr__(self):
        return json.dumps(self.__dict__).encode()

    def __str__(self):
        return json.dumps(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]

    def __len__(self):
        return len(self.__dict__)


class SRequest():
    def __init__(self, str):
        self.__dict__ = json.loads(str.decode())

    def __repr__(self):
        return json.dumps(self.__dict__).encode()

    def __str__(self):
        return json.dumps(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]

    def __len__(self):
        return len(self.__dict__)

