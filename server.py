import socket

PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PORT))
client = []  # Массив где храним адреса клиентов
print("Chat server started on port " + str(PORT))
while 1:
    data, addres = sock.recvfrom(1024)
    print(addres, data.hex())
    if addres not in client:
        client.append(addres)  # Если такова клиента нету , то добавить
    for clients in client:
        if clients == addres:
            continue  # Не отправлять данные клиенту который их прислал
        sock.sendto(data, clients)
