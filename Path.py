from Response import SRecponse as Res
import os
class Path():
    def join(self, base, relative, user_dir = ""):
        dst = None
        if   self.is_local(relative):   dst= os.path.join(base, user_dir, relative)
        elif self.is_abs(relative)  :   dst= os.path.join(base, relative[1:])
        self.if_exceed_base(base, dst)

        return os.path.normpath(dst)

    def join_user_dir(self, relative, user_dir):
        dst = None
        if   self.is_local(relative):   dst= os.path.join(user_dir, relative)
        elif self.is_abs(relative)  :   dst= relative[1:]

        return os.path.normpath(dst)
        

    def is_local(self, path):
        return not self.is_abs(path)

    def is_abs(self, path):
        return path[0] == "/"

    def if_exceed_base(self, base, dst):
        dst  = os.path.normpath(dst)
        base = os.path.normpath(base)
        if len(dst) < len(base):
            raise Res(500, "invalid path")
    