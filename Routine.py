class Routine():
    def __init__(self):
        pass
    def service(self, req, user):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError