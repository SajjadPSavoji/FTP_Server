from Response import SRecponse as Res
from Path import Path
import json

class Athorization():
    def __init__(self, base, config_path):
        self.base = base
        self.path = config_path
        self.load_info()

    def load_info(self):
        with open(self.path) as config:
            data = json.load(config)
            dct = data["authorization"]
            self.enable = dct["enable"]
            self.admins = dct["admins"]
            self.files  = dct["files"]

    def __call__(self, path, user):
        if not self.enable : return
        if self.is_path_protected(path) and not self.is_user_athorized(user):
            raise Res(550)

    def is_path_protected(self, path):
        for p in self.files:
            if path == self.get_path(p): return True
        return False

    def is_user_athorized(self, user):
        for name in self.admins:
            if name == user.username : return True
        return False

    def get_path(self, path):
        return Path().join(self.base, path)
        