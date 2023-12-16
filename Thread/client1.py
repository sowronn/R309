import socket
import threading

state = True

def envoyer(client_socket):
    global state
    while state:
        message = input("Enter your message : ")
        client_socket.send(message.encode())

        if message.lower() == 'bye':
            print("Customer stopped")
            client_socket.close()
            state = False
            break

        elif message.lower() == 'stop':
            print("Customer stopped")
            client_socket.close()
            state = False
            break

def main():
    global state
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1024))

    threading.Thread(target=envoyer, args=(client_socket,), daemon=True).start()

    while state:
        pass

if __name__ == "__main__":
    main()
