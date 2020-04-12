import threading
import datetime

class Log():
    def __init__(self, dict):
        self.lk = threading.Lock()
        self.path = dict["path"]
        self.enabel = dict["enable"]

    def __call__(self, user, logable):
        if not self.enabel : return
        self.lk.acquire()
        time = datetime.datetime.now()
        with open(self.path , "a+") as f:
            f.write(f"[{time}]-{user}\n{logable}\n")
        self.lk.release()


        

