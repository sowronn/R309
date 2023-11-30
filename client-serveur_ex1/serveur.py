import socket

port = 1234
flag = False

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)
conn, address = server_socket.accept()
while not flag:
    reply = input("reply=")
    try:
        message = conn.recv(1024).decode()
        print(message)
        conn.send(reply.encode())
        if reply == "arret":
            flag = True
            conn.close()
            server_socket.close()

        elif message == "bye":
            conn.close()

    except ConnectionAbortedError:
        print('la connexion a été coupé')
    except ConnectionRefusedError:
        print('la connexion a été  refusé')
    except ConnectionResetError:
        print('la connexion a été réinitialisé')

    else:
        print("fin")
