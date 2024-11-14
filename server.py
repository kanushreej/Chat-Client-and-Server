import socket
import threading

host = "127.0.0.1" # localhost
port = 56756

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []

def handle(client):
    while True:
        try:
            data = ""
            while True:
                newData = client.recv(1)
                newData = newData.decode()

                if newData == "\n":
                    newData = ""
                    break
                data += newData
            print(data)
            
            if data[0:10] == "HELLO-FROM":
                handshake(data, client)
            if data == "WHO":
                who(client)
            elif data[0:4] == "SEND":
                stringBytes = "SEND-OK\n"
                client.sendall(stringBytes.encode("utf-8"))
                send(data, client)
            else:
                stringBytes = "BAD-RQST-HDR\n"
                client.sendall(stringBytes.encode("utf-8"))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            break

def who(client):
    try:
        stringBytes = "WHO-OK " + ",".join(usernames) + "\n"
        client.sendall(stringBytes.encode("utf-8"))
    except:
        stringBytes = "BAD-RQST-BODY\n"
        client.sendall(stringBytes.encode("utf-8"))

def handshake(data, sock):
    try:
        username = data[11:]
        if len(usernames) >= 63:
            stringBytes = "BUSY\n"
            sock.sendall(stringBytes.encode("utf-8"))
        if username in usernames:
            stringBytes = "IN-USE\n"
            sock.sendall(stringBytes.encode("utf-8"))
        else:
            usernames.append(username)
            clients.append(sock)
            stringBytes = "HELLO " + username + "\n"
            sock.sendall(stringBytes.encode("utf-8"))
        print(usernames)
    except:
        stringBytes = "BAD-RQST-BODY\n"
        sock.sendall(stringBytes.encode("utf-8"))

def send(data, client):
    try:
        data = data.split(" ")
        if data[1] in usernames:
            destinationIndex = usernames.index(data[1])

            userIndex = clients.index(client)
            sendFrom = usernames[userIndex]
            
            sock = clients[destinationIndex]
            stringBytes = "DELIVERY " + sendFrom + " " + " ".join(data[2:]) + "\n"
            sock.sendall(stringBytes.encode("utf-8"))
        else:
            stringBytes = "UNKNOWN\n"
            client.sendall(stringBytes.encode("utf-8"))
    except:
        stringBytes = "BAD-RQST-BODY\n"
        client.sendall(stringBytes.encode("utf-8"))

def receive():
    
    while True:
        sock, address = server.accept()

        thread = threading.Thread(target=handle, args=(sock,))
        thread.start()

print("Server is listening...")
receive()
