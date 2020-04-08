from Response import SRecponse as Res
import os
class File():
    def __init__(self, abs_path = None, str = "", name=None):
        self.name = name
        self.str = str
        self.path = abs_path
        if self.path is not None:
            self.load_file()
        self.size = len(self.str)

    def __repr__(self):
        return self.str

    def __str__(self):
        if self.name is not None:
            return self.name + ':\n' + self.str
        else:
            return self.str

    def data(self):
        return (self.name , self.str)

    def load_file(self):
        try:
            with open(self.path) as file:
                self.str = file.read()
                self.name = os.path.basename(file.name)
        except:
            raise Res(500, "invalid file name")

    def save(self, path=None):
        if path is None: path = self.path

        with open(path, "w") as file:
            file.write(self.str)

    def load(self, res):
        self.name = res["file"][0]
        self.str  = res["file"][1]
        self.size = len(self.str)
        if self.name is not None:
            self.path = os.path.join("./" + self.name)