from Response import SRecponse as Res
from Email    import Email
import threading
import json

class Accounting():
    def __init__(self, config_path):
        self.path = config_path
        self.lk = threading.Lock()
        self.load_info()

        # raise not implmente Erro()
        self.email = Email()


    def load_info(self):
        with open(self.path) as config:
            data = json.load(config)
            self.users = data["accounting"]["users"]
            self.enable = data["accounting"]["enable"]
            self.th = data["accounting"]["threshold"]

    def update_info(self):
        self.lk.acquire()
        with open(self.path) as config:
            data = json.load(config)
        with open(self.path, "w") as config:
            data["accounting"]["users"] = self.users
            json.dump(data, config, indent=4)
        self.lk.release()

    def __call__(self, user, file):
        if not self.enable: return
        if not self.has_user(user): return
        info = self.get_user_info(user)
        if self.can_pay(info, file):
            self.pay(info, file)
            self.update_info()
            self.check_th(info)
        else: raise Res(425)

    def has_user(self, user):
        for d in self.users:
            if d["user"] == user.username: return True
        return False

    def get_user_info(self, user):
        for d in self.users:
            if d["user"] == user.username: return d

    def can_pay(self, user_info, file):
        if user_info["size"] >= file.size: 
            return True
        return False

    def pay(self, user_info , file):
        user_info["size"] -= file.size

    def check_th(self, user_info):
        if user_info["size"] <= self.th and user_info["alert"]:
            self.email(user_info)


