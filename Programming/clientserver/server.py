import socket
import threading

HEADER = 8
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname()) #Gets the local IP address
ADDRESS = (SERVER, PORT) #Makes a tuple for the address
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for ipv4. SOCK_STREAM is for TCP, SOCK_DGRAM is UDP
server.bind(ADDRESS)

def GetMsgs(conn,addr):
    #receiving messages
    conn.setblocking(False)
    try:
        msgLen = conn.recv(HEADER).decode(FORMAT) #Waits for message with length 8 bytes to be received from the client and then decodes it 
    except socket.error:
        return " "
    if msgLen:  #First message will always be empty
        msgLen = int(msgLen)

        conn.setblocking(True)
        msg = conn.recv(msgLen).decode(FORMAT) #Waits for a message with length msgLen to be received
        
        return msg

def SendMsg(newMsg, conn):
    encMessage = newMsg.encode(FORMAT) #encodes msg with utf-8
    msgLen = len(encMessage)
    msgLen = str(msgLen).encode(FORMAT) 
    msgLen += b' ' * (HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
    #b' ' means the byte representation of a space
    conn.send(msgLen)
    conn.send(encMessage)
    newMsg = ""
    return newMsg

def HandleClient(conn, addr):
    print(f"New Client: {addr}")  #Outputs the new client's local address
    newMsg = "Connection established"
    #create new thread for getting messages
    while True: 
        GetMsgs(conn, addr)
        #sending messages
        if newMsg:
            newMsg = SendMsg(newMsg, conn)
        #put stuff here for server to do to change newMsg

def GetClient():
    server.listen() #Looks for connections
    threads = []
    while True:
        conn, addr = server.accept() #When connection occurs
        thread = threading.Thread(target=HandleClient, args=(conn, addr)) #Makes a new thread for the client handling so when it listens it doesn't stop the whole program
        thread.start()  #Starts the thread
        threads.append(thread)

#server starts here
print("Starting server")
GetClient()