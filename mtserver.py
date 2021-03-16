import socket
import _thread

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def client_thread(connection):
    try:
        while True:
            data = connection.recv(2048).decode("utf-8")
            if not data:
                break
            broadcast(str.encode(data), connection)
    except ConnectionResetError:
        print("Client disconnecting.")
    connection.close()

server_socket = socket.socket() # use defaults of AF_INET, SOCK_STREAM

_host = "127.0.0.1"
_port = 33003
ThreadCount = 0

print("Waiting for connection...")
try:
    server_socket.bind((_host, _port))
except socket.error as err:
    print("Failed. Reason: %s" % err)
server_socket.listen(5)

list_of_clients = []

try:
    while True:
        client, address = server_socket.accept()
        list_of_clients.append(client)
        print("Connection received from %s!" % address[0], address[1])
        _thread.start_new_thread(client_thread, (client,))
        ThreadCount += 1
        print("ThreadCount: %s" % ThreadCount)
except:
    print("Connection closed.")
