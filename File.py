import os
class File():
    def __init__(self, abs_path = None, str = ""):
        self.str = str
        self.path = abs_path
        if self.path is not None:
            self.load_file()
        self.size = len(self.str)

    def __repr__(self):
        return self.str

    def load_file(self):
        with open(self.path) as file:
            self.str = file.read()

    def save_file(self):
        with open(self.path, "x") as file:
            file.write(self.str)