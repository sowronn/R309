import socket
import time

host = "127.0.0.1"
port = 1234
flag = False

client_socket = socket.socket()
client_socket.connect((host, port))

while not flag:
    message = input('message =')
    time.sleep(1)
    try:
        client_socket.send(message.encode())
        reply = client_socket.recv(1024).decode()
        print(reply)

        if message == 'bye' or reply == "bye":
            client_socket.close()
            flag = True

        if reply == "arret" or message == "arret":
            client_socket.close()
            flag = True



    except ConnectionAbortedError:
        print('connection stopped')
    except ConnectionRefusedError:
        print('connection refused')
    except ConnectionResetError:
        print('connection reinitialized')

    else:
        print('end')