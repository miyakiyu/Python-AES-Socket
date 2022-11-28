import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
server.bind(("127.0.0.1",48763)) #binding host and port to socket
server.listen()

clients = []
nicknames = []

## get the key file ##
get_key = "key.bin"
with open(get_key,"rb") as f:
    key = f.read()

## DEFINE ##
def broadcast(message):  #broadcast function declaration
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        #recieving valid messages from client
        message = client.recv(1024) #get the message 
        broadcast(message)

def receive(): #accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))  

        client.send('NICKNAME'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode())
        client.send('Connected to server!'.encode())
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

## MAIN ##
receive()