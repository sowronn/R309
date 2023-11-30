import socket
import threading


def main():
    port = 1234
    try:
        reply = ""
        message = ""
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(1)
        conn, address = server_socket.accept()
        reply = ""
        message = ""
        t1 = threading.Thread(target=reception, args=(conn,))
        t1.start()
        envoie(conn)


    except ConnectionAbortedError:
        print('connection stopped')
    except ConnectionRefusedError:
        print('connection refused')
    except ConnectionResetError:
        print('connection reinitialized')
    except OSError:
        pass

    else:
        if message == "arret":
            server_socket.close()


def reception(conn):
    flag = False
    while flag == False:
        try:
            message = conn.recv(1024).decode()
            print(message)
            if message == 'arret':
                server_socket.close()
                flag = True

            elif message == 'bye':
                conn.send(message.encode())
                conn.close()
                flag = True
                main()


        except ConnectionAbortedError:
            print('connection stopped')
        except ConnectionRefusedError:
            print('connection refused')
        except ConnectionResetError:
            print('connection reinitialized')
        except OSError:
            pass

        else:
            print('')


def envoie(conn):
    flag = False
    while flag == False:
        reply = input('reply = ')
        try:
            conn.send(reply.encode())
            print(reply)
            if reply == "arret":
                server_socket.close()
                flag = True


        except ConnectionAbortedError:
            print('connection stopped')
        except ConnectionRefusedError:
            print('connection refused')
        except ConnectionResetError:
            print('connection reinitialized')
        except OSError:
            pass

        else:
            print('')


if __name__ == '__main__':
    main()