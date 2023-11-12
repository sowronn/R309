import socket
import time

host = "127.0.0.1"
port = 1234
flag = False

client_socket = socket.socket()
client_socket.connect((host, port))

while not flag:
    message = input("message deux points = ")
    time.sleep(1.5)
    try:
        client_socket.send(message.encode())
        reply = client_socket.recv(1024).decode()
        print(reply)
        if message == "bye" or reply == "bye":
            client_socket.close()
            flag = True

        elif message == "arret" or reply == "arret":
            client_socket.close()
            flag = True

    except ConnectionAbortedError:
        print('la connexion a été coupé')
    except ConnectionRefusedError:
        print('la connexion a été  refusé')
    except ConnectionResetError:
        print('la connexion a été réinitialisé')

    else:
        print("fin de boucle")
