import socket
import select

PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PORT))
clients = []  # Массив где храним адреса клиентов
print("Chat server started on port " + str(PORT))
while 1:
    data, addres = sock.recvfrom(1024)
    print(addres, clients)
    if addres not in clients:
        clients.append(addres)  # Если такова клиента нету , то добавить

    for client in clients:
        if client == addres:
            continue  # Не отправлять данные клиенту который их прислал
        sock.sendto(data, client)
