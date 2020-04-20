import socket
import sys

if len(sys.argv)<2:
    print("Usage : python server.py port")
else:
    PORT = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))
clients = []  # Массив где храним адреса клиентов
print("Chat server started on port " + str(PORT))
while 1:
    data, address = sock.recvfrom(1024)
    print(address)
    if address not in clients:
        clients.append(address)  # Если такова клиента нету , то добавить

    for client in clients:
        if client == address:
            continue  # Не отправлять данные клиенту который их прислал
        sock.sendto(data, client)
