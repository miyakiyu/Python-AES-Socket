import socket
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


nickname = input("Choose your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
client.connect(('127.0.0.1', 48763)) #connecting client to server


## salt your key ##
salt = b'\xd8\xfbY\xe1\xe1+\x06I\xc6\xb3\x10xl\xd9\xd0\xbc'
password = 'nek0isme0w'
key = PBKDF2(password,salt,16) #now we have a key
key_file = "key.bin"
with open(key_file,"wb") as f :
    f.write(key)
cipher = AES.new(key,AES.MODE_ECB) #use for encrypt or decrypt

## DEFINE ##
def receive():
    while True: #making valid connection
        message = client.recv(1024).decode()
        if message == 'NICKNAME':
            client.send(nickname.encode('ascii'))
        else:
            ciphertext = message.encode()
            orinal_message = unpad(cipher.decrypt(ciphertext),AES.block_size) #decrypt message 
            print(orinal_message.decode()) 

def write():
    while True: #message layout
        message = '{}: {}'.format(nickname, input(''))
        ciphertext = cipher.encrypt(pad(message.encode(),AES.block_size)) #encrypt message
        client.send(ciphertext)


## MAIN ##
receive_thread = threading.Thread(target=receive) #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write) #sending messages 
write_thread.start()