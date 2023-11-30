import socket

port = 1234

reply = ""
message = ""

while reply != "arret" and message != "arret":
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    reply = ""
    message = ""
    while message != "bye" and reply != "bye" and message != "arret" and reply != "arret":
        try:
            reply = input('reply = ')
            message = conn.recv(1024).decode()
            print(message)
            conn.send(reply.encode())


        except ConnectionAbortedError:
            print('connection stopped')
        except ConnectionRefusedError:
            print('connection refused')
        except ConnectionResetError:
            print('connection reinitialized')



        else:
            if message == "arret" or reply == "arret":
                server_socket.close()