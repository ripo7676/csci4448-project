class User():
    def __init__(self):
        self.username = None
        self.password = None
        self.commSocket = None

    def setCommSocket(self, socket):
        self.commSocket = socket

    def validateLogon(self, dbProxy, username, password):
        if True:
            return 1
        else:
            return False
