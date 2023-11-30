import socket
import time
import threading


def main():
    host = "127.0.0.1"
    port = 1234
    try:

        client_socket = socket.socket()
        client_socket.connect((host, port))
        t1 = threading.Thread(target=reception, args=(client_socket,))
        t1.start()
        envoie(client_socket)



    except ConnectionAbortedError:
        print('la connexion a été coupé')
    except ConnectionRefusedError:
        print('la connexion a été  refusé')
    except ConnectionResetError:
        print('la connexion a été réinitialisé')

    else:
        print('')


def reception(client_socket):
    flag = False
    while flag == False:
        try:
            reply = client_socket.recv(1024).decode()
            print(reply)

            if reply == 'bye' or reply == "arret":
                client_socket.close()
                flag = True

        except ConnectionAbortedError:
            print('la connexion a été coupé')
        except ConnectionRefusedError:
            print('la connexion a été  refusé')
        except ConnectionResetError:
            print('la connexion a été réinitialisé')

        else:
            print('')


def envoie(client_socket):
    flag = False
    while flag == False:
        try:
            message = input('message =')
            client_socket.send(message.encode())

            if message == 'bye' or message == "arret":
                client_socket.close()
                flag = True


        except ConnectionAbortedError:
            print('connection stopped')
        except ConnectionRefusedError:
            print('connection refused')
        except ConnectionResetError:
            print('connection reinitialized')

        else:
            print('')


if __name__ == '__main__':
    main()
