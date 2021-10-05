import socket
import threading

HEADER = 8
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname()) #Gets the local IP address
ADDRESS = (SERVER, PORT) #Makes a tuple for the address
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for ipv4. SOCK_STREAM is for TCP, SOCK_DGRAM is UDP
server.bind(ADDRESS)

def HandleClient(conn, addr):
    print("New client:", addr)  #Outputs the new client's local address

    connected = True
    while connected: 
        msgLen = conn.recv(HEADER).decode(FORMAT) #Waits for message with length 8 bytes to be received from the client and then decodes it 
        if msgLen:  #First message will always be empty
            msgLen = int(msgLen)
            msg = conn.recv(msgLen).decode(FORMAT) #Waits for a message with length msgLen to be received
            
            if msg == "!DISCONNECT":
                connected = False

            print(str(addr) +  ":", str(msg)) #Prints the message

    conn.close()    #This allows the user to reconnect later


def GetClient():
    server.listen() #Looks for connections
    while True:
        NumClients()
        conn, addr = server.accept() #When connection occurs
        thread = threading.Thread(target=HandleClient, args=(conn, addr)) #Makes a new thread for the client handling so when it listens it doesn't stop the whole program
        thread.start()  #Starts the thread
        

def NumClients():
    print("Clients:", str(threading.active_count() - 1)) #prints number of active clients (-1 due to GetClient being a thread). This would really only ever be 2 in the actual project

#server starts here
print("Starting server")
GetClient()
