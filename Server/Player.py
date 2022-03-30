from Datastructures import Queue

class Player:
    def __init__(self, address, connection):
        self.address = address
        self.connection = connection
        self.msgsToSend = Queue()
        self.msgsReceived = Queue()
        self.loggedIn = False

        #Details used for stats section and logging in / creating new player
        self.username = ""