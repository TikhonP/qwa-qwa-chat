import socket
import threading
from encryption import symmetric_encrypt, symmetric_decrypt
import sys
# from console.utils import wait_keys
import json

# settings
is_pyinstaller = False
use_username = True

running = True

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


def read_sok():
    global running
    while running:
        try:
            data = sock.recv(1024)
        except ConnectionRefusedError as e:
            print('\rConnection refused...')
            break
        try:
            sys.stdout.write('\r' + symmetric_decrypt(data, key) + '\n')
        except UnicodeDecodeError as e:
            print('\r' + '...        ' + '\n')
        prompt()
    quit()

def setting():
    global host, port, alias
    if is_pyinstaller:
        host = input('Enter hostname server > ')
        port = int(input('Enter port server > '))
    else:
        if(len(sys.argv) < 3):
            print('Usage : python client2.py hostname port')
            sys.exit()
        else:
            host = sys.argv[1]
            port = int(sys.argv[2])
    if use_username:
        alias = input("Username: ")
    else:
        alias = '~'


def setup():
    global server, key, sock, t
    server = (host, port)
    key = input("Key: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(server)
    sendmsg('<' + alias + '> Connected to server')
    t = threading.Thread(target=read_sok)
    t.start()
    print('Connected to remote host. Start sending messages.')
    prompt()


def sendmsg(message):
    global key
    try:
        sock.send(symmetric_encrypt(message, key))
    except ConnectionRefusedError:
        print('\rConnection refused...')
        quit()

def quit():
    # print('If you want to quit, please press q.')
    # if wait_keys()=='q':
    sock.close()
    running = False
    t.join()
    sys.exit()


if __name__ == '__main__':
    setting()
    setup()

    while 1:
        mensahe = input()
        if mensahe == 'exit':
            quit()
        sendmsg('<' + alias + '> ' + mensahe)
        prompt()
