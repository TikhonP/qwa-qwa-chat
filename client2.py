import socket
import threading
from encryption import symmetric_encrypt, symmetric_decrypt
import sys

key = '567hbjkhvjkhvjkvjhkvkjvjkvjkvvhgdcfdzszsredftyvbiuppokpkmokok'

def read_sok():
    while 1:
        data = sor.recv(1024)
        print(symmetric_decrypt(data, key))

if(len(sys.argv) < 3): 
    print('Usage : python client2.py hostname port')
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

server = (host, port)  # Данные сервера
alias = input("Username: ")  # Вводим наш псевдоним
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(('', 0))  # Задаем сокет как клиент
message = '<' + alias + '> Connected to server'
sor.sendto((symmetric_encrypt(message, key)),
           server)  # Уведомляем сервер о подключении
potok = threading.Thread(target=read_sok)
potok.start()

while 1:
    mensahe = input()
    message = '<' + alias + '> ' + mensahe
    sor.sendto((symmetric_encrypt(message, key)), server)
