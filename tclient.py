import socket
import threading

def receive_message():
    try:
        while True:
            response = client.recv(1024)
            if not response:
                break
            print(response.decode("utf-8"))
    except ConnectionResetError:
        print("Server not available for now.")

def send_message():
    try:
        while True:
            message = "<%s> " % username + input()
            if message == "<%s> " % username + "END":
                client.close()
            else:
                client.send(message.encode("utf-8"))
    except ConnectionAbortedError:
        print("User %s has disconnected." % username)

client = socket.socket()

_host = "127.0.0.1"
_port = 33003

print("Waiting for server response...")
try:
    client.connect((_host, _port))
except socket.error as err:
    print("Failed because: %s" % err)

username = input("Username: ")

t = threading.Thread(target=receive_message)
t.start()
send_message()
