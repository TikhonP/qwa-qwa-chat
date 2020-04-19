import socket
import threading
from encryption import symmetric_encrypt, symmetric_decrypt
import sys


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


def read_sok():
    while True:
        data = sor.recv(1024)
        try:
            sys.stdout.write('\r' + symmetric_decrypt(data, key) + '\n')
        except UnicodeDecodeError as e:
            print('\r' + '...        ' + '\n')
        prompt()


# if(len(sys.argv) < 3):
#     print('Usage : python client2.py hostname port')
#     sys.exit()


host = '192.168.31.158'#sys.argv[1]
port = 5050#int(sys.argv[2])

server = (host, port)  # Данные сервера
alias = input("Username: ")  # Вводим наш псевдоним
key = input("Key: ")
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(('', 0))  # Задаем сокет как клиент
message = '<' + alias + '> Connected to server'
sor.sendto((symmetric_encrypt(message, key)),
           server)  # Уведомляем сервер о подключении
potok = threading.Thread(target=read_sok)
potok.start()
print('Connected to remote host. Start sending messages')
prompt()

while 1:
    mensahe = input()
    if mensahe == 'exit':
        potok.kill()
        potok.join()
        sys.exit()
    message = '<' + alias + '> ' + mensahe
    sor.sendto((symmetric_encrypt(message, key)), server)
    prompt()
