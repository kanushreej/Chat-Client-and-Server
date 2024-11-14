import socket
import threading
import os

def run_sock():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_port = ("143.47.184.219", 5378)
    sock.connect(host_port)

def receive():

    while True:

        data = ""

        while True:
            newData = sock.recv(1)
            newData = newData.decode()

            if newData == "\n":
                newData = ""
                break
            data = data + newData

        if data[0:6] == "WHO-OK":
            print ("Currently logged in users: " + data[7:])
            
        elif data[0:8] == "DELIVERY":
            data = data.split(" ")
            print(data[1] + " has sent you a message: " + " ".join(data[2:]))
            
        elif (data[0:7] == "UNKNOWN"):
            print("The user you are trying to reach is not currently logged in :(")

        elif (data == "BAD-RQST-HDR"):
            print("There is an error in the header")
        
        elif (data == "BAD-RQST-BODY"):
            print("There is an error in the body")

def handshake(username):

    run_sock()
    stringBytes = "HELLO-FROM " + username + "\n"
    sock.sendall(stringBytes.encode("utf-8"))
    data = sock.recv(4096)
    data = data.decode()
    if (data == "IN-USE\n"):
        print("This username is already in use. Try another one!\n")
        username = input("Enter your username: ")
        handshake(username)
    elif (data == "BUSY\n"):
        print( "The maximum number of clients has been reached, you can't log in")


username = input("Enter your username: ")
handshake(username)

def send():

    print("Options: \n- Type '!quit' to shutdown the client\n- Type '!who' to list all currently logged-in users\n- Type '@username message' to send messages to other users.\n ")

    while True:
        userInput = input()

        if (userInput == ""):
            print("Invalid Input")

        elif (userInput == "!who"):
            stringBytes = "WHO\n"
            sock.sendall(stringBytes.encode("utf-8"))
                    
        elif (userInput[0] == "@"):
            userInput = userInput[1:]
            userData = userInput.split()
            stringBytes = "SEND " + " ".join(userData) + "\n"
            sock.sendall(stringBytes.encode("utf-8"))

        elif (userInput == "!quit"):
            os._exit(0)

sendThread = threading.Thread(target=send)
receiveThread = threading.Thread(target=receive)
    
sendThread.start()
receiveThread.start()

sendThread.join()
receiveThread.join()

#sendThread.setDaemon(True)
#receiveThread.setDaemon(True)

'''- dynamic
- empty data
- request headers'''
    









    

    
    
    
    
    
    
