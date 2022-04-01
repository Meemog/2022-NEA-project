from Datastructures import Queue

class Player:
    def __init__(self, address, connection):
        self.address = address
        self.connection = connection
        self.connected = True
        self.msgsToSend = Queue()
        self.msgsReceived = Queue()
        self.loggedIn = False

        self.username = ""

        self.textWritten = ""

    def Reset(self):
        self.textWritten = ""
    