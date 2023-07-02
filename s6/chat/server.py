import os
import socket
import threading
import keyboard

# Connection Data
host = ('127.0.0.1', 55555)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(host)
server.listen()

# Lists For Clients and Their Nicknames
clients = dict()


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            nickname = clients.get(client)
            clients.pop(client)
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            print(f'{nickname} disconnected')
            client.close()
            break


# Receiving / Listening Function
def receive():
    while True:
        # if keyboard.read_key() == "q":
        #     break
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        clients[client] = nickname

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# выход из программы
def stop():
    os._exit(0)


print("Server if listening...")
# выход из программы по хоткею
keyboard.add_hotkey('ctrl+s', stop)
try:
    receive()
# обработка ошибки чтобы не выключался сервер
except ConnectionResetError:
    pass
finally:
    server.close()
