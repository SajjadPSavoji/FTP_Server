import json
class CRequest():
    def __init__(self, str):
        self.__dict__ = self.parse(str)

    def parse(self, command):
        my_dict = {}
        command = command.split()
        my_dict["command"] = command.pop(0)
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

class SRequest():
    def __init__(self, str):
        self.__dict__ = json.loads(str.decode())
        
    def __repr__(self):
        return json.dumps(self.__dict__).encode()
