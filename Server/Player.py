class Player:
    def __init__(self, address, connection):
        self.address = address
        self.connection = connection
        self.msgsToSend = []
        self.msgsReceived = []
        self.username = ""

    def SendMsg(self, msg):
        self.msgsToSend.append(msg)